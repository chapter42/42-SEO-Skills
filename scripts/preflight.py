#!/usr/bin/env python3
"""
42-SEO-Skills Pre-flight Check

Validates environment, dependencies, API keys, and external tools.
Determines capability tier and writes capabilities.json.

Usage:
    python3 scripts/preflight.py                     # Human-readable output
    python3 scripts/preflight.py --json              # Machine-readable JSON
    python3 scripts/preflight.py --domain example-com  # Write to 42-reports/<domain>/
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure references/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "references"))
from load_env import load_env


# ── Core packages (required for full functionality) ─────────────────────

CORE_PACKAGES = {
    "numpy": "numpy",
    "scipy": "scipy",
    "google.generativeai": "google-generativeai",
    "bs4": "beautifulsoup4",
    "requests": "requests",
    "lxml": "lxml",
    "PIL": "Pillow",
    "validators": "validators",
}

OPTIONAL_PACKAGES = {
    "playwright": "playwright",
    "reportlab": "reportlab",
    "textstat": "textstat",
    "networkx": "networkx",
    "rapidfuzz": "rapidfuzz",
    "spacy": "spacy",
    "nltk": "nltk",
    "plotly": "plotly",
    "google.oauth2": "google-auth",
    "googleapiclient": "google-api-python-client",
}


def check_python_version() -> dict:
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    ok = sys.version_info >= (3, 11)
    return {"version": version, "ok": ok, "minimum": "3.11"}


def check_packages(package_map: dict) -> dict:
    results = {}
    for import_name, pip_name in package_map.items():
        try:
            __import__(import_name)
            results[pip_name] = True
        except ImportError:
            results[pip_name] = False
    return results


def check_api_key_gemini() -> dict:
    """Validate Google Gemini API key with a lightweight call."""
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"configured": False, "valid": False, "detail": "not configured"}

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        models = list(genai.list_models())
        embedding_models = [m.name for m in models if "embedding" in m.name.lower()]
        return {
            "configured": True,
            "valid": True,
            "detail": f"{len(embedding_models)} embedding model(s) available",
        }
    except ImportError:
        return {"configured": True, "valid": None, "detail": "google-generativeai not installed"}
    except Exception as e:
        return {"configured": True, "valid": False, "detail": str(e)[:100]}


def check_api_key_dataforseo() -> dict:
    """Validate DataForSEO credentials with balance endpoint."""
    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        return {"configured": False, "valid": False, "detail": "not configured"}

    try:
        import base64
        import urllib.request
        import ssl

        auth = base64.b64encode(f"{login}:{password}".encode()).decode()
        req = urllib.request.Request(
            "https://api.dataforseo.com/v3/appendix/user_data",
            headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
            data=b"[]",
            method="POST",
        )
        # Handle macOS SSL
        try:
            ctx = ssl.create_default_context()
            resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        except ssl.SSLError:
            try:
                import certifi
                ctx = ssl.create_default_context(cafile=certifi.where())
            except ImportError:
                ctx = ssl._create_unverified_context()
            resp = urllib.request.urlopen(req, timeout=10, context=ctx)

        data = json.loads(resp.read().decode())
        if data.get("status_code") == 20000:
            money = data.get("tasks", [{}])[0].get("result", [{}])[0].get("money", {})
            balance = money.get("balance", "unknown")
            return {"configured": True, "valid": True, "detail": f"balance: ${balance}"}
        else:
            return {"configured": True, "valid": False, "detail": data.get("status_message", "auth failed")}
    except Exception as e:
        return {"configured": True, "valid": False, "detail": str(e)[:100]}


def check_api_key_gsc() -> dict:
    """Check if Google Search Console service account is configured."""
    sa_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON") or os.environ.get("GSC_SERVICE_ACCOUNT_PATH")
    if not sa_path:
        return {"configured": False, "valid": False, "detail": "not configured"}

    path = Path(sa_path)
    if not path.is_file():
        return {"configured": True, "valid": False, "detail": f"file not found: {sa_path}"}

    try:
        with open(path) as f:
            sa_data = json.load(f)
        if "client_email" in sa_data and "private_key" in sa_data:
            return {"configured": True, "valid": True, "detail": f"service account: {sa_data['client_email']}"}
        else:
            return {"configured": True, "valid": False, "detail": "invalid service account JSON"}
    except Exception as e:
        return {"configured": True, "valid": False, "detail": str(e)[:100]}


def check_screaming_frog() -> dict:
    """Check Screaming Frog CLI availability."""
    sf_path = os.environ.get("SF_CLI_PATH")

    # Platform-specific defaults
    if not sf_path:
        candidates = [
            "/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher",
            "/usr/bin/screamingfrogseospider",
            shutil.which("screamingfrogseospider") or "",
        ]
        for c in candidates:
            if c and Path(c).is_file():
                sf_path = c
                break

    if not sf_path or not Path(sf_path).is_file():
        return {"available": False, "path": None, "version": None}

    # SF CLI doesn't support --version; just confirm it exists and is executable
    return {"available": True, "path": sf_path, "version": "installed"}


def determine_tier(api_results: dict, sf_result: dict) -> int:
    """Determine capability tier based on available tools.

    Tier 1: Manual — no API keys, all skills work via paste-data + WebFetch
    Tier 2: Basic API — DataForSEO or Gemini available
    Tier 3: Full Automation — SF CLI + (GSC or embedding) + DataForSEO
    """
    has_dataforseo = api_results["dataforseo"]["configured"] and api_results["dataforseo"]["valid"] is not False
    has_gemini = api_results["gemini"]["configured"] and api_results["gemini"]["valid"] is not False
    has_gsc = api_results["gsc"]["configured"] and api_results["gsc"]["valid"] is not False
    has_sf = sf_result["available"]

    if has_sf and has_dataforseo and (has_gsc or has_gemini):
        return 3
    elif has_dataforseo or has_gemini:
        return 2
    else:
        return 1


def run_preflight(domain: str | None = None, verbose: bool = True) -> dict:
    """Run all pre-flight checks and return results."""
    load_env(domain=domain)

    python = check_python_version()
    core = check_packages(CORE_PACKAGES)
    optional = check_packages(OPTIONAL_PACKAGES)

    api_results = {
        "gemini": check_api_key_gemini(),
        "dataforseo": check_api_key_dataforseo(),
        "gsc": check_api_key_gsc(),
    }

    sf = check_screaming_frog()
    tier = determine_tier(api_results, sf)

    results = {
        "tier": tier,
        "python": python,
        "core_packages": core,
        "optional_packages": optional,
        "api_keys": api_results,
        "screaming_frog": sf,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

    return results


def to_capabilities_json(results: dict) -> dict:
    """Convert full results to compact capabilities.json format."""
    return {
        "tier": results["tier"],
        "detected": {
            "python": results["python"]["version"],
            "screaming_frog": results["screaming_frog"]["available"],
            "dataforseo": results["api_keys"]["dataforseo"].get("valid", False) or False,
            "google_api": results["api_keys"]["gemini"].get("valid", False) or False,
            "gsc": results["api_keys"]["gsc"].get("valid", False) or False,
        },
        "checked_at": results["checked_at"],
    }


def print_human_readable(results: dict) -> None:
    """Print results in human-friendly format."""
    ok = "\u2713"
    fail = "\u2717"

    print("\nPre-flight Check Results")
    print("=" * 40)

    # Python
    py = results["python"]
    sym = ok if py["ok"] else fail
    print(f"\nPython:          {py['version']} {sym}")

    # Core packages
    core = results["core_packages"]
    installed = sum(1 for v in core.values() if v)
    total = len(core)
    sym = ok if installed == total else fail
    print(f"Core packages:   {installed}/{total} installed {sym}")
    for pkg, ok_val in core.items():
        if not ok_val:
            print(f"  {fail} {pkg} — pip install {pkg}")

    # Optional packages
    opt = results["optional_packages"]
    missing = [pkg for pkg, v in opt.items() if not v]
    if missing:
        print(f"Optional:        {', '.join(missing[:5])} {fail}")

    # API Keys
    print("\nAPI Keys:")
    for name, data in results["api_keys"].items():
        label = {
            "gemini": "GOOGLE_API_KEY",
            "dataforseo": "DATAFORSEO_LOGIN",
            "gsc": "GSC_SERVICE_ACCOUNT",
        }[name]
        sym = ok if data.get("valid") else fail
        detail = data.get("detail", "")
        pad = " " * (24 - len(label))
        print(f"  {label}:{pad}{sym} ({detail})")

    # Screaming Frog
    sf = results["screaming_frog"]
    print("\nTools:")
    if sf["available"]:
        print(f"  Screaming Frog CLI:    {ok} ({sf['version']})")
    else:
        print(f"  Screaming Frog CLI:    {fail} (not found)")

    # Tier
    tier = results["tier"]
    print(f"\nCapability Tier: {tier}")
    tiers = {
        1: ("Manual", "All skills work via paste-data + WebFetch"),
        2: ("Basic API", "DataForSEO + Gemini unlocked"),
        3: ("Full Automation", "SF + GSC + embedding + DataForSEO"),
    }
    for t, (label, desc) in tiers.items():
        marker = ok if t <= tier else fail
        print(f"  Tier {t} ({label}):{' ' * (14 - len(label))}{marker} {desc}")

    print()


def write_capabilities(results: dict, domain: str | None = None) -> Path | None:
    """Write capabilities.json to 42-reports/<domain>/ if domain specified."""
    if not domain:
        return None

    project_root = Path(__file__).resolve().parent.parent
    reports_dir = project_root / "42-reports" / domain
    reports_dir.mkdir(parents=True, exist_ok=True)

    caps_path = reports_dir / "capabilities.json"
    caps = to_capabilities_json(results)

    with open(caps_path, "w", encoding="utf-8") as f:
        json.dump(caps, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return caps_path


def main():
    parser = argparse.ArgumentParser(description="42-SEO-Skills Pre-flight Check")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--domain", type=str, help="Domain slug (e.g., example-com)")
    args = parser.parse_args()

    results = run_preflight(domain=args.domain)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_human_readable(results)

    # Write capabilities.json if domain specified
    caps_path = write_capabilities(results, domain=args.domain)
    if caps_path and not args.json:
        print(f"Capabilities written to: {caps_path}")

    # Exit code: 0 if tier >= 1 (always passes), non-zero only on Python version fail
    sys.exit(0 if results["python"]["ok"] else 1)


if __name__ == "__main__":
    main()
