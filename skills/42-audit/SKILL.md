---
name: 42-audit
description: >
  Unified SEO & GEO audit orchestrator with dual scoring. Runs parallel subagents
  for technical, content, schema, sitemap, images, AI visibility analysis.
  Modes: --seo (traditional SEO), --geo (AI citability), --full (both).
  Use when user says "audit", "SEO audit", "GEO audit", "site check", "analyze site".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
version: 2.0.0
tags: [audit, seo, geo, orchestrator]
---

# 42-audit -- Unified SEO & GEO Audit Orchestrator

## Modes

| Invocation | What runs | Output scores |
|---|---|---|
| `/42:audit --seo <url>` | SEO subagents only | `seo_score` |
| `/42:audit --geo <url>` | GEO subagents only | `geo_score` |
| `/42:audit --full <url>` | Both (default) | `seo_score` + `geo_score` |

When no flag is provided, `--full` is assumed.

---

## Audit Variants

### Quick Audit (Phase 2 DISCOVER)

- **Purpose**: Establish baseline scores during discovery phase
- **Scope**: ~50 pages (homepage + top navigation + key landing pages + blog sample)
- **When**: Early in the project, before deep analysis
- **Output**: `reports/DISCOVERY.md` with composite scores and top issues

### Deep-Dive Audit (Phase 5)

- **Purpose**: Comprehensive single-page analysis for top-5 selected pages
- **Scope**: 1 page, full analysis stack
- **When**: After top-5 selection by client, during content analysis phase
- **Output**: Per-page report with granular scores and specific fix recommendations

---

## Workflow

### Step 1: Fetch Homepage and Detect Business Type

1. Use WebFetch to retrieve the homepage at the provided URL.
2. Extract the following signals:
   - Page title, meta description, H1 heading
   - Navigation menu items (reveals site structure)
   - Footer content (reveals business info, location, legal pages)
   - Schema.org markup on homepage (Organization, LocalBusiness, etc.)
   - Pricing page link (SaaS indicator)
   - Product listing patterns (E-commerce indicator)
   - Blog/resource section (Publisher indicator)
   - Service pages (Agency indicator)
   - Address/phone/Google Maps embed (Local business indicator)

3. Classify the business type using these patterns:

| Business Type | Detection Signals |
|---|---|
| **SaaS** | Pricing page, "Sign up" / "Free trial" CTAs, app.domain.com subdomain, feature comparison tables, integration pages |
| **Local Business** | Physical address on homepage, Google Maps embed, "Near me" content, LocalBusiness schema, service area pages |
| **E-commerce** | Product listings, shopping cart, product schema, category pages, price displays, "Add to cart" buttons |
| **Publisher** | Blog-heavy navigation, article schema, author pages, date-based archives, RSS feeds, high content volume |
| **Agency/Services** | Case studies, portfolio, "Our Work" section, team page, client logos, service descriptions |
| **Hybrid** | Combination of above signals -- classify by dominant pattern |

### Step 2: Crawl Sitemap and Internal Links

1. Attempt to fetch `/sitemap.xml` and `/sitemap_index.xml`.
2. If sitemap exists, extract up to 50 unique page URLs prioritized by:
   - Homepage (always include)
   - Top-level navigation pages
   - High-value pages (pricing, about, contact, key service/product pages)
   - Blog posts (sample 5-10 most recent)
   - Category/landing pages
3. If no sitemap exists, crawl internal links from the homepage:
   - Extract all `<a href>` links pointing to the same domain
   - Follow up to 2 levels deep
   - Prioritize pages linked from main navigation
4. Respect `robots.txt` directives -- do not fetch disallowed paths.
5. Enforce a maximum of 50 pages for quick audit, 1 page for deep-dive.

**Optional SF input:** If Screaming Frog export CSVs exist at
`42-reports/<domain>/exports/latest/`, use them instead of re-crawling.
This provides richer data (embeddings, GSC, link graph) at no additional crawl cost.

### Step 3: Collect Page-Level Data

For each page in the crawl set, record:
- URL, title, meta description, canonical URL
- H1-H6 heading structure
- Word count of main content
- Schema.org types present
- Internal/external link counts
- Images with/without alt text
- Open Graph and Twitter Card meta tags
- Response status code
- Whether the page has structured data

### Step 4: Delegate to Subagents

Based on the active mode, delegate to the appropriate subagent set. Run subagents in parallel where possible.

#### SEO Subagents (run when `--seo` or `--full`)

| Subagent | Responsibility |
|---|---|
| `42-technical` | robots.txt, sitemaps, canonicals, security headers, crawlability, indexability |
| `42-content --seo` | E-E-A-T, readability, thin content, duplicate content, content quality |
| `42-structured-data --seo` | Schema detection, validation, generation recommendations |
| `42-sitemap` | Structure analysis, quality gates, missing pages |
| `42-images` | Alt text, image format, sizing, lazy loading, responsive images |
| `chrome-devtools: debug-optimize-lcp` | Performance (CWV): LCP, INP, CLS measurement via Chrome DevTools MCP |

#### GEO Subagents (run when `--geo` or `--full`)

| Subagent | Responsibility |
|---|---|
| `42-citability` | AI citation readiness, passage quotability, answer block quality |
| `42-brand-intelligence` | Brand presence across YouTube, Reddit, Wikipedia, LinkedIn; mention volume and sentiment |
| `42-crawlers` | AI crawler access in robots.txt (GPTBot, ClaudeBot, PerplexityBot, etc.) |
| `42-llmstxt` | llms.txt presence, quality, and completeness |
| `42-content --geo` | Content E-E-A-T from AI perspective, author credentials, source citations |
| `42-structured-data --geo` | GEO-critical schema types (FAQ, HowTo, Organization, Product, Article) |
| `42-platform-optimizer` | Per-platform optimization (ChatGPT, Claude, Perplexity, Gemini) |

### Step 5: Score Aggregation

Calculate composite scores based on weighted category averages.

---

## SEO Scoring Weights (total: 100%)

| Category | Weight | What It Measures |
|---|---|---|
| Technical SEO | 22% | Crawlability, indexability, security, redirects |
| Content Quality | 23% | E-E-A-T, readability, thin content, duplicate content |
| On-Page SEO | 20% | Titles, meta descriptions, headings, internal linking |
| Schema / Structured Data | 10% | Schema.org markup quality and completeness |
| Performance (CWV) | 10% | LCP, INP, CLS via Chrome DevTools MCP |
| AI Search Readiness | 10% | Citability, structural improvements, authority signals |
| Images | 5% | Alt text, format, sizing, lazy loading |

**Formula:**
```
SEO_Score = (Technical * 0.22) + (Content * 0.23) + (OnPage * 0.20) + (Schema * 0.10) + (CWV * 0.10) + (AISearch * 0.10) + (Images * 0.05)
```

## GEO Scoring Weights (total: 100%)

| Category | Weight | What It Measures |
|---|---|---|
| AI Citability & Visibility | 25% | How quotable/extractable content is for AI systems |
| Brand Authority Signals | 20% | Third-party mentions, entity recognition signals |
| Content Quality & E-E-A-T | 20% | Experience, Expertise, Authoritativeness, Trustworthiness |
| Technical Foundations | 15% | AI crawler access, llms.txt, rendering, speed |
| Structured Data | 10% | Schema.org markup quality and completeness |
| Platform Optimization | 10% | Presence on platforms AI models train on and cite |

**Formula:**
```
GEO_Score = (Citability * 0.25) + (Brand * 0.20) + (EEAT * 0.20) + (Technical * 0.15) + (Schema * 0.10) + (Platform * 0.10)
```

---

## Score Interpretation

| Score Range | Rating | SEO Interpretation | GEO Interpretation |
|---|---|---|---|
| 90-100 | Excellent | Top-tier SEO health; strong rankings expected | Highly likely to be cited by AI systems |
| 75-89 | Good | Strong SEO foundation with room for improvement | Strong GEO foundation with optimization opportunities |
| 60-74 | Fair | Moderate SEO presence; significant gaps exist | Moderate GEO presence; AI systems may underrepresent |
| 40-59 | Poor | Weak SEO signals; rankings likely suffering | Weak GEO signals; AI systems may struggle to cite |
| 0-39 | Critical | Severe SEO issues; indexing/ranking blocked | Minimal GEO optimization; largely invisible to AI |

---

## Issue Severity Classification

### Critical (Fix Immediately)
- All AI crawlers blocked in robots.txt
- No indexable content (JavaScript-rendered only with no SSR)
- Domain-level noindex directive
- Site returns 5xx errors on key pages
- Complete absence of any structured data
- Brand not recognized as an entity by any AI system
- Broken canonical chains blocking indexation

### High (Fix Within 1 Week)
- Key AI crawlers (GPTBot, ClaudeBot, PerplexityBot) blocked
- No llms.txt file present
- Zero question-answering content blocks on key pages
- Missing Organization or LocalBusiness schema
- No author attribution on content pages
- All content behind login/paywall with no preview
- Missing or duplicate title tags on high-traffic pages

### Medium (Fix Within 1 Month)
- Partial AI crawler blocking (some allowed, some blocked)
- llms.txt exists but is incomplete or malformed
- Content blocks average under 50 citability score
- Missing FAQ schema on pages with FAQ content
- Thin author bios without credentials
- No Wikipedia or Reddit brand presence
- Suboptimal internal linking structure

### Low (Optimize When Possible)
- Minor schema validation errors
- Some images missing alt text
- Content freshness issues on non-critical pages
- Missing Open Graph tags
- Suboptimal heading hierarchy on some pages
- LinkedIn company page exists but is incomplete

---

## Crawl Configuration

```
Max pages (quick audit): 50
Max pages (deep-dive):   1
Respect robots.txt:      Yes
Follow redirects:        Yes (max 3 hops)
Timeout per page:        30 seconds
Concurrent requests:     5
Delay between requests:  1 second
Content types:           HTML only (skip PDFs, images, binaries)
Deduplication:           Canonicalize URLs before crawling (HTTP/HTTPS, www/non-www, trailing slashes)
```

---

## Business-Type-Specific Audit Adjustments

### SaaS Sites
- Extra weight on: Feature comparison tables (high citability), integration pages, documentation quality
- Check for: API documentation structure, changelog pages, knowledge base organization
- Key schema: SoftwareApplication, FAQPage, HowTo

### Local Businesses
- Extra weight on: NAP consistency, Google Business Profile signals, local schema
- Check for: Service area pages, location-specific content, review markup
- Key schema: LocalBusiness, GeoCoordinates, OpeningHoursSpecification

### E-commerce Sites
- Extra weight on: Product descriptions (citability), comparison content, buying guides
- Check for: Product schema completeness, review aggregation, FAQ sections on product pages
- Key schema: Product, AggregateRating, Offer, BreadcrumbList

### Publishers
- Extra weight on: Article quality, author credentials, source citation practices
- Check for: Article schema, author pages, publication date freshness, original research
- Key schema: Article, NewsArticle, Person (author), ClaimReview

### Agency/Services
- Extra weight on: Case studies (citability), expertise demonstration, thought leadership
- Check for: Portfolio schema, team credentials, industry-specific expertise signals
- Key schema: Organization, Service, Person (team), Review

---

## Shared Resource References

- `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md` -- E-E-A-T evaluation criteria and scoring rubric
- `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md` -- Content quality thresholds and pass/fail criteria
- `${CLAUDE_PLUGIN_ROOT}/skills/references/cwv-thresholds.md` -- Core Web Vitals scoring detail and target values

---

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess site content. Suggest the user verify the URL and try again. |
| robots.txt blocks crawling | Report which paths are blocked. Analyze only accessible pages and note the limitation in the report. |
| Rate limiting (429 responses) | Back off and reduce concurrent requests. Report partial results with a note on which sections could not be completed. |
| Timeout on large sites | Cap the crawl at the page limit. Report findings for pages crawled and estimate total site scope. |
| Subagent failure | Log the failure, continue with remaining subagents. Mark the failed category as "incomplete" in the report. |
| No structured data found | Score Schema category as 0, flag as Critical severity, continue with other categories. |

---

## Output Format

The audit produces `reports/DISCOVERY.md` that `42-seo-project` can read downstream.

```markdown
# Audit Report: [Site Name]

**Audit Date:** [Date]
**URL:** [URL]
**Business Type:** [Detected Type]
**Pages Analyzed:** [Count]
**Mode:** [--seo | --geo | --full]

---

## Executive Summary

**SEO Score: [X]/100 ([Rating])**    ← when --seo or --full
**GEO Score: [X]/100 ([Rating])**    ← when --geo or --full

[2-3 sentence summary of the site's health, biggest strengths, and most critical gaps.]

---

## SEO Score Breakdown

| Category | Score | Weight | Weighted |
|---|---|---|---|
| Technical SEO | [X]/100 | 22% | [X] |
| Content Quality | [X]/100 | 23% | [X] |
| On-Page SEO | [X]/100 | 20% | [X] |
| Schema / Structured Data | [X]/100 | 10% | [X] |
| Performance (CWV) | [X]/100 | 10% | [X] |
| AI Search Readiness | [X]/100 | 10% | [X] |
| Images | [X]/100 | 5% | [X] |
| **SEO Score** | | | **[X]/100** |

## GEO Score Breakdown

| Category | Score | Weight | Weighted |
|---|---|---|---|
| AI Citability & Visibility | [X]/100 | 25% | [X] |
| Brand Authority Signals | [X]/100 | 20% | [X] |
| Content Quality & E-E-A-T | [X]/100 | 20% | [X] |
| Technical Foundations | [X]/100 | 15% | [X] |
| Structured Data | [X]/100 | 10% | [X] |
| Platform Optimization | [X]/100 | 10% | [X] |
| **GEO Score** | | | **[X]/100** |

---

## Score Interpretation

| Score Range | Rating | Meaning |
|---|---|---|
| 90-100 | Excellent | Top-tier optimization |
| 75-89 | Good | Strong foundation, room to improve |
| 60-74 | Fair | Significant optimization opportunities |
| 40-59 | Poor | Weak signals, performance likely impacted |
| 0-39 | Critical | Severe issues, immediate action required |

---

## Top Issues

| # | Severity | Category | Description | Recommended Fix |
|---|---|---|---|---|
| 1 | Critical | [cat] | [description] | [fix] |
| 2 | High | [cat] | [description] | [fix] |
| ... | | | | |

---

## Critical Issues (Fix Immediately)

[List each critical issue with specific page URLs and recommended fix]

## High Priority Issues (Fix Within 1 Week)

[List each high-priority issue with details]

## Medium Priority Issues (Fix Within 1 Month)

[List each medium-priority issue]

## Low Priority Issues (Optimize When Possible)

[List each low-priority issue]

---

## Quick Wins (Implement This Week)

1. [Specific, actionable quick win with expected impact]
2. [Another quick win]
3. [Another quick win]
4. [Another quick win]
5. [Another quick win]

---

## Appendix: Pages Analyzed

| URL | Title | SEO Issues | GEO Issues |
|---|---|---|---|
| [url] | [title] | [count] | [count] |
```

---

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, spawn the `seo-dataforseo` agent alongside existing subagents to enrich the audit with live data: real SERP positions, backlink profiles with spam scores, on-page analysis (Lighthouse), business listings, and AI visibility checks (ChatGPT scraper, LLM mentions).

## Google API Integration (Optional)

If Google API credentials are configured (`python scripts/google_auth.py --check`), spawn the `seo-google` agent to enrich the audit with real Google field data: CrUX Core Web Vitals (replaces lab-only estimates), GSC URL indexation status, search performance (clicks, impressions, CTR), and GA4 organic traffic trends. The Performance (CWV) category score benefits most from field data.

## Chrome DevTools MCP for CWV

For Performance (CWV) scoring, use Chrome DevTools MCP via `chrome-devtools: debug-optimize-lcp`:
- LCP measurement and optimization guidance
- INP detection and event handler analysis
- CLS identification and layout shift debugging
- Lighthouse audit for comprehensive performance scoring

This replaces lab-only estimates with real browser measurements when available.
