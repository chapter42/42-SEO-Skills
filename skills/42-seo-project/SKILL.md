---
name: 42-seo-project
description: >
  SEO project orchestrator that guides the complete SEO improvement lifecycle
  from intake through audit, analysis, and implementation to ongoing monitoring.
  Manages state, tracks progress across sessions, and delegates to 49+ specialized
  SEO/GEO skills in the right order. Use when user says "SEO project", "start SEO",
  "SEO roadmap", "SEO workflow", "where do I start", "what should I fix first",
  "next step", "SEO traject", "SEO verbeterplan", "SEO stappenplan", "volgende stap".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
version: 2.0.0
tags: [orchestrator, seo, geo, project, workflow, state-machine]
---

# SEO Project Orchestrator

Guides the complete SEO/GEO improvement lifecycle for a website. Manages state
across sessions, decides which skills to run when, and tracks progress from
first intake to ongoing monitoring.

**This skill does NOT duplicate skill logic.** It delegates to existing skills
and adds sequencing, state tracking, and intelligent routing on top.

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo-project intake` | Fase 0: intake questions, homepage crawl, first impression |
| `/seo-project init` | Interactive setup: pre-flight, directory setup, .env |
| `/seo-project start <url>` | Quick start: intake + init + crawl + discover in one go |
| `/seo-project next` | Auto-detect current phase, execute next logical step |
| `/seo-project status` | Show progress dashboard without taking action |
| `/seo-project crawl [url]` | Run/re-run Phase 1: Screaming Frog crawl + Top-25 |
| `/seo-project discover [url]` | Run/re-run Phase 2: baseline audit + SEO plan |
| `/seo-project keywords` | Phase 3: keyword research & mapping |
| `/seo-project technical` | Phase 4: technical audit |
| `/seo-project content` | Phase 5: content analysis & GEO |
| `/seo-project entities` | Phase 6: entity & structured data |
| `/seo-project links` | Phase 7: internal links & structure |
| `/seo-project competitive` | Phase 8: competitive intelligence |
| `/seo-project report` | Phase 9: final report & strategy |
| `/seo-project skip <phase>` | Skip a phase, advance to next |
| `/seo-project history` | Show audit history and score trends |
| `/seo-project reset` | Clear state, start over (asks confirmation) |

---

## Phases

The SEO improvement lifecycle has 10 phases (0-9).

```
FASE 0: INTAKE & INIT
  Intake-vragen → homepage crawl → bevindingen → pre-flight → directory setup

FASE 1: CRAWL & DATA FOUNDATION
  Screaming Frog crawl (embeddings + GSC + GA) → exports → Top-25 → Top-5 selectie

FASE 2: DISCOVERY & PLANNING
  Baseline scores (SEO + GEO) → industrie-template → voorzichtig SEO-plan

FASE 3: KEYWORD RESEARCH & MAPPING
  GSC analyse → keyword-expansie → PAA → mapping → clustering → gaps

FASE 4: TECHNISCHE AUDIT
  Technische analyse op SF-data → Chrome DevTools CWV/a11y → AI-crawlers → sitemap → hreflang

FASE 5: CONTENT-ANALYSE & GEO
  Content decay (eerst!) → near-duplicates → Top-5 deep-dive → bulk health → GEO-analyse

FASE 6: ENTITY & STRUCTURED DATA
  Entiteiten → schema audit → blog-schema (indien relevant)

FASE 7: INTERNE LINKS & STRUCTUUR
  Link-analyse → link graph → taxonomie → kannibalisatie

FASE 8: COMPETITIVE INTELLIGENCE
  Brand intelligence → share of voice → competitor analyse

FASE 9: RAPPORTAGE & STRATEGIE
  Consolidatie → geprioriteerd rapport → actieplan → decision locking → implementatie-waves
```

---

### Fase 0: INTAKE & INITIALISATIE

**Goal:** Gather project context, get a first impression of the site, validate
environment, and set up the project directory.

**This is interactive.** Ask the user each question, confirm, then proceed.

#### 0.1 — Intake Questions

Stel de volgende vragen aan de opdrachtgever:

| # | Vraag | Waarom |
|---|-------|--------|
| 1 | **Wat is de domeinnaam?** | Projectmap en crawl-target |
| 2 | **Wat voor type bedrijf is het?** (SaaS, eCommerce, lokaal, publisher, B2B, agency) | Bepaalt industrie-template voor SEO-plan |
| 3 | **Wat is het product of de dienst?** | Context voor keyword research en content-beoordeling |
| 4 | **Wie is de doelgroep?** | Taal, markt, persona-context |
| 5 | **Wat zijn de belangrijkste doelen?** (meer verkeer, meer conversies, AI-zichtbaarheid, etc.) | Prioritering van fases |
| 6 | **Welke taal/markt?** (NL, EN, DE, multi-language) | Hreflang-relevantie, content-taal |
| 7 | **Zijn er concurrenten die je wilt vergelijken?** (max 3 URLs) | Competitive intelligence scope |
| 8 | **Is er een bestaand GSC/GA account beschikbaar?** | Data-beschikbaarheid bepalen |
| 9 | **Is er budget/tijdslijn?** | Impact op strategie-scope |

#### 0.2 — Homepage Crawl met Firecrawl

```
Actie: Crawl de homepage met firecrawl_scrape
Doel:  Eerste indruk ophalen — technische staat, content, structured data, meta tags
```

Analyseer de Firecrawl-output op:
- Title tag en meta description kwaliteit
- Heading structuur (H1, H2 hierarchie)
- Schema.org markup aanwezig?
- Zichtbare content-kwaliteit (first impression)
- Technische signalen (HTTPS, canonical, robots)
- Interne links vanuit homepage

#### 0.3 — Bevindingen Terugkoppelen + Vervolgvragen

Presenteer de eerste bevindingen en stel gerichte vervolgvragen:
- "Ik zie dat jullie [X] doen, klopt dat?"
- "Er is geen structured data op de homepage — is dat bewust?"
- "De site lijkt [eCommerce/SaaS/etc.] — klopt dat met jullie focus?"

#### 0.4 — Pre-flight Check

Run `python3 scripts/preflight.py` to validate the environment:
- Python version >= 3.11
- Core packages installed (numpy, scipy, google-generativeai, etc.)
- API key validation (Gemini, DataForSEO, GSC — with live endpoint checks)
- Screaming Frog CLI detection
- Capability tier determination (1=Manual, 2=Basic API, 3=Full Automation)

Show the pre-flight results to the user. If critical issues (Python version),
block and ask to fix. If optional tools missing, continue with tier note.

**Progressive Enhancement Tiers:**
- **Tier 1 (Manual):** No API keys. All skills work via paste-data + WebFetch.
- **Tier 2 (Basic API):** DataForSEO or Gemini available. Keyword research, embeddings, SERP data unlocked.
- **Tier 3 (Full Automation):** SF CLI + GSC + Gemini + DataForSEO. Automated crawls, full pipeline.

For missing optional keys, show what they unlock but don't block progress:

```
Capability Tier: 2 (Basic API)

  ✓ Gemini API (embeddings, AI analysis)
  ✓ DataForSEO (SERP data, keyword research)
  ✗ GSC (not configured — striking-distance and content-decay will need manual CSV)
  ✗ Screaming Frog (not found — crawl phase will be skipped, skills use WebFetch fallback)
```

#### 0.5 — Directory Setup

Create the project directory structure:

```
42-reports/
├── INDEX.md                          # Overzicht alle projecten + scores
├── config.json                       # Preferences (taal, SF profiel, output format)
│
└── <domain>/
    ├── STATE.md                      # Fase-status, capabilities, scores
    ├── capabilities.json             # Pre-flight resultaten (machine-readable)
    ├── INTAKE.md                     # Antwoorden op intake-vragen + homepage-analyse
    ├── TODO.md                       # Lopende takenlijst per fase
    │
    ├── exports/                      # Screaming Frog CSV exports
    │   ├── <YYYY-MM-DD>/            # Per-datum crawl snapshot
    │   │   ├── _crawl-meta.json     # SF versie, pages crawled, duration
    │   │   └── *.csv                # Export tabs
    │   └── latest -> <YYYY-MM-DD>/  # Symlink naar meest recente crawl
    │
    ├── reports/                       # Alle fase-outputs
    │   ├── DISCOVERY.md
    │   ├── TOP-25.md
    │   ├── SEO-PLAN-DRAFT.md
    │   ├── TECHNICAL-AUDIT.md
    │   ├── CONTENT-ANALYSE.md
    │   ├── GEO-ANALYSE.md
    │   ├── STRUCTURED-DATA.md
    │   ├── LINK-STRUCTUUR.md
    │   ├── COMPETITIVE-INTELLIGENCE.md
    │   ├── EINDRAPPORT.md
    │   └── pages/                    # Per-pagina deep-dive rapporten
    │
    └── history/                       # Audit snapshots over tijd
        ├── <YYYY-MM-DD>-discover.md
        └── scores.json               # Trend data [{date, seo_score, geo_score}]
```

#### 0.6 — Write capabilities.json & STATE.md

Run `python3 scripts/preflight.py --domain <domain>` to write
`42-reports/<domain>/capabilities.json` with detected tools and tier.

Initialize STATE.md with intake data. Update INDEX.md with new project row.

**Output:** `INTAKE.md`, `STATE.md`, `capabilities.json`

---

### Fase 1: CRAWL & DATA FOUNDATION

**Goal:** Run a Screaming Frog crawl to create the data foundation, then
identify the Top-25 most important pages and let the user select 5 for deep-dive.

**Delegates to:**
- `/42:screaming-frog crawl <url>` → Full technical crawl (embeddings + GSC + GA)
- `/42:screaming-frog export <url> --bulk` → Export all tabs as CSV

**Why first:** Many 42-skills require Screaming Frog export data as input:
- `42-keyword-mapper` → needs SF embedding export
- `42-link-graph` → needs Inlinks:All export
- `42-passage-analyzer` → needs SF text export
- `42-migration` → needs Internal:HTML export
- `42-meta-optimizer` → needs Internal:HTML export
- `42-striking-distance` → needs Internal:HTML export
- `42-page-health` → needs crawl data for composite scoring
- `42-near-duplicates` → needs content hashes from SF
- `42-readability` → needs SF text export

**Actions:**
1. Check Screaming Frog availability: `/42:screaming-frog check`
2. If SF available:
   - Run crawl: `/42:screaming-frog crawl <url>` with custom profile (embeddings + GSC + GA)
   - Export all tabs: `/42:screaming-frog export <url> --bulk`
   - Record crawl path in STATE.md
3. If SF NOT available:
   - Log warning: "Screaming Frog not installed — some 42-skills will have limited data"
   - Mark phase as `skipped` (not `completed`)
   - Proceed to Phase 2 with WebFetch-based crawling only

#### 1.1 — Top-25 Page Identification

After the crawl completes, combine SF + GSC data to rank the 25 most important pages.

**Priority Score Formula:**

```
Priority Score = (Organic Clicks × 0.30)
              + (Impressions × 0.20)
              + (Inlinks count × 0.15)
              + (Revenue/Conversions × 0.20)   ← indien beschikbaar
              + (Word Count > 500 bonus × 0.05)
              + (Content Decay Risk × 0.10)
```

Each factor is normalized to 0-100 before weighting. If Revenue/Conversions data
is not available (no GA integration), redistribute the 0.20 weight proportionally
across the other factors.

**Output:** `reports/TOP-25.md` with ranked table:

| # | URL | Clicks (30d) | Impressions (30d) | Avg. Position | Inlinks | Priority Score | Reden |
|---|-----|-------------|-------------------|---------------|---------|---------------|-------|

#### 1.2 — Top-25 Verification + Top-5 Selection

Present the Top-25 to the user as an interactive selection list:

```markdown
## Top-25 pagina's — Selecteer 5 voor deep-dive

| # | Selecteer | URL | Clicks | Impressions | Pos. | Score | Reden |
|---|-----------|-----|--------|-------------|------|-------|-------|
| 1 | [ ] | /product/... | 2.340 | 45.000 | 4.2 | 92 | Hoogste traffic |
| 2 | [ ] | /blog/... | 1.890 | 38.000 | 6.1 | 87 | Meeste impressies |
| ... | | | | | | | |
```

The user:
- Confirms or corrects the Top-25 ranking
- May add strategically important pages (e.g., new product page)
- **Selects 5 pages for deep-dive analysis** across Phases 4-5

Store the selection in STATE.md under `top_25_pages` and `top_5_selected`.

**Output:** SF exports in `42-reports/<domain>/exports/<YYYY-MM-DD>/`, `reports/TOP-25.md`,
Top-5 selection stored in `STATE.md`.

---

### Fase 2: DISCOVERY & PLANNING

**Goal:** Establish baseline scores and create an initial SEO plan direction.

**Delegates to:**
- `/42:audit --full <url>` → Unified SEO + GEO audit (SEO Health Score 0-100, GEO Score 0-100)
- `/42:seo-plan` → Strategic SEO plan with industry template

**Uses Phase 1 data:** If SF crawl data is available, the audit skills reference
it for richer technical analysis instead of re-crawling via WebFetch.

**Actions:**
1. Run `/42:audit --full <url>` (runs both SEO and GEO audit)
2. Capture scores per category in `DISCOVERY.md`
3. Choose industry template based on `business_type` from intake:
   - SaaS → focus on content authority, feature pages, comparison pages
   - eCommerce → focus on category pages, product schema, internal linking
   - Local → focus on GBP, local schema, NAP
   - Publisher → focus on article schema, content freshness, Discover
   - B2B → focus on thought leadership, case studies, E-E-A-T
   - Agency → focus on portfolio, case studies, service pages
4. Generate initial SEO plan direction (NOT implementation plan — that comes in Phase 9)
   - Top-3 opportunities based on data
   - Top-3 risks/problems
   - Suggested focus per phase
   - Time estimate (indicative)
5. Update STATE.md: `discover: completed`, record scores

**Shared Resources:** Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md` for E-E-A-T scoring criteria.

**Output:** `42-reports/<domain>/reports/DISCOVERY.md`, `42-reports/<domain>/reports/SEO-PLAN-DRAFT.md`

---

### Fase 3: KEYWORD RESEARCH & MAPPING

**Goal:** Understand what the site ranks for, identify gaps, and map keywords to pages.

**Delegates to (each step is a separate skill run):**

| Step | Skill | What it does |
|------|-------|-------------|
| 3.1 | GSC data from SF export | Existing keywords, positions, clicks, impressions per URL |
| 3.2 | `/42:keyword-discovery` | Seed expansion via DataForSEO (suggestions + related) |
| 3.3 | `/42:paa-scraper` | People Also Ask extraction for top keywords |
| 3.4 | `/42:keyword-mapper` | Map keywords to pages via SF embeddings + GSC data |
| 3.5 | `/42:serp-cluster` | SERP-based keyword clustering |
| 3.6 | `/42:striking-distance` | Quick wins: pages at position 4-20 |
| 3.7 | `/42:topical-map` | Hierarchical topic architecture (pillars → clusters → subtopics) |

**Actions:**
1. Analyze GSC data from SF export for existing keyword positions
2. Run keyword expansion with DataForSEO seeds (if Tier 2+)
3. Scrape PAA questions for top keywords, cluster by theme
4. Map keywords to pages, identify orphaned keywords and cannibalization
5. Cluster keywords that share SERPs
6. Identify striking distance opportunities (position 4-20)
7. Build topical map with hub-and-spoke structure
8. Update STATE.md: `keywords: completed`

**Output:** Results per step in `reports/`, update TODO.md

---

### Fase 4: TECHNISCHE AUDIT

**Goal:** Assess the technical state of the site using crawl data and spot-checks.

**Delegates to:**

| Step | Skill / Tool | What it does |
|------|-------------|-------------|
| 4.1 | `/42:technical` | Technical SEO + GEO analysis on SF data (crawlability, indexability, URL structure, mobile, security) |
| 4.2 | `chrome-devtools: debug-optimize-lcp` | Core Web Vitals on top-5 pages — LCP debugging and optimization |
| 4.2 | `chrome-devtools: a11y-debugging` | Accessibility audit on top-5 pages — WCAG compliance |
| 4.2 | `chrome-devtools: lighthouse_audit` | Full Lighthouse audit on top-5 pages |
| 4.3 | `/42:crawlers` | AI-crawler access analysis (14 crawlers, tier impact) |
| 4.4 | `/42:llmstxt` | llms.txt check and generation |
| 4.5 | `/42:sitemap` | XML sitemap validation |
| 4.6 | `/42:hreflang` | Internationalization (only if multi-language from intake) |
| 4.7 | `/42:images` | Image optimization (alt text, formats, responsive, lazy loading) |
| 4.8 | `/42:migration` | Migration check (only if relevant from intake) |

**Step 4.2 — Chrome DevTools Deep-Dive (Top-5 pages):**

For each of the 5 user-selected pages from Phase 1:
1. Run `chrome-devtools: debug-optimize-lcp` — measure and optimize LCP
2. Run `chrome-devtools: a11y-debugging` — accessibility audit per web.dev guidelines
3. Run `chrome-devtools: lighthouse_audit` — full Lighthouse (performance, a11y, best practices, SEO)

Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/cwv-thresholds.md` for CWV pass/fail thresholds.
Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/web-quality/` for accessibility and performance deep-dive criteria.

**Firecrawl as complement:** Use `firecrawl_scrape` for rendered HTML verification
on top-5 pages where JS-dependent content is suspected. SF is primary data source;
Firecrawl is supplementary for spot-checks.

**Output:** `reports/TECHNICAL-AUDIT.md`

---

### Fase 5: CONTENT-ANALYSE & GEO

**Goal:** Assess content quality, detect decay, and measure GEO readiness.

**IMPORTANT:** Content decay runs FIRST — it determines which pages need attention
and informs all subsequent content analysis decisions.

**Delegates to:**

| Step | Skill | What it does |
|------|-------|-------------|
| 5.1 | `/42:content-decay` | **FIRST** — Detect pages losing impressions/clicks, correlate with algo updates |
| 5.2 | `/42:near-duplicates` | Duplicate detection early — affects all subsequent analysis |
| 5.3 | Top-5 deep-dive stack | Full analysis per user-selected page (see below) |
| 5.4 | `/42:page-health` | Bulk health scoring top-50 URLs (configurable via `MAX_URLS` in STATE.md) |
| 5.5 | `/42:readability` | Readability sample of ~10-20 important pages |
| 5.6 | GEO analysis suite | AI visibility, citability, passage quality, platform optimization |
| 5.7 | `/42:blog` | Blog audit if blog is present (combines blog-seo-check + blog-geo + blog-schema) |

#### 5.1 — Content Decay Detection (FIRST)

Run `/42:content-decay` before any other content skill:
- Which pages are losing impressions/clicks over time?
- Correlation with known algorithm updates?
- Trend vs. one-time dip?
- Pages flagged here get priority in the deep-dive

**Data:** GSC historical data from SF export

#### 5.2 — Near-Duplicates Detection (Early)

Run `/42:near-duplicates` early — duplicates affect all subsequent analysis:
- Exact duplicates (MD5)
- Near-duplicates (MinHash)
- Semantic similarity (embeddings)
- Boilerplate vs. unique content

**Data:** SF content hashes + embeddings

#### 5.3 — Top-5 Deep-Dive

For each of the 5 user-selected pages, run the full analysis stack:

```
Per page:
├── /42:page-analysis ────── Full single-page audit
├── /42:content ──────────── Content quality (SEO + GEO dual mode)
├── /42:citability ────────── AI-citeerability scoring
├── /42:passage-analyzer ──── Passage extraction quality
├── /42:entity-extractor ──── Entities and relationships
├── /42:structured-data ───── Schema validation
├── /42:readability ────────── Readability score
├── /42:qrg ────────────────── SQRG score vs. top-3 competitors
├── chrome-devtools: lighthouse_audit ── CWV/Lighthouse per page
└── chrome-devtools: a11y-debugging ──── Accessibility per page
```

Output per page: consolidated report with scores and priorities in `reports/pages/`.

Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md` for E-E-A-T evaluation.
Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md` for content quality thresholds.

#### 5.6 — GEO Analysis

For the top-5 pages + site-wide:

| Analysis | Skill | What it does |
|----------|-------|-------------|
| AI visibility | `/42:ai-visibility` | Monitoring across 6 AI platforms |
| Citability | `/42:citability` | 5-category rubric score (already in 5.3 for top-5) |
| Passage quality | `/42:passage-analyzer` | Chunk optimization (already in 5.3 for top-5) |
| Platform optimization | `/42:platform-optimizer` | Per-platform GEO advice |
| Brand mentions | `/42:brand-intelligence` | Brand mentions + sentiment |

#### 5.7 — Blog Analysis (if blog present)

Sample of 5 blog posts:
- On-page SEO check
- GEO optimization
- Blog-specific schema (Article/BlogPosting, Author, Publisher)

**Skill:** `/42:blog` (unified skill combining blog-seo-check, blog-geo, and blog-schema)

**Output:** `reports/CONTENT-ANALYSE.md`, `reports/GEO-ANALYSE.md`, per-page reports in `reports/pages/`

---

### Fase 6: ENTITY & STRUCTURED DATA

**Goal:** Identify entities and validate/generate structured data.

**Delegates to:**

| Step | Skill | What it does |
|------|-------|-------------|
| 6.1 | `/42:entity-extractor` | NER, relationship mapping, entity density, consistency check |
| 6.2 | `/42:structured-data` | Schema audit + JSON-LD generation, sameAs strategy, @graph structure |
| 6.3 | `/42:blog` (schema component) | Article/BlogPosting schema (if blog present) |

Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/schema-types.md` for supported schema types and best practices.

**Output:** `reports/STRUCTURED-DATA.md`, generated JSON-LD files

---

### Fase 7: INTERNE LINKS & STRUCTUUR

**Goal:** Analyze link equity flow and identify structural issues.

**Delegates to:**

| Step | Skill | What it does |
|------|-------|-------------|
| 7.1 | `/42:internal-links` | Competitive link block analysis (27-block taxonomy) |
| 7.2 | `/42:link-graph` | PageRank calculation, orphaned pages, anchor text analysis |
| 7.3 | `/42:ecom-taxonomy` | eCommerce category structure (if eCommerce) |
| 7.4 | `/42:cannibalization` | Keyword cannibalization detection + consolidation recommendations |

**Output:** `reports/LINK-STRUCTUUR.md`

---

### Fase 8: COMPETITIVE INTELLIGENCE

**Goal:** Understand competitive positioning.

**Delegates to:**

| Step | Skill | What it does |
|------|-------|-------------|
| 8.1 | `/42:brand-intelligence` | Brand mentions + sentiment (Reddit, news, forums, reviews, social) |
| 8.2 | `/42:share-of-voice` | Visibility share for target keywords (CTR-weighted) |
| 8.3 | `/42:competitor-pages` | Gap analysis (optional, only if competitors specified in intake) |

**Output:** `reports/COMPETITIVE-INTELLIGENCE.md`

---

### Fase 9: RAPPORTAGE & STRATEGIE

**Goal:** Consolidate all findings into a prioritized report with action plan,
lock strategic decisions, and define implementation waves.

#### 9.1 — Data Consolidation

Gather all intermediate reports:
- INTAKE.md, TOP-25.md, DISCOVERY.md, SEO-PLAN-DRAFT.md
- Keyword research results
- TECHNICAL-AUDIT.md, CONTENT-ANALYSE.md, GEO-ANALYSE.md
- STRUCTURED-DATA.md, LINK-STRUCTUUR.md, COMPETITIVE-INTELLIGENCE.md

#### 9.2 — Priority Matrix

Score all findings on:
- **Impact** (high/medium/low)
- **Effort** (high/medium/low)
- **Urgency** (critical/important/nice-to-have)

Group into implementation priorities:

| Priority | What | Typical |
|----------|------|---------|
| **P1 — Fix now** | High impact, low effort | Broken redirects, missing canonicals, blocked AI-crawlers |
| **P2 — Quick wins** | High impact, medium effort | Striking distance fixes, meta optimization, schema additions |
| **P3 — Strategic** | High impact, high effort | Content rewrites, topical map execution, link restructuring |
| **P4 — Maintenance** | Medium/low impact | Image optimization, readability improvements, blog-schema |

#### 9.3 — Decision Locking

Present findings to user. Lock decisions with IDs (D-01, D-02, etc.):
- Scope: which issues to address now vs later
- Priority order within scope
- Budget/timeline constraints
- Content language and target market
- Tools/APIs available

```markdown
## Locked Decisions

- **D-01**: Focus on Dutch market only (no hreflang needed)
- **D-02**: Prioritize GEO over traditional SEO (AI traffic growing 527%)
- **D-03**: Budget: 20 hours total, spread across 4 waves
- **D-04**: DataForSEO available for keyword research
- **D-05**: Blog content rewrites before new content creation
- **D-06**: No programmatic pages (site too small)
```

**Important:** Once decisions are locked, they persist across sessions. The
orchestrator references them before every implementation action to prevent
drift from agreed-upon priorities.

#### 9.4 — Implementation Waves

Generate concrete implementation waves based on locked decisions:

| Wave | Priority | Exact skills to invoke |
|------|----------|----------------------|
| 1 | Critical | `/42:technical` fixes, `/42:crawlers` unblocking, `/42:structured-data` generation, broken canonical/indexing fixes |
| 2 | High | `/42:content` rewrites, `/42:llmstxt` generation, `/42:genai-optimizer` passage rewrites, `/42:meta-optimizer` bulk title/meta, `/42:sitemap` generation |
| 3 | Medium | `/42:images` optimization, `/42:internal-links` improvements, `/42:programmatic-seo` pages, `/42:title-optimizer` headlines, `/42:product-titles` (e-commerce), `/42:blog` schema generation |
| 4 | Low | `/42:blog` validation + GEO optimization, `/42:hreflang` implementation, `/42:content-repurposer` hergebruik, advanced GEO tweaks |

**Note:** Wave contents are determined by the locked decisions, not hardcoded.
The table above shows typical assignments. Decisions may move tasks between waves.

#### 9.5 — Final Report

Generate structured end report:

```markdown
# SEO & GEO Analyse — [Domeinnaam]

## Management Summary
- 3 biggest opportunities
- 3 biggest risks
- Overall SEO score: X/100
- Overall GEO score: X/100

## Scores per Category
| Category | Score | Status |

## Top-5 Page Deep-Dives
[Per page: scorecard + findings + recommendations]

## Priority Action Plan
### P1 — Fix now (week 1-2)
### P2 — Quick wins (week 2-4)
### P3 — Strategic (month 2-3)
### P4 — Maintenance (ongoing)

## Keyword Landscape
## Technical
## Content & GEO
## Links & Structure
## Competitive Position
## Appendices
```

**Delegates to:** `/42:geo-report` (extended), `/42:seo-plan` for final strategy

**Output:** `reports/EINDRAPPORT.md`, `reports/STRATEGY.md`

---

## State Machine — `/seo-project next` Routing

```
Read 42-reports/<domain>/STATE.md
  |
  +-- No 42-reports/ exists
  |   -> "No project found. Run: /seo-project intake or /seo-project start <url>"
  |
  +-- intake: pending
  |   -> Run Fase 0 (intake questions + homepage crawl)
  |
  +-- intake: completed, init: pending
  |   -> Run Fase 0 continued (pre-flight + directory setup)
  |
  +-- init: completed, crawl: pending
  |   -> Run Fase 1 (Screaming Frog crawl + Top-25)
  |
  +-- crawl: completed, top_5_selected: empty
  |   -> Present Top-25, ask user to select Top-5
  |
  +-- crawl: completed OR skipped, discover: pending
  |   -> Run Fase 2 (baseline audit + SEO plan)
  |
  +-- discover: completed, keywords: pending
  |   -> Run Fase 3 (keyword research & mapping)
  |
  +-- keywords: completed, technical: pending
  |   -> Run Fase 4 (technical audit)
  |
  +-- technical: completed, content: pending
  |   -> Run Fase 5 (content analysis — content-decay FIRST)
  |
  +-- content: completed, entities: pending
  |   -> Run Fase 6 (entity & structured data)
  |
  +-- entities: completed, links: pending
  |   -> Run Fase 7 (internal links & structure)
  |
  +-- links: completed, competitive: pending
  |   -> Run Fase 8 (competitive intelligence)
  |
  +-- competitive: completed, report: pending
  |   -> Run Fase 9 (final report + strategy + decision locking)
  |
  +-- report: completed, implement: pending
  |   -> Show strategy summary, begin wave 1
  |
  +-- implement: in_progress, wave N < total
  |   -> Continue current wave or start next wave
  |
  +-- implement: all waves completed
  |   -> Run verification (re-audit and compare)
  |
  +-- verify: completed, monitor: pending
  |   -> Show verification results, set up monitoring
  |
  +-- monitor: active
  |   -> Check if re-audit is due
  |   -> If due: run re-audit cycle
  |   -> If not: show "Next check: <date>. Score trend: ..."
```

### Multi-Site Detection

If `42-reports/` contains multiple domain directories and no specific domain
is provided, show a project selector:

```
Active SEO Projects:
  1. example.com — Fase 4 (Technische Audit), Score: SEO 42/100, GEO 35/100
  2. shop.nl — Fase 5 (Content), 23 issues found
  3. agency.io — Monitor, next check: Apr 15

Which project? (number or domain)
```

---

## State File Format

State files use YAML-in-markdown (same as project artifacts in this ecosystem).
See `templates/STATE.md` for the full template.

Key fields in STATE.md:

```yaml
site: https://example.com
domain: example-com
business_type: saas          # saas | ecommerce | local | publisher | b2b | agency
language: nl
created: 2026-04-12
last_updated: 2026-04-12
capability_tier: 2           # 1 = Manual, 2 = Basic API, 3 = Full Automation

current_phase: crawl
phase_status: in_progress

# Top page selections from Phase 1
top_25_pages: []             # [{url, clicks, impressions, position, inlinks, score, reason}]
top_5_selected: []           # [url, url, url, url, url]

phases:
  intake:
    status: pending          # pending | in_progress | completed | skipped
  init:
    status: pending
  crawl:
    status: pending
    export_path: null
  discover:
    status: pending
    seo_score: null
    geo_score: null
  keywords:
    status: pending
  technical:
    status: pending
  content:
    status: pending
    content_decay_run: false  # Must run before other content skills
  entities:
    status: pending
  links:
    status: pending
  competitive:
    status: pending
  report:
    status: pending
    decisions_locked: 0
  implement:
    status: pending
    current_wave: 0
    total_waves: 4
    tasks_completed: 0
    tasks_total: 0
  verify:
    status: pending
    seo_delta: null
    geo_delta: null
  monitor:
    status: pending
    next_check: null
    checks_completed: 0
```

---

## `/seo-project start <url>` — Quick Start

**`/seo-project start <url>`** is a shortcut that runs Fase 0 + Fase 1 + Fase 2 in sequence:
1. Run intake with the provided URL (ask remaining questions interactively)
2. Run pre-flight and directory setup
3. Proceed to Fase 1 (crawl + Top-25 + Top-5 selection)
4. Then Fase 2 (discover + SEO plan)

**`/seo-project intake`** runs only the intake, without starting any analysis.
Use this when you want to configure everything first and start later.

---

## `/seo-project status` — Progress Dashboard

Read STATE.md and display:

```
SEO Project: example.com
Type: SaaS | Tier: 3 (Full Automation) | Language: NL
Created: 2026-04-12 | Last updated: 2026-04-12

Phase Progress:
  0. INTAKE & INIT  [========] Completed, 9 questions answered
  1. CRAWL          [========] 1.234 pages crawled, Top-5 selected
  2. DISCOVER       [========] Score: SEO 42/100, GEO 35/100
  3. KEYWORDS       [========] 340 keywords mapped, 12 gaps
  4. TECHNICAL      [====    ] 6/8 checks done
  5. CONTENT        [        ] pending
  6. ENTITIES       [        ] pending
  7. LINKS          [        ] pending
  8. COMPETITIVE    [        ] pending
  9. REPORT         [        ] pending

Current: Fase 4 (TECHNICAL) — step 4.7 Images
Next action: /seo-project next or /seo-project technical
```

---

## Shared Resource References

Skills should reference these shared resource files for consistent evaluation criteria:

| Resource | Path | Used by |
|----------|------|---------|
| CWV Thresholds | `${CLAUDE_PLUGIN_ROOT}/skills/references/cwv-thresholds.md` | Technical audit, Chrome DevTools, page health |
| E-E-A-T Framework | `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md` | Content analysis, QRG scoring, discovery |
| Schema Types | `${CLAUDE_PLUGIN_ROOT}/skills/references/schema-types.md` | Structured data audit, blog schema |
| Quality Gates | `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md` | Content thresholds, readability, page health |
| Web Quality | `${CLAUDE_PLUGIN_ROOT}/skills/references/web-quality/` | Accessibility, performance, CWV deep-dive |

These files provide the single source of truth for scoring thresholds and
evaluation criteria. Individual skills should not hardcode these values but
reference the shared resources instead.

---

## Integration with Existing Skills

This skill sits ABOVE individual 42-* skills and orchestrates them:

```
42-seo-project (project lifecycle orchestrator)
  |
  +-- 42:audit (unified SEO+GEO audit)
  |   +-- 42:technical, 42:content, 42:structured-data, ...
  |   +-- 42:citability, 42:crawlers, 42:brand-intelligence, ...
  |
  +-- 42:blog (unified blog skill: seo-check + geo + schema)
  |
  +-- chrome-devtools (CWV, Lighthouse, accessibility)
  |   +-- debug-optimize-lcp, a11y-debugging, lighthouse_audit
  |
  +-- firecrawl_scrape (homepage crawl, spot-checks)
  |
  +-- 42-* (all specialist skills, called per phase)
```

**All skills remain independently invocable.** This orchestrator adds
project-level state and sequencing on top, but never locks skills behind phases.
Users can always run any skill directly without a project context.

### Skill Routing — Exact Invocations per Phase

| Phase | Skills (exact invocation) |
|-------|--------------------------|
| Fase 0 | `firecrawl_scrape`, `python3 scripts/preflight.py` |
| Fase 1 | `/42:screaming-frog crawl`, `/42:screaming-frog export` |
| Fase 2 | `/42:audit --full <url>`, `/42:seo-plan` |
| Fase 3 | `/42:keyword-discovery`, `/42:paa-scraper`, `/42:keyword-mapper`, `/42:serp-cluster`, `/42:striking-distance`, `/42:topical-map` |
| Fase 4 | `/42:technical`, `chrome-devtools: debug-optimize-lcp`, `chrome-devtools: a11y-debugging`, `chrome-devtools: lighthouse_audit`, `/42:crawlers`, `/42:llmstxt`, `/42:sitemap`, `/42:hreflang`, `/42:images`, `/42:migration` |
| Fase 5 | `/42:content-decay` (FIRST), `/42:near-duplicates`, `/42:page-analysis`, `/42:content`, `/42:citability`, `/42:passage-analyzer`, `/42:entity-extractor`, `/42:structured-data`, `/42:readability`, `/42:qrg`, `/42:page-health`, `/42:ai-visibility`, `/42:platform-optimizer`, `/42:brand-intelligence`, `/42:blog` |
| Fase 6 | `/42:entity-extractor`, `/42:structured-data`, `/42:blog` (schema component) |
| Fase 7 | `/42:internal-links`, `/42:link-graph`, `/42:ecom-taxonomy`, `/42:cannibalization` |
| Fase 8 | `/42:brand-intelligence`, `/42:share-of-voice`, `/42:competitor-pages` |
| Fase 9 | `/42:geo-report`, `/42:seo-plan`, `/42:audience-angles` (optional) |

### Always-Available Skills (not phase-bound)

These skills are useful at any point and are never auto-triggered by the
orchestrator. Run them whenever you need them:

| Skill | Purpose |
|-------|---------|
| `/42:screaming-frog` | Manual crawl, export, or analysis |
| `/42:entity-extractor` | Extract entities for Knowledge Graph |
| `/42:migration` | URL migration mapping and redirect planning |
| `/42:near-duplicates` | Detect near-duplicate content |
| `/42:readability` | Bulk readability scoring |
| `/42:page-analysis` | Deep single-page analysis |
| `/42:seo-agi` | Write GEO-optimized pages from scratch |
| `/42:ai-visibility` | Track AI search visibility |
| `/42:sentiment` | Online sentiment analysis |
| `/42:geo-proposal` | Generate client proposal from audit data |
| `/42:geo-prospect` | CRM pipeline management |
| `/42:geo-report` | Client-ready GEO report |
| `/42:genai-optimizer` | GEO passage rewrites (implementation phase) |
| `/42:content-repurposer` | Repurpose content to platforms (implementation phase) |
| `/42:programmatic-seo` | Scalable template pages (implementation phase) |
| `/42:audience-angles` | Content angles via QPAFFCGMIM framework |
| `/seo page <url>` | Quick single-page SEO check |
| `/geo quick <url>` | 60-second GEO snapshot |

---

## Session Continuity

All state lives in `42-reports/<domain>/` files. When a conversation resets:

1. `/seo-project next` reads STATE.md to determine position
2. Reads the relevant phase file (DISCOVERY.md, TOP-25.md, TECHNICAL-AUDIT.md, etc.)
3. Resumes from exactly where the previous session left off
4. No context is lost between sessions

---

## Error Handling

- **Skill not available**: If a delegated skill fails to load, log the error
  in STATE.md `blockers` field and suggest the user run it manually
- **Audit timeout**: Large sites may take long. If interrupted, STATE.md
  records partial progress so `/seo-project next` can resume
- **Score regression in verify**: Flag regressions prominently and suggest
  a targeted diagnose→fix mini-cycle for regressed categories only
- **Chrome DevTools unavailable**: If chrome-devtools MCP is not connected,
  skip CWV/Lighthouse/a11y checks, note in report, suggest manual PageSpeed Insights
- **Firecrawl unavailable**: Skip homepage crawl in Fase 0, proceed with
  manual site inspection or WebFetch fallback
- **SF not available (Tier 1/2)**: Many skills degrade gracefully. Mark crawl
  as `skipped`, note reduced capabilities in each affected phase report

---

## Quality Gates (Inherited)

This orchestrator inherits all quality gates from sub-skills:
- Max 500 pages per crawl (seo-audit)
- Max 50 pages per GEO audit (geo-audit)
- Never recommend HowTo schema (deprecated Sept 2023)
- FAQ schema restrictions (Aug 2023)
- All CWV references use INP, never FID
- Respect robots.txt always

Additional quality gates from shared resources:
- Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md` for content thresholds
- Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/cwv-thresholds.md` for CWV pass/fail criteria
- Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/schema-types.md` for schema validity
