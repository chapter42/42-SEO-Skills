---
name: 42-page-analysis
version: 2.0.0
description: >
  Deep single-page SEO analysis covering on-page elements, content quality,
  technical meta tags, schema, images, and performance. Supports optional
  Screaming Frog data input and Chrome DevTools MCP for CWV/Lighthouse.
  Use when user says "analyze this page", "check page SEO", or provides
  a single URL for review.
---

# Single Page Analysis

## Optional Data Inputs

Before starting the analysis, check if additional data sources are available:

### Screaming Frog Data (Optional)

If the user provides Screaming Frog crawl data for this URL, use it to enrich the analysis:

1. **How to use SF data**: Look for the URL in the SF export CSV. Relevant columns:
   - `Title 1`, `Title 1 Length`, `Title 1 Pixel Width` -- title tag data
   - `Meta Description 1`, `Meta Description 1 Length` -- meta description
   - `H1-1`, `H2-1`, `H2-2`, etc. -- heading hierarchy
   - `Canonical Link Element 1` -- canonical tag
   - `Meta Robots 1` -- robots directives
   - `Status Code` -- HTTP status
   - `Word Count` -- page word count
   - `Indexability`, `Indexability Status` -- whether SF considers it indexable
   - `Response Time` -- server response time
   - `Inlinks` -- number of internal links pointing to this page
   - `Outlinks` -- number of links on this page
   - `Unique Inlinks` -- deduplicated internal link count
   - `Crawl Depth` -- clicks from homepage

2. **Cross-reference SF data with live analysis**: If SF data and live fetch disagree (e.g., different title tag), flag this -- it may indicate recent changes or dynamic rendering differences.

3. **SF-only metrics to include**: Crawl depth, inlink count, response time, and indexability status are not available from a simple page fetch. When SF data provides these, add them to the analysis.

### Chrome DevTools MCP (Optional)

If the Chrome DevTools MCP is available, use it for real per-page Core Web Vitals and Lighthouse data:

1. **Lighthouse audit**: Run `lighthouse_audit` on the URL to get actual LCP, INP proxy, CLS scores, accessibility score, and performance score.
2. **Performance trace**: Use `performance_start_trace` and `performance_stop_trace` to capture real rendering performance.
3. **Network analysis**: Use `list_network_requests` to identify render-blocking resources, large payloads, and slow third-party scripts.

When Chrome DevTools MCP is available, replace the "reference only" CWV section with actual measured data.

---

## What to Analyze

### On-Page SEO
- Title tag: 50-60 characters, includes primary keyword, unique
- Meta description: 150-160 characters, compelling, includes keyword
- H1: exactly one, matches page intent, includes keyword
- H2-H6: logical hierarchy (no skipped levels), descriptive
- URL: short, descriptive, hyphenated, no parameters
- Internal links: sufficient, relevant anchor text, no orphan pages
- External links: to authoritative sources, reasonable count

### Content Quality
- Word count vs page type minimums (see quality-gates.md)
- Readability: Flesch Reading Ease score, grade level
- Keyword density: natural (1-3%), semantic variations present
- E-E-A-T signals: author bio, credentials, first-hand experience markers
- Content freshness: publication date, last updated date

### Technical Elements
- Canonical tag: present, self-referencing or correct
- Meta robots: index/follow unless intentionally blocked
- Open Graph: og:title, og:description, og:image, og:url
- Twitter Card: twitter:card, twitter:title, twitter:description
- Hreflang: if multi-language, correct implementation

### Schema Markup
- Detect all types (JSON-LD preferred)
- Validate required properties
- Identify missing opportunities
- NEVER recommend HowTo (deprecated) or FAQ (restricted to gov/health)

### Images
- Alt text: present, descriptive, includes keywords where natural
- File size: flag >200KB (warning), >500KB (critical)
- Format: recommend WebP/AVIF over JPEG/PNG
- Dimensions: width/height set for CLS prevention
- Lazy loading: loading="lazy" on below-fold images

### Core Web Vitals

**Without Chrome DevTools MCP** (reference only -- not measurable from HTML alone):
- Flag potential LCP issues (huge hero images, render-blocking resources)
- Flag potential INP issues (heavy JS, no async/defer)
- Flag potential CLS issues (missing image dimensions, injected content)

**With Chrome DevTools MCP** (actual measurements):
- LCP: measured value and element identified. Target < 2.5s.
- INP: interaction responsiveness proxy. Target < 200ms.
- CLS: measured layout shift score. Target < 0.1.
- Performance score: Lighthouse overall (0-100)
- Accessibility score: Lighthouse a11y audit (0-100)
- Render-blocking resources: list with size and impact
- Largest resource loads: top 5 by size with recommendations

For deep-dive accessibility and performance analysis beyond what this single-page audit covers, see `${CLAUDE_PLUGIN_ROOT}/skills/references/web-quality/` (accessibility patterns, performance optimization, and best practices).

## Output

### Page Score Card
```
Overall Score: XX/100

On-Page SEO:     XX/100  --------..
Content Quality: XX/100  ..........
Technical:       XX/100  -------...
Schema:          XX/100  ------.....
Images:          XX/100  --------..
```

If SF data available, add:
```
Crawl Depth:     X clicks from homepage
Internal Links:  XX inlinks / XX outlinks
Response Time:   XXXms
Indexability:     [Indexable / Non-Indexable: reason]
```

If Chrome DevTools available, add:
```
LCP:             X.Xs [Good/Needs Improvement/Poor]
CLS:             X.XX [Good/Needs Improvement/Poor]
Performance:     XX/100
Accessibility:   XX/100
```

### Issues Found
Organized by priority: Critical > High > Medium > Low

### Recommendations
Specific, actionable improvements with expected impact

### Schema Suggestions
Ready-to-use JSON-LD code for detected opportunities

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `serp_organic_live_advanced` for real SERP positions and `backlinks_summary` for backlink data and spam scores.
