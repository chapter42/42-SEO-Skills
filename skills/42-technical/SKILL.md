---
name: 42-technical
description: >
  Unified technical SEO & GEO audit across crawlability, indexability, security,
  URL structure, mobile, Core Web Vitals (INP/LCP/CLS), server-side rendering,
  structured data, JavaScript rendering, and IndexNow. Dual scoring: traditional
  SEO score + GEO score (AI crawler accessibility weighted higher for GEO).
  Use when user says "technical audit", "technical SEO", "crawlability", "CWV",
  "Core Web Vitals", "page speed", "indexability", "mobile SEO".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
version: 2.0.0
tags: [technical, seo, geo, audit, cwv, crawlability]
---

# Unified Technical SEO & GEO Audit

## Purpose

Technical SEO forms the foundation of both traditional search visibility and AI search citation. A technically broken site cannot be crawled, indexed, or cited by any platform. This skill audits **10 categories** of technical health with **dual scoring**:

- **SEO Score (0-100):** Traditional weighting — CWV and mobile weighted higher (Google ranking signals)
- **GEO Score (0-100):** SSR weighted 2x, AI crawler access weighted 2x (AI crawlers do NOT execute JavaScript)

---

## Input Options

### Option 1: Screaming Frog CSV Exports (preferred — richer data)

Import one or more Screaming Frog CSV exports for bulk analysis:
- `internal_all.csv` — all internal URLs with status codes, redirect chains, canonicals
- `response_codes.csv` — HTTP status code breakdown
- `page_titles.csv` — title tags and lengths
- `meta_description.csv` — meta descriptions and lengths
- `h1.csv` / `h2.csv` — heading structure
- `structured_data.csv` — detected schema markup
- `images.csv` — image URLs, alt text, dimensions
- `directives.csv` — robots directives per URL
- `canonical_tags.csv` — canonical tag analysis
- `hreflang.csv` — hreflang tag validation

**Usage:** Place CSV files in working directory or provide paths. The skill will auto-detect Screaming Frog export format and parse accordingly.

### Option 2: Live Crawl via WebFetch (fallback)

Provide a homepage URL + 2-3 key inner pages. The skill will:
1. Fetch each page via WebFetch to get raw HTML and HTTP headers
2. Fetch `robots.txt` and `sitemap.xml`
3. Analyze responses against all 10 categories

### Option 3: Single URL Deep-Dive

Provide one URL for a thorough per-page technical analysis. Best for diagnosing specific page issues (CWV, SSR, structured data rendering).

---

## Procedure

1. Determine input type (Screaming Frog CSV, live crawl, or single URL)
2. Collect raw HTML and HTTP headers for target pages
3. Fetch and parse `robots.txt` and XML sitemap
4. Run through each of the 10 audit categories below
5. Score each category for BOTH SEO and GEO using the dual scoring rubric
6. Generate output report with dual score tables

---

## Category 1: Crawlability

### What to Check

#### 1.1 robots.txt Validity
- Fetch `https://[domain]/robots.txt`
- Check syntactic validity: proper `User-agent`, `Allow`, `Disallow` directives
- Check for common errors: missing User-agent, wildcards blocking important paths, `Disallow: /` blocking entire site
- Verify XML sitemap is referenced: `Sitemap: https://[domain]/sitemap.xml`

#### 1.2 AI Crawler Management (CRITICAL for GEO)

Check robots.txt for directives targeting these AI crawlers:

**Tier 1 — Critical (block = major GEO impact)**

| Crawler | User-Agent | Platform | Purpose |
|---------|-----------|----------|---------|
| GPTBot | `GPTBot` | ChatGPT / OpenAI | Model training + search |
| ChatGPT-User | `ChatGPT-User` | ChatGPT | Real-time browsing |
| Googlebot | `Googlebot` | Google Search + AI Overviews | Search + AIO |
| Bingbot | `bingbot` | Bing + Copilot + ChatGPT (via Bing) | Search + AI |

**Tier 2 — Important (block = reduced GEO visibility)**

| Crawler | User-Agent | Platform | Purpose |
|---------|-----------|----------|---------|
| PerplexityBot | `PerplexityBot` | Perplexity AI | Search index + training |
| Google-Extended | `Google-Extended` | Gemini training | AI training (NOT search) |
| ClaudeBot | `ClaudeBot` | Anthropic Claude | Model training |
| Applebot-Extended | `Applebot-Extended` | Apple Intelligence | AI features |

**Tier 3 — Training-only (block = minimal search impact)**

| Crawler | User-Agent | Platform | Purpose |
|---------|-----------|----------|---------|
| Bytespider | `Bytespider` | ByteDance / TikTok AI | Model training |
| CCBot | `CCBot` | Common Crawl | Open dataset (used by many AI) |
| FacebookBot | `FacebookExternalHit` | Meta AI | Social + AI training |
| Amazonbot | `Amazonbot` | Amazon / Alexa AI | AI features |

**Key distinctions:**
- Blocking `Google-Extended` prevents Gemini training but does NOT affect Google Search indexing or AI Overviews (those use `Googlebot`). However, blocking may reduce presence in AI Overviews.
- Blocking `GPTBot` prevents OpenAI training but does NOT prevent ChatGPT from citing your content via browsing (`ChatGPT-User`)
- ~3-5% of websites now use AI-specific robots.txt rules

**Example — selective AI crawler blocking:**
```
# Allow search indexing, block AI training crawlers
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Bytespider
Disallow: /

# Allow all other crawlers (including Googlebot for search)
User-agent: *
Allow: /
```

#### 1.3 XML Sitemaps
- Fetch sitemap (check robots.txt for location, or try `/sitemap.xml`, `/sitemap_index.xml`)
- Validate XML syntax
- Check for `<lastmod>` dates (should be present and accurate)
- Count URLs — compare to expected number of indexable pages
- Check for sitemap index if large site (50,000+ URLs per sitemap max)
- Verify all sitemap URLs return 200 status codes (sample check)

#### 1.4 Crawl Depth
- Homepage = depth 0. All important pages reachable within **3 clicks** (depth 3)
- Pages at depth 4+ receive significantly less crawl budget and are less likely to be cited by AI
- Check internal linking: are key content pages linked from homepage or main navigation?

#### 1.5 Orphan Pages
- Identify pages in XML sitemap that have zero internal links pointing to them
- Check for pages receiving organic traffic but not linked from site navigation
- Orphan pages are invisible to AI crawlers that rely on link discovery

#### 1.6 Crawl Budget (large sites >10k pages)
- Assess whether thin, duplicate, or parameter pages waste crawl budget
- Check for unnecessary URLs in sitemap (paginated, filtered, sorted variations)
- Flag if indexed pages significantly exceed valuable content pages

#### 1.7 Noindex Management
- Check for `<meta name="robots" content="noindex">` on pages that SHOULD be indexed
- Check for `X-Robots-Tag: noindex` HTTP headers
- Common mistakes: noindex on paginated pages, category pages, or key landing pages

### How to Check
- `WebFetch` or `curl` to fetch robots.txt and sitemap
- Screaming Frog `directives.csv` for bulk noindex detection
- Screaming Frog `internal_all.csv` for crawl depth analysis

### Pass/Warn/Fail Thresholds
| Check | Pass | Warn | Fail |
|-------|------|------|------|
| robots.txt | Valid, no critical blocks | Minor syntax issues | Missing or blocking site |
| AI crawlers | All Tier 1+2 allowed | Some Tier 2 blocked | Tier 1 crawlers blocked |
| XML sitemap | Present, valid, referenced | Present but issues | Missing entirely |
| Crawl depth | All key pages within 3 clicks | Some pages at depth 4 | Key pages at depth 5+ |
| Noindex | No erroneous noindex | 1-2 accidental noindex | Critical pages noindexed |

### Quick Fixes
- Add missing `Sitemap:` directive to robots.txt
- Remove accidental `Disallow` rules blocking AI crawlers
- Add orphan pages to navigation or internal linking
- Fix noindex directives on pages that should be indexed

### Scoring

**SEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| robots.txt valid and complete | 20 |
| XML sitemap present and valid | 25 |
| Crawl depth within 3 clicks | 20 |
| No orphan pages | 15 |
| No erroneous noindex | 20 |

**GEO sub-score (of 100) — AI crawler access weighted 2x:**

| Check | Points |
|-------|--------|
| robots.txt valid and complete | 10 |
| AI crawlers allowed (Tier 1+2) | **40** |
| XML sitemap present and valid | 15 |
| Crawl depth within 3 clicks | 15 |
| No orphan pages | 10 |
| No erroneous noindex | 10 |

---

## Category 2: Indexability

### What to Check

#### 2.1 Canonical Tags
- Every indexable page must have `<link rel="canonical" href="...">`
- Canonical must self-reference for the authoritative version
- Check for conflicting canonicals (HTML vs HTTP header)
- Check for canonical chains (A->B->C should be A->C directly)

**JavaScript caveat (Dec 2025):** If a canonical tag in raw HTML differs from one injected by JavaScript, Google may use EITHER one. Ensure canonical tags are identical between server-rendered HTML and JS-rendered output.

#### 2.2 Duplicate Content
- www vs non-www: both resolve, one redirects
- HTTP vs HTTPS: HTTP must redirect to HTTPS
- Trailing slash consistency: pick one pattern, redirect the other
- Parameter-based duplicates (`?sort=price` creating duplicate pages)

#### 2.3 Pagination
- Check for `rel="next"` / `rel="prev"` (Google ignores since 2019; Bing still uses)
- Preferred: `rel="canonical"` on paginated pages pointing to view-all or first page
- Ensure paginated pages not noindexed if they contain unique content

#### 2.4 Hreflang (international sites)
- Check for `<link rel="alternate" hreflang="xx">` tags
- Validate reciprocal hreflang (A->B means B must->A)
- Validate x-default fallback exists
- Check language/region code validity (ISO 639-1 / ISO 3166-1)

#### 2.5 Index Bloat
- Estimate indexed pages (sitemap count, `site:domain.com`)
- Compare indexed vs actual valuable content pages
- Flag if indexed pages significantly exceed content pages

### How to Check
- Screaming Frog `canonical_tags.csv` for bulk canonical analysis
- Screaming Frog `hreflang.csv` for hreflang validation
- `WebFetch` to inspect HTML `<head>` for canonical/meta tags
- HTTP response headers for `Link: rel="canonical"` header

### Pass/Warn/Fail Thresholds
| Check | Pass | Warn | Fail |
|-------|------|------|------|
| Canonicals | Self-referencing on all pages | Minor conflicts | Missing or pointing to wrong URLs |
| Duplicates | No duplicate variants indexable | Some parameter URLs indexable | www/non-www or HTTP/HTTPS both indexable |
| Pagination | Properly handled | Missing rel=next/prev (Bing) | Paginated pages noindexed with unique content |
| Hreflang | Reciprocal, valid codes | Minor code issues | One-way or missing x-default |
| Index bloat | Indexed ~= valuable pages | 20%+ bloat | 50%+ bloat |

### Quick Fixes
- Add self-referencing canonical to all indexable pages
- Set up 301 redirects for www/non-www and HTTP/HTTPS variants
- Configure URL parameter handling in Google Search Console
- Add x-default hreflang fallback

### Scoring

**SEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| Canonical tags correct | 25 |
| No duplicate content issues | 25 |
| Pagination handled correctly | 15 |
| Hreflang correct (if applicable) | 20 |
| No index bloat | 15 |

**GEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| Canonical tags correct | 25 |
| No duplicate content issues | 25 |
| Pagination handled correctly | 15 |
| Hreflang correct (if applicable) | 20 |
| No index bloat | 15 |

---

## Category 3: Security

### What to Check

#### 3.1 HTTPS Enforcement
- Site loads over HTTPS
- HTTP redirects to HTTPS (301)
- No mixed content warnings (HTTP resources on HTTPS pages)
- SSL/TLS certificate valid and not expired

#### 3.2 Security Headers

| Header | Required Value | Purpose |
|--------|---------------|---------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Forces HTTPS |
| `Content-Security-Policy` | Appropriate policy | Prevents XSS |
| `X-Content-Type-Options` | `nosniff` | Prevents MIME sniffing |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Prevents clickjacking |
| `Referrer-Policy` | `strict-origin-when-cross-origin` or stricter | Controls referrer |
| `Permissions-Policy` | Appropriate restrictions | Controls browser features |

#### 3.3 HSTS Preload
- For high-security sites: check HSTS preload list inclusion
- Requires: `includeSubDomains` and `preload` directives in HSTS header

### How to Check
- `WebFetch` or `curl -I` to inspect HTTP response headers
- Check for mixed content by scanning HTML for `http://` resource URLs
- Verify SSL certificate validity and expiry date

### Pass/Warn/Fail Thresholds
| Check | Pass | Warn | Fail |
|-------|------|------|------|
| HTTPS | Enforced with valid cert | Valid but no redirect from HTTP | No HTTPS or expired cert |
| HSTS | Present with long max-age | Present with short max-age | Missing |
| Mixed content | None | Minor (images) | Critical (scripts, iframes) |
| Security headers | 5+ headers present | 3-4 headers | Fewer than 3 headers |

### Quick Fixes
- Enable HTTPS redirect in server config or CDN
- Add HSTS header: `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- Add `X-Content-Type-Options: nosniff` to server response
- Replace all `http://` resource URLs with `https://` or protocol-relative

### Scoring

**SEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| HTTPS enforced with valid cert | 40 |
| HSTS header present | 20 |
| No mixed content | 15 |
| X-Content-Type-Options | 5 |
| X-Frame-Options | 5 |
| Referrer-Policy | 5 |
| Content-Security-Policy | 10 |

**GEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| HTTPS enforced with valid cert | 40 |
| HSTS header present | 20 |
| No mixed content | 15 |
| X-Content-Type-Options | 5 |
| X-Frame-Options | 5 |
| Referrer-Policy | 5 |
| Content-Security-Policy | 10 |

---

## Category 4: URL Structure

### What to Check

#### 4.1 Clean URLs
- Human-readable: `/blog/seo-guide` not `/blog?id=12345`
- No session IDs in URLs
- Lowercase only (no mixed case)
- Hyphens for word separation (not underscores)
- No special characters or encoded spaces

#### 4.2 Logical Hierarchy
- URL path reflects site architecture: `/category/subcategory/page`
- Flat where appropriate — avoid unnecessarily deep nesting
- Consistent pattern across the site

#### 4.3 Redirect Chains
- No redirect chains (A->B->C)
- Maximum 1 hop recommended (A->C directly)
- No redirect loops
- All redirects 301 (permanent), not 302, unless intentionally temporary

#### 4.4 Parameter Handling
- URL parameters must not create duplicate indexable pages
- Use canonical tags or `robots.txt Disallow` for parameter variations
- Configure parameter handling in Google Search Console and Bing Webmaster Tools

#### 4.5 URL Length
- Flag URLs >100 characters
- Shorter URLs correlate with better click-through rates and easier sharing

#### 4.6 Trailing Slash Consistency
- Pick one pattern (with or without trailing slash)
- Redirect the other pattern to the canonical version
- Inconsistency creates duplicate content signals

### How to Check
- Screaming Frog `internal_all.csv` for URL patterns, redirect chains, status codes
- Screaming Frog `response_codes.csv` for redirect analysis
- `WebFetch` to follow redirect chains manually

### Pass/Warn/Fail Thresholds
| Check | Pass | Warn | Fail |
|-------|------|------|------|
| Clean URLs | All URLs readable, hyphens | Minor issues (underscores) | Session IDs or encoded params |
| Hierarchy | Logical, consistent | Somewhat inconsistent | No discernible pattern |
| Redirects | No chains | 1 chain found | Multiple chains or loops |
| URL length | All <100 chars | Some 100-150 chars | Many >150 chars |
| Trailing slashes | Consistent pattern | Minor inconsistency | No redirect, both versions index |

### Quick Fixes
- Implement 301 redirects to consolidate redirect chains to 1 hop
- Add trailing slash redirect rules to server config
- Replace underscores with hyphens and redirect old URLs
- Set up canonical tags for parameter variations

### Scoring

**SEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| Clean, readable URLs | 25 |
| Logical hierarchy | 20 |
| No redirect chains (max 1 hop) | 25 |
| Parameter handling configured | 15 |
| URL length <100 chars | 15 |

**GEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| Clean, readable URLs | 25 |
| Logical hierarchy | 20 |
| No redirect chains (max 1 hop) | 25 |
| Parameter handling configured | 15 |
| URL length <100 chars | 15 |

---

## Category 5: Mobile Optimization

### Critical Context

As of **July 2024**, Google crawls ALL sites exclusively with mobile Googlebot. There is no desktop crawling. **Mobile-first indexing is 100% complete.** If your site does not work on mobile, it does not work for Google. Period.

### What to Check

#### 5.1 Responsive Design
- Check for `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Content must not require horizontal scrolling on mobile
- No fixed-width layouts wider than viewport

#### 5.2 Tap Targets
- Interactive elements (buttons, links) at least **48x48 CSS pixels**
- Minimum **8px spacing** between tap targets
- Navigation usable on mobile

#### 5.3 Font Sizes
- Base font size at least **16px**
- No text requiring zoom to read
- Sufficient contrast ratio (WCAG AA: 4.5:1 normal text, 3:1 large text)

#### 5.4 Mobile Content Parity
- All desktop-visible content also visible on mobile
- No hidden content behind "read more" toggles that crawlers cannot expand (Google improved at expanding these as of 2025, but AI crawlers cannot)
- Images and media load on mobile

### How to Check
- `WebFetch` with mobile user-agent to inspect mobile rendering
- Check viewport meta tag in raw HTML
- `chrome-devtools: lighthouse_audit` for mobile usability scores
- Screaming Frog with mobile user-agent crawl configuration

### Pass/Warn/Fail Thresholds
| Check | Pass | Warn | Fail |
|-------|------|------|------|
| Viewport tag | Correct `width=device-width` | Present but misconfigured | Missing |
| Responsive | No horizontal scroll | Minor overflow | Fixed-width layout |
| Tap targets | All 48x48+ with 8px spacing | Most adequate | Many too small or overlapping |
| Font sizes | 16px+ base | 14px base | Below 14px or requires zoom |

### Quick Fixes
- Add `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Set `max-width: 100%` on images and containers
- Increase button/link tap target size with padding
- Set base font-size to 16px in CSS root

### Scoring

**SEO sub-score (of 100) — weighted higher for SEO:**

| Check | Points |
|-------|--------|
| Viewport meta tag correct | 30 |
| Responsive layout (no horizontal scroll) | 30 |
| Tap targets appropriately sized | 20 |
| Font sizes legible | 20 |

**GEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| Viewport meta tag correct | 30 |
| Responsive layout (no horizontal scroll) | 30 |
| Tap targets appropriately sized | 20 |
| Font sizes legible | 20 |

---

## Category 6: Core Web Vitals

### Reference

For full thresholds, LCP subparts, and tooling details, see: `${CLAUDE_PLUGIN_ROOT}/skills/references/cwv-thresholds.md`

### 2026 Metrics and Thresholds

Core Web Vitals use the **75th percentile** of real user data (field data). Lab data is useful for debugging but field data determines the ranking signal.

| Metric | Good | Needs Improvement | Poor | Notes |
|--------|------|-------------------|------|-------|
| **LCP** (Largest Contentful Paint) | <=2.5s | 2.5s-4.0s | >4.0s | Loading — time until largest visible element renders |
| **INP** (Interaction to Next Paint) | <=200ms | 200ms-500ms | >500ms | Replaced FID March 2024. Measures ALL interactions |
| **CLS** (Cumulative Layout Shift) | <=0.1 | 0.1-0.25 | >0.25 | Visual stability — unexpected layout movements |

> **FID is dead.** INP replaced FID on March 12, 2024. FID was fully removed from all Chrome tools (CrUX API, PageSpeed Insights, Lighthouse) on September 9, 2024. Do NOT reference FID anywhere.

### LCP Subparts (for diagnosing slow LCP)

| Subpart | What It Measures | Target |
|---------|------------------|--------|
| **TTFB** | Time to First Byte (server response) | <800ms |
| **Resource Load Delay** | Time from TTFB to resource request start | Minimize |
| **Resource Load Time** | Time to download the LCP resource | Depends on size |
| **Element Render Delay** | Time from resource loaded to rendered | Minimize |

**Total LCP = TTFB + Resource Load Delay + Resource Load Time + Element Render Delay**

### How to Measure

**Chrome DevTools MCP (recommended for live measurement):**
- `chrome-devtools: debug-optimize-lcp` — Guided LCP debugging with waterfall analysis
- `chrome-devtools: lighthouse_audit` — Full Lighthouse audit including all CWV metrics

> These tools MEASURE performance. For fixing guidance, reference:
> - `${CLAUDE_PLUGIN_ROOT}/skills/references/web-quality/core-web-vitals/SKILL.md` — INP/LCP/CLS fix strategies
> - `${CLAUDE_PLUGIN_ROOT}/skills/references/web-quality/performance/SKILL.md` — Performance budgets, font optimization, caching

**Without CrUX data — estimate from page characteristics:**
- **LCP**: Check largest above-fold element. Image (check size/format)? Text (check web font loading)? Server response time (TTFB)?
- **INP**: Check for heavy JavaScript. Long tasks (>50ms) block interactivity. Third-party scripts?
- **CLS**: Images without explicit width/height? Dynamically inserted content above fold? Web fonts causing layout shift (FOUT/FOIT)?

### Common LCP Fixes
1. Optimize hero images: **WebP/AVIF** format, correct sizing, preload with `<link rel="preload">`
2. Reduce server response time (**TTFB < 800ms**)
3. Eliminate render-blocking CSS/JS
4. Preconnect to critical third-party origins: `<link rel="preconnect" href="...">`
5. Use `fetchpriority="high"` on LCP element

### Common INP Fixes
1. Break up long tasks (>50ms) into smaller chunks using `requestIdleCallback` or `scheduler.yield()`
2. Reduce third-party JavaScript
3. Use `content-visibility: auto` for off-screen content
4. Debounce/throttle event handlers
5. Defer non-critical JavaScript with `defer` attribute

### Common CLS Fixes
1. Always include `width` and `height` attributes on images and videos
2. Reserve space for ads and embeds with CSS `aspect-ratio` or explicit dimensions
3. Use `font-display: swap` with size-adjusted fallback fonts
4. Avoid inserting content above existing content after page load
5. Use `min-height` on dynamic containers

### Pass/Warn/Fail Thresholds
| Metric | Pass | Warn | Fail |
|--------|------|------|------|
| LCP | <=2.5s | 2.5s-4.0s | >4.0s |
| INP | <=200ms | 200ms-500ms | >500ms |
| CLS | <=0.1 | 0.1-0.25 | >0.25 |

### Scoring

**SEO sub-score (of 100) — weighted higher for SEO:**

| Check | Points |
|-------|--------|
| LCP <= 2.5s | 35 |
| INP <= 200ms | 35 |
| CLS <= 0.1 | 30 |

**GEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| LCP <= 2.5s | 35 |
| INP <= 200ms | 35 |
| CLS <= 0.1 | 30 |

---

## Category 7: Server-Side Rendering

### CRITICAL FOR GEO

### Why SSR Matters

**For GEO (CRITICAL):** AI crawlers (GPTBot, PerplexityBot, ClaudeBot, etc.) do **NOT execute JavaScript**. They fetch raw HTML and parse it. If content is rendered client-side by React, Vue, Angular, or any JavaScript framework, AI crawlers see an empty page.

**For SEO (important):** Even Googlebot, which does execute JavaScript, deprioritizes JS-rendered content. Google processes JS rendering in a separate "rendering queue" that can delay indexing by days or weeks.

### What to Check

#### 7.1 SSR Detection
1. Fetch the page with curl / WebFetch (no JavaScript execution)
2. Compare raw HTML to rendered DOM (via browser)
3. If key content (headings, paragraphs, product info, article text) is MISSING from the raw HTML, the site relies on client-side rendering

#### 7.2 Critical Elements in Raw HTML

| Element | In raw HTML? | Impact if missing |
|---------|:------------:|------------------|
| Main content text (article body, product description) | Required | AI crawlers see empty page |
| Headings (H1, H2, H3) | Required | No semantic structure for AI |
| Navigation / internal links | Required | Crawlability broken for all crawlers |
| Structured data (JSON-LD) | Required | No entity recognition |
| Meta tags (title, description, canonical, OG) | Required | No SEO signals |
| Images with alt text | Recommended | Missing media context |

#### 7.3 SSR Solutions by Framework

| Framework | SSR Solution | Notes |
|-----------|-------------|-------|
| React | **Next.js** (SSR/SSG/ISR) | Recommended. Turbopack default bundler in v16 |
| React | Remix | Full SSR, nested routing |
| React | Gatsby | SSG-focused |
| Vue | **Nuxt.js** (SSR/SSG) | Recommended |
| Angular | Angular Universal | SSR support |
| Svelte | **SvelteKit** | SSR/SSG built-in |
| Generic | Prerender.io | Prerendering service (not true SSR) |
| Generic | Rendertron | Google's prerendering solution |

### How to Check
- `curl -s [URL]` and inspect raw HTML for content presence
- `WebFetch` to retrieve raw HTML without JS execution
- Check for SPA framework markers without SSR:
  - React: `react-dom` present but `__NEXT_DATA__` absent = no Next.js
  - Vue: `__vue__` present but `__NUXT__` absent = no Nuxt
  - Angular: `ng-version` present but universal markers absent

### Pass/Warn/Fail Thresholds
| Check | Pass | Warn | Fail |
|-------|------|------|------|
| Main content in HTML | Fully server-rendered | Most content present, some JS-only | Content requires JS to render |
| Meta tags in HTML | All critical meta in raw HTML | Most present | Title/canonical JS-injected |
| Internal links | All nav links in raw HTML | Most present | Navigation is JS-rendered |
| Structured data | JSON-LD in raw HTML | Present but JS-injected | Missing entirely |

### Quick Fixes
- Migrate to SSR framework (Next.js, Nuxt, SvelteKit)
- Implement prerendering service (Prerender.io) as interim fix
- Ensure all meta tags are in server-rendered HTML, not JS-injected
- Move JSON-LD structured data to `<head>` in server template

### Scoring

**SEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| Main content in raw HTML | 50 |
| Meta tags + structured data in raw HTML | 30 |
| Internal links in raw HTML | 20 |

**GEO sub-score (of 100) — weighted 2x in overall GEO score:**

| Check | Points |
|-------|--------|
| Main content in raw HTML | 50 |
| Meta tags + structured data in raw HTML | 30 |
| Internal links in raw HTML | 20 |

> **GEO weighting note:** This category's GEO sub-score is multiplied by 2x in the overall GEO calculation. A site with client-side rendering that scores 0 here loses double the points in the GEO total.

---

## Category 8: Structured Data

### Basic Validation (detailed analysis in 42-structured-data)

This category provides a quick structural check. For full schema audit with code generation, use `42:structured-data`.

### What to Check
- JSON-LD detected? (preferred format)
- Microdata or RDFa only? Flag for migration to JSON-LD
- Organization/Person schema present? (entity recognition)
- Article schema with author details? (E-E-A-T signal)
- sameAs properties present? (entity graph for AI)
- Server-rendered or JavaScript-injected? (critical — JS-injected schema may not be processed by AI crawlers)

### How to Check
- Inspect raw HTML for `<script type="application/ld+json">` blocks
- Screaming Frog `structured_data.csv` for bulk analysis
- `WebFetch` to examine raw HTML for schema presence

### Pass/Warn/Fail Thresholds
| Check | Pass | Warn | Fail |
|-------|------|------|------|
| Schema format | JSON-LD in raw HTML | JSON-LD but JS-injected | Microdata only or none |
| Organization schema | Present with sameAs | Present without sameAs | Missing |
| Page-type schema | Correct type for page | Generic WebPage only | Missing |

### Quick Fixes
- Add JSON-LD Organization schema to site header
- Convert Microdata to JSON-LD format
- Move JS-injected schema to server-rendered HTML
- Run `42:structured-data` for comprehensive schema generation

### Scoring

**SEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| JSON-LD format used | 30 |
| Organization/entity schema present | 25 |
| Page-specific schema correct | 25 |
| Schema in server-rendered HTML (not JS) | 20 |

**GEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| JSON-LD format used | 25 |
| Organization/entity schema present | 25 |
| Page-specific schema correct | 20 |
| Schema in server-rendered HTML (not JS) | 30 |

---

## Category 9: JavaScript Rendering

### What to Check

#### 9.1 Content Visibility
- Check if content is visible in initial HTML vs requires JavaScript
- Identify client-side rendered (CSR) vs server-side rendered (SSR) vs static site generation (SSG)
- Flag SPA frameworks (React, Vue, Angular) running without SSR

#### 9.2 JavaScript SEO — Canonical & Indexing (December 2025)

Google updated JavaScript SEO documentation in December 2025 with critical clarifications:

1. **Canonical conflicts:** If canonical in raw HTML differs from one injected by JavaScript, Google may use EITHER one. Ensure canonical tags are identical between server-rendered and JS-rendered output.
2. **noindex with JavaScript:** If raw HTML contains `<meta name="robots" content="noindex">` but JavaScript removes it, Google MAY still honor the raw HTML noindex. Serve correct robots directives in initial HTML.
3. **Non-200 status codes:** Google does NOT render JavaScript on pages returning non-200 HTTP status codes. JS-injected content on error pages is invisible to Googlebot.
4. **Structured data in JavaScript:** Product, Article, and other structured data injected via JS may face delayed processing. For time-sensitive structured data, include in server-rendered HTML.

**Best practice:** Serve ALL critical SEO elements (canonical, meta robots, structured data, title, meta description) in initial server-rendered HTML. Never rely on JavaScript injection for these.

#### 9.3 Web Rendering Service (WRS) Considerations
- Googlebot uses a headless Chromium-based renderer (WRS)
- WRS renders with the latest stable Chrome version
- Rendering is queued separately from crawling — indexing delays of days/weeks
- Heavy JavaScript pages consume more crawl budget

#### 9.4 Hydration Issues
- Check for hydration mismatches (server HTML differs from client render)
- Mismatches can cause content flicker and SEO signal confusion
- Common in React/Next.js when server and client state diverge

### How to Check
- Compare `curl` output (raw HTML) with browser-rendered DOM
- Check for `__NEXT_DATA__`, `__NUXT__`, `ng-version` markers
- Look for empty `<div id="root">` or `<div id="app">` in raw HTML (CSR indicators)
- `chrome-devtools: lighthouse_audit` for JavaScript execution analysis

### Pass/Warn/Fail Thresholds
| Check | Pass | Warn | Fail |
|-------|------|------|------|
| Critical content | In initial HTML | Mostly in HTML, some JS-only | Requires JS to render |
| Meta tags | All in server HTML | Some JS-injected | All JS-injected |
| JS bundle size | <200KB compressed | 200-500KB | >500KB |
| Third-party scripts | Async/deferred | Some render-blocking | Multiple render-blocking |

### Quick Fixes
- Move critical content to server-rendered templates
- Add `defer` or `async` to non-critical scripts
- Implement code splitting for large JS bundles
- Ensure canonical/meta robots are in initial HTML response

### Scoring

**SEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| Critical content in initial HTML | 30 |
| SEO meta tags in server HTML | 25 |
| JS bundle size reasonable | 20 |
| No render-blocking third-party scripts | 15 |
| No hydration mismatches | 10 |

**GEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| Critical content in initial HTML | 35 |
| SEO meta tags in server HTML | 25 |
| JS bundle size reasonable | 15 |
| No render-blocking third-party scripts | 15 |
| No hydration mismatches | 10 |

---

## Category 10: IndexNow

### What It Is

IndexNow is an open protocol allowing websites to notify search engines instantly when content is created, updated, or deleted. Supported by **Bing, Yandex, Seznam, and Naver**. Google does NOT support IndexNow but monitors the protocol.

### Why It Matters for GEO

ChatGPT uses **Bing's index**. Bing Copilot uses **Bing's index**. Faster Bing indexing means faster AI visibility on two major AI platforms. Implementing IndexNow can reduce the time from content publication to AI citation from weeks to hours.

### What to Check
1. Check for IndexNow key file: `https://[domain]/.well-known/indexnow-key.txt` or similar
2. Check if CMS has IndexNow plugin:
   - WordPress: IndexNow plugin (official)
   - Many modern CMS platforms support natively
   - Next.js: can implement via API route
3. If not implemented, recommend adding with instructions

### How to Check
- `WebFetch` to check for IndexNow key file at common locations
- Check for IndexNow plugin references in HTML source
- Ask about CMS platform for plugin recommendations

### Pass/Warn/Fail Thresholds
| Check | Pass | Warn | Fail |
|-------|------|------|------|
| IndexNow | Implemented and active | Key file present but not integrated | Not implemented |

### Quick Fixes
- Install IndexNow plugin for your CMS
- Generate and host IndexNow key file
- Implement API endpoint to ping IndexNow on content publish/update

### Implementation Example

```
POST https://api.indexnow.org/IndexNow HTTP/1.1
Content-Type: application/json

{
  "host": "example.com",
  "key": "your-indexnow-key",
  "urlList": [
    "https://example.com/new-page",
    "https://example.com/updated-page"
  ]
}
```

### Scoring

**SEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| IndexNow key file present | 40 |
| Active integration (pings on publish) | 40 |
| Multiple search engines configured | 20 |

**GEO sub-score (of 100):**

| Check | Points |
|-------|--------|
| IndexNow key file present | 35 |
| Active integration (pings on publish) | 40 |
| Multiple search engines configured | 25 |

---

## Dual Scoring System

### SEO Score Calculation (0-100)

Traditional weighting with CWV and mobile weighted higher:

| Category | Weight | Notes |
|----------|--------|-------|
| Crawlability | 12% | Foundation |
| Indexability | 12% | Foundation |
| Security | 8% | Trust signal |
| URL Structure | 6% | Crawl efficiency |
| Mobile Optimization | **15%** | Google requires mobile-first |
| Core Web Vitals | **18%** | Ranking signal, Dec 2025 update weighted mobile CWV more |
| Server-Side Rendering | 5% | Nice-to-have (Google renders JS) |
| Structured Data | 8% | Rich results eligibility |
| JavaScript Rendering | 8% | Indexing efficiency |
| IndexNow | 8% | Non-Google indexing speed |

**SEO Score = Sum of (category sub-score x weight)**

### GEO Score Calculation (0-100)

SSR weighted 2x, AI crawler access weighted 2x:

| Category | Weight | Notes |
|----------|--------|-------|
| Crawlability | **16%** | AI crawler access sub-component weighted 2x within category |
| Indexability | 8% | Standard |
| Security | 5% | Standard |
| URL Structure | 4% | Standard |
| Mobile Optimization | 6% | Less critical for AI crawlers |
| Core Web Vitals | 8% | UX signal, less direct GEO impact |
| Server-Side Rendering | **20%** | **2x weight — AI crawlers cannot execute JS** |
| Structured Data | 9% | Entity recognition for AI |
| JavaScript Rendering | **16%** | **2x weight — content must be in raw HTML** |
| IndexNow | 8% | ChatGPT/Copilot via Bing index |

**GEO Score = Sum of (category sub-score x weight)**

### Status Thresholds (both scores)

| Score | Rating |
|-------|--------|
| 90-100 | Excellent |
| 70-89 | Good |
| 50-69 | Needs Work |
| 30-49 | Poor |
| 0-29 | Critical |

---

## Page Speed & Server Performance

> **Note:** Page speed checks are distributed across relevant categories above (TTFB in CWV/LCP subparts, resource optimization in JavaScript Rendering, image optimization in CWV/CLS). For comprehensive performance auditing including caching, CDN, compression, and performance budgets, reference:
> - `${CLAUDE_PLUGIN_ROOT}/skills/references/web-quality/performance/SKILL.md` — Performance budgets, font optimization, caching strategies
> - `chrome-devtools: lighthouse_audit` — Full Lighthouse performance score

Key server performance checks to include in the audit:

- **TTFB:** Target <800ms (ideally <200ms). Measure with `curl -o /dev/null -s -w 'TTFB: %{time_starttransfer}s\n' [URL]`
- **Compression:** gzip/brotli must be enabled (check `Content-Encoding` header)
- **CDN:** Check for CDN headers (`CF-Ray`, `X-Cache`, `X-Served-By`, `X-Vercel-Cache`)
- **Caching:** Static assets should have `Cache-Control: max-age=31536000` with content-hashed filenames
- **Page weight:** Target <2MB total (critical pages <1MB)

---

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, enhance the audit with live data:

| Tool | Purpose | Category |
|------|---------|----------|
| `on_page_instant_pages` | Real page analysis: status codes, timing, broken links | Crawlability, URL Structure |
| `on_page_lighthouse` | Lighthouse audit: performance, accessibility, SEO scores | CWV, Performance |
| `domain_analytics_technologies_domain_technologies` | Technology stack detection | SSR/JS detection |

These are optional enrichments — the audit works fully without them using WebFetch.

---

## Output Format

```markdown
## Technical Audit — [domain]

Date: [Date]
Pages analyzed: [List of URLs]
Input: [Screaming Frog CSV / Live crawl / Single URL]

| Category | SEO Score | GEO Score | Issues |
|----------|-----------|-----------|--------|
| Crawlability | 85 | 72 | 3 |
| Indexability | 90 | 90 | 1 |
| Security | 75 | 75 | 4 |
| URL Structure | 95 | 95 | 1 |
| Mobile | 80 | 80 | 2 |
| Core Web Vitals | 60 | 60 | 3 |
| Server-Side Rendering | 70 | 70 | 2 |
| Structured Data | 50 | 45 | 5 |
| JavaScript Rendering | 65 | 55 | 4 |
| IndexNow | 0 | 0 | 1 |

**Overall SEO Technical Score: X/100**
**Overall GEO Technical Score: X/100**

### AI Crawler Access

| Crawler | User-Agent | Tier | Status | Recommendation |
|---------|-----------|------|--------|----------------|
| GPTBot | GPTBot | 1 | Allowed/Blocked | [Action] |
| ChatGPT-User | ChatGPT-User | 1 | Allowed/Blocked | [Action] |
| Googlebot | Googlebot | 1 | Allowed/Blocked | [Action] |
| Bingbot | bingbot | 1 | Allowed/Blocked | [Action] |
[Continue for all crawlers]

### Server-Side Rendering Assessment

| Element | In Raw HTML | Status |
|---------|:-----------:|--------|
| Main content text | Yes/No | [Impact] |
| Headings (H1-H3) | Yes/No | [Impact] |
| Navigation links | Yes/No | [Impact] |
| Structured data (JSON-LD) | Yes/No | [Impact] |
| Meta tags | Yes/No | [Impact] |

### Core Web Vitals

| Metric | Value | Rating | Fix Priority |
|--------|-------|--------|-------------|
| LCP | X.Xs | Good/Needs Work/Poor | [Specific fix] |
| INP | Xms | Good/Needs Work/Poor | [Specific fix] |
| CLS | X.XX | Good/Needs Work/Poor | [Specific fix] |

### Critical Issues
[Fix immediately — items scoring 0 or blocking crawling/indexing]

### High Priority
[Fix within 1 week — items causing significant score reduction]

### Medium Priority
[Fix within 1 month — optimization opportunities]

### Low Priority
[Backlog — minor improvements]

### Detailed Findings
[Per-category breakdown with evidence and specific URLs]
```

---

## Cross-References

- For **CWV thresholds and subparts** -> `${CLAUDE_PLUGIN_ROOT}/skills/references/cwv-thresholds.md`
- For **CWV fix guidance** -> `${CLAUDE_PLUGIN_ROOT}/skills/references/web-quality/core-web-vitals/SKILL.md`
- For **performance budgets and optimization** -> `${CLAUDE_PLUGIN_ROOT}/skills/references/web-quality/performance/SKILL.md`
- For **CWV measurement** -> `chrome-devtools: debug-optimize-lcp` and `chrome-devtools: lighthouse_audit`
- For **full schema audit** -> `42:structured-data`
- For **AI crawler reference** -> `42:crawlers`
- For **content quality & E-E-A-T** -> `42:content`
- For **image optimization** -> `42:images`
