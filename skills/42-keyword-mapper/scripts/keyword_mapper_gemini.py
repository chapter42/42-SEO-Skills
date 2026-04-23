#!/usr/bin/env python3
"""
Keyword → Page Mapper via Gemini Embeddings (workaround for SF AI export failure)

Embeds keywords (DataForSEO ranked_keywords JSON or plain CSV) and pages
(Screaming Frog internal_html.csv with Title/H1/H2/Meta) using Google Gemini
text-embedding-004, then computes cosine similarity to find the best matching
page per keyword. Optionally cross-checks against actual ranking URL to detect
cannibalization or misallocation.

Usage:
    python3 keyword_mapper_gemini.py \\
        --keywords ranked-keywords-nl-full.json,ranked-keywords-en-full.json \\
        --pages internal_html.csv \\
        --output-dir output/ \\
        --max-pages 1000 \\
        --ranked-keywords ranked-keywords-nl-full.json,ranked-keywords-en-full.json

Requires:
    - GEMINI_API_KEY in environment
    - numpy
"""
import argparse
import csv
import json
import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import requests

API_KEY = os.environ.get("GEMINI_API_KEY")
# gemini-embedding-001 is the current stable embedding model (3072 dims).
# text-embedding-004 was deprecated. batchEmbedContents is NOT available for
# this model — only embedContent (single). Use ThreadPoolExecutor for throughput.
MODEL = "models/gemini-embedding-001"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/{model}:embedContent"
RPM_LIMIT = 90  # stay under 100 RPM free tier limit
WORKERS = 8

# Token-bucket style rate limiter shared across worker threads
_rate_lock = threading.Lock()
_rate_window = []  # timestamps of recent calls


def _rate_limit():
    """Block until we're under RPM_LIMIT for the trailing 60s window."""
    while True:
        with _rate_lock:
            now = time.time()
            # Drop timestamps older than 60s
            while _rate_window and _rate_window[0] < now - 60:
                _rate_window.pop(0)
            if len(_rate_window) < RPM_LIMIT:
                _rate_window.append(now)
                return
            sleep_for = 60 - (now - _rate_window[0]) + 0.05
        time.sleep(max(sleep_for, 0.1))


def embed_one(text, task_type="RETRIEVAL_DOCUMENT", retries=4):
    """Embed a single text via Gemini API embedContent. Returns a vector list."""
    payload = {
        "model": MODEL,
        "content": {"parts": [{"text": text[:8000]}]},
        "taskType": task_type,
    }
    url = ENDPOINT.format(model=MODEL) + f"?key={API_KEY}"
    for attempt in range(retries):
        _rate_limit()
        try:
            resp = requests.post(url, json=payload, timeout=60)
            if resp.status_code == 429 and attempt < retries - 1:
                wait = (attempt + 1) * 10
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                print(f"HTTP {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
                resp.raise_for_status()
            body = resp.json()
            return body["embedding"]["values"]
        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                time.sleep(3)
                continue
            raise


def embed_all(texts, task_type, label="items"):
    """Embed all texts concurrently with ThreadPoolExecutor + rate limiter."""
    n = len(texts)
    out = [None] * n
    completed = [0]
    lock = threading.Lock()

    def _work(i):
        out[i] = embed_one(texts[i], task_type)
        with lock:
            completed[0] += 1
            if completed[0] % 25 == 0 or completed[0] == n:
                print(f"  {label}: {completed[0]}/{n}", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(_work, i) for i in range(n)]
        for f in as_completed(futures):
            f.result()  # propagate exceptions

    return np.array(out, dtype=np.float32)


def load_keywords(paths):
    """Load keywords from one or more sources. Supports DataForSEO JSON or CSV."""
    keywords = []
    seen = set()
    for path in paths.split(","):
        path = path.strip()
        if path.endswith(".json"):
            with open(path) as f:
                d = json.load(f)
            items = d.get("tasks", [{}])[0].get("result", [{}])[0].get("items", [])
            for it in items:
                kw = it.get("keyword_data", {}).get("keyword", "").strip()
                sv = (
                    it.get("keyword_data", {})
                    .get("keyword_info", {})
                    .get("search_volume", 0)
                    or 0
                )
                serp = it.get("ranked_serp_element", {}).get("serp_item", {})
                actual_url = serp.get("url", "")
                rank = serp.get("rank_group", 99)
                if kw and kw not in seen:
                    seen.add(kw)
                    keywords.append(
                        {
                            "kw": kw,
                            "sv": sv,
                            "actual_url": actual_url,
                            "actual_rank": rank,
                        }
                    )
        else:
            with open(path, encoding="utf-8-sig") as f:
                r = csv.DictReader(f)
                for row in r:
                    kw = (row.get("keyword") or row.get("Keyword") or "").strip()
                    if kw and kw not in seen:
                        seen.add(kw)
                        keywords.append({"kw": kw, "sv": 0, "actual_url": "", "actual_rank": 99})
    return keywords


def load_pages(path, max_pages=1000, min_words=50):
    """Load pages from SF internal_html.csv. Returns list filtered + sorted by inlinks."""
    pages = []
    with open(path, encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                status = int(row.get("Status Code", "0") or 0)
            except ValueError:
                status = 0
            indexable = row.get("Indexability", "").strip().lower()
            try:
                words = int(row.get("Word Count", "0") or 0)
            except ValueError:
                words = 0
            try:
                inlinks = int(row.get("Inlinks", "0") or 0)
            except ValueError:
                inlinks = 0
            if status != 200:
                continue
            if indexable != "indexable":
                continue
            if words < min_words:
                continue
            pages.append(
                {
                    "url": row.get("Address", "").strip(),
                    "title": row.get("Title 1", "").strip(),
                    "h1": row.get("H1-1", "").strip(),
                    "h2": row.get("H2-1", "").strip(),
                    "meta": row.get("Meta Description 1", "").strip(),
                    "words": words,
                    "inlinks": inlinks,
                }
            )
    pages.sort(key=lambda p: -p["inlinks"])
    return pages[:max_pages]


def page_text(p):
    """Build text representation for embedding."""
    parts = [p["title"], p["h1"], p["h2"], p["meta"]]
    return " | ".join(x for x in parts if x)


def cosine_topk(q_emb, doc_emb, k=5):
    """Return (top_idx, sim_matrix) for each query against documents."""
    qn = q_emb / (np.linalg.norm(q_emb, axis=1, keepdims=True) + 1e-8)
    dn = doc_emb / (np.linalg.norm(doc_emb, axis=1, keepdims=True) + 1e-8)
    sims = qn @ dn.T
    top_idx = np.argsort(-sims, axis=1)[:, :k]
    return top_idx, sims


def write_report(results, output_dir, n_pages, n_keywords):
    """Write KEYWORD-MAPPER.md report."""
    cannibalization = [r for r in results if r.get("cannibalization")]
    misallocations = [r for r in results if r.get("cannibalization") and r["actual_rank"] <= 20]
    high_intent = sorted(results, key=lambda r: -r["sv"])[:30]

    md = [
        "# Keyword → Page Mapping — fireware.nl",
        "",
        f"**Generated**: {time.strftime('%Y-%m-%d')}",
        f"**Method**: Gemini gemini-embedding-001 (3072 dims) via direct API",
        f"**Pages embedded**: {n_pages} (filtered: indexable, status 200, ≥50 words)",
        f"**Keywords embedded**: {n_keywords}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|------:|",
        f"| Total keywords mapped | {len(results)} |",
        f"| Cannibalization / misallocation flagged | {len(cannibalization)} |",
        f"| Misallocations on ranking pages (rank ≤20) | {len(misallocations)} |",
        "",
        "## Top 30 Keywords by Search Volume — Best Semantic Match",
        "",
        "| # | Keyword | SV | Actual ranking URL | Semantic best match | Sim | Status |",
        "|--:|---------|---:|-------------------|--------------------|----:|--------|",
    ]
    for i, r in enumerate(high_intent, 1):
        actual = r["actual_url"].replace("https://www.fireware.nl", "") or "—"
        best = r["best_match"].replace("https://www.fireware.nl", "")
        sim = f"{r['best_score']:.2f}"
        match_status = "✅ aligned" if r["actual_url"] == r["best_match"] else "⚠️ mismatch"
        md.append(
            f"| {i} | {r['kw']} | {r['sv']} | {actual[:50]} | {best[:50]} | {sim} | {match_status} |"
        )

    md += [
        "",
        "## Cannibalization / Misallocation",
        "",
        f"Found **{len(cannibalization)}** cases where the actual ranking URL ≠ the semantically best matching page.",
        "",
    ]
    if misallocations:
        md += [
            f"### {len(misallocations)} cases on pages already ranking (rank ≤20)",
            "",
            "These are highest-priority — Google ranks the wrong page for the keyword.",
            "",
            "| Keyword | SV | Rank | Actual URL | Should be | Sim |",
            "|---------|---:|----:|-----------|-----------|----:|",
        ]
        for r in sorted(misallocations, key=lambda x: -x["sv"])[:25]:
            actual = r["actual_url"].replace("https://www.fireware.nl", "")
            best = r["best_match"].replace("https://www.fireware.nl", "")
            md.append(
                f"| {r['kw']} | {r['sv']} | {r['actual_rank']} | {actual[:50]} | {best[:50]} | {r['best_score']:.2f} |"
            )

    md += [
        "",
        "## Source",
        "",
        "- Script: `dist/42-keyword-mapper/scripts/keyword_mapper_gemini.py`",
        "- Embedding model: Google Gemini `text-embedding-004` (768 dim)",
        "- Full dataset: `keyword-mapping.json`",
        "",
    ]

    out_path = Path(output_dir) / "KEYWORD-MAPPER.md"
    out_path.write_text("\n".join(md))
    print(f"Wrote {out_path}", file=sys.stderr)


def main():
    if not API_KEY:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    ap = argparse.ArgumentParser()
    ap.add_argument("--keywords", required=True, help="DataForSEO JSON or CSV (comma-separated for multiple)")
    ap.add_argument("--pages", required=True, help="SF internal_html.csv")
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--max-pages", type=int, default=1000)
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--ranked-keywords", help="DataForSEO JSON for cannibalization detection")
    args = ap.parse_args()

    keywords = load_keywords(args.keywords)
    print(f"Loaded {len(keywords)} unique keywords", file=sys.stderr)

    pages = load_pages(args.pages, max_pages=args.max_pages)
    print(f"Loaded {len(pages)} pages (filtered, top by inlinks)", file=sys.stderr)

    page_texts = [page_text(p) for p in pages]
    kw_texts = [k["kw"] for k in keywords]

    print("Embedding pages...", file=sys.stderr)
    page_emb = embed_all(page_texts, "RETRIEVAL_DOCUMENT", "pages")
    print("Embedding keywords...", file=sys.stderr)
    kw_emb = embed_all(kw_texts, "RETRIEVAL_QUERY", "keywords")

    print("Computing similarity...", file=sys.stderr)
    top_idx, sims = cosine_topk(kw_emb, page_emb, k=args.top_k)

    results = []
    for i, k in enumerate(keywords):
        matches = []
        for j in range(min(args.top_k, top_idx.shape[1])):
            idx = int(top_idx[i, j])
            matches.append(
                {
                    "rank": j + 1,
                    "url": pages[idx]["url"],
                    "title": pages[idx]["title"],
                    "score": float(sims[i, idx]),
                }
            )
        r = {
            **k,
            "best_match": matches[0]["url"] if matches else "",
            "best_score": matches[0]["score"] if matches else 0.0,
            "alternatives": matches[1:],
        }
        if k.get("actual_url") and k["actual_url"] != r["best_match"]:
            r["cannibalization"] = {
                "actual_ranking_url": k["actual_url"],
                "semantic_best": r["best_match"],
                "delta": "consider redirect/internal link strategy",
            }
        results.append(r)

    os.makedirs(args.output_dir, exist_ok=True)
    json_path = Path(args.output_dir) / "keyword-mapping.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Wrote {json_path}", file=sys.stderr)

    write_report(results, args.output_dir, len(pages), len(keywords))


if __name__ == "__main__":
    main()
