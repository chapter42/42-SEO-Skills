---
name: 42-competitor-pages
version: 2.0.0
description: >
  Generate SEO-optimized competitor comparison and alternatives pages. Covers
  "X vs Y" layouts, "alternatives to X" pages, feature matrices, schema markup,
  and conversion optimization. Integrates SERP data via DataForSEO for competitor
  keyword gap analysis. Use when user says "comparison page", "vs page",
  "alternatives page", "competitor comparison", or "X vs Y".
---

# Competitor Comparison & Alternatives Pages

Create high-converting comparison and alternatives pages that target
competitive intent keywords with accurate, structured content.

## Page Types

### 1. "X vs Y" Comparison Pages
- Direct head-to-head comparison between two products/services
- Balanced feature-by-feature analysis
- Clear verdict or recommendation with justification
- Target keyword: `[Product A] vs [Product B]`

### 2. "Alternatives to X" Pages
- List of alternatives to a specific product/service
- Each alternative with brief summary, pros/cons, best-for use case
- Target keyword: `[Product] alternatives`, `best alternatives to [Product]`

### 3. "Best [Category] Tools" Roundup Pages
- Curated list of top tools/services in a category
- Ranking criteria clearly stated
- Target keyword: `best [category] tools [year]`, `top [category] software`

### 4. Comparison Table Pages
- Feature matrix with multiple products in columns
- Sortable/filterable if interactive
- Target keyword: `[category] comparison`, `[category] comparison chart`

## SERP Data Integration (DataForSEO)

Use DataForSEO to identify competitor keyword gaps and validate comparison page opportunities before writing.

### Competitor Keyword Gap Analysis

**Step 1: Pull competitor ranked keywords**

For each competitor domain, fetch their organic keywords:

```bash
curl -s --user "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" \
  https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live \
  -X POST \
  -H "Content-Type: application/json" \
  -d '[{
    "target": "competitor-domain.com",
    "language_code": "en",
    "location_code": 2840,
    "limit": 100,
    "filters": ["keyword_data.keyword_info.search_volume", ">", 100],
    "order_by": ["keyword_data.keyword_info.search_volume,desc"]
  }]'
```

**Step 2: Find comparison-intent keywords**

Filter for keywords containing comparison signals:
- "vs", "versus", "compared to", "alternative", "alternatives"
- "better than", "switch from", "migrate from"
- "[your product] vs", "[competitor] alternative"

**Step 3: Run keyword gap analysis**

Use the Domain Intersection endpoint to find keywords competitors rank for that you do not:

```bash
curl -s --user "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" \
  https://api.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live \
  -X POST \
  -H "Content-Type: application/json" \
  -d '[{
    "target1": "competitor-domain.com",
    "target2": "your-domain.com",
    "language_code": "en",
    "location_code": 2840,
    "intersect_type": "not_intersecting",
    "limit": 50,
    "filters": ["keyword_data.keyword_info.search_volume", ">", 50],
    "order_by": ["keyword_data.keyword_info.search_volume,desc"]
  }]'
```

This returns keywords where the competitor ranks but you do not -- these are gap opportunities for new comparison pages.

**Step 4: Validate SERP landscape**

For the top comparison keyword opportunities, check the current SERP:

```bash
curl -s --user "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" \
  https://api.dataforseo.com/v3/serp/google/organic/live/advanced \
  -X POST \
  -H "Content-Type: application/json" \
  -d '[{
    "keyword": "[Product A] vs [Product B]",
    "language_code": "en",
    "location_code": 2840,
    "depth": 10
  }]'
```

Analyze who currently ranks: are they product sites, review sites, or aggregators? This determines the content depth and format needed to compete.

**If DataForSEO is unavailable:** Use WebSearch to manually research comparison keywords. Search for `[competitor] vs`, `[competitor] alternatives`, and note which comparison pages rank. This is slower but functional.

---

## Comparison Table Generation

### Feature Matrix Layout
```
| Feature          | Your Product | Competitor A | Competitor B |
|------------------|:------------:|:------------:|:------------:|
| Feature 1        | Yes          | Yes          | No           |
| Feature 2        | Yes          | Partial      | Yes          |
| Feature 3        | Yes          | No           | No           |
| Pricing (from)   | $X/mo        | $Y/mo        | $Z/mo        |
| Free Tier        | Yes          | No           | Yes          |
```

### Data Accuracy Requirements
- All feature claims must be verifiable from public sources
- Pricing must be current (include "as of [date]" note)
- Update frequency: review quarterly or when competitors ship major changes
- Link to source for each competitor data point where possible

## Schema Markup Recommendations

### Product Schema with AggregateRating
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Product Name]",
  "description": "[Product Description]",
  "brand": {
    "@type": "Brand",
    "name": "[Brand Name]"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[Rating]",
    "reviewCount": "[Count]",
    "bestRating": "5",
    "worstRating": "1"
  }
}
```

### SoftwareApplication (for software comparisons)
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "[Software Name]",
  "applicationCategory": "[Category]",
  "operatingSystem": "[OS]",
  "offers": {
    "@type": "Offer",
    "price": "[Price]",
    "priceCurrency": "USD"
  }
}
```

### ItemList (for roundup pages)
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Best [Category] Tools [Year]",
  "itemListOrder": "https://schema.org/ItemListOrderDescending",
  "numberOfItems": "[Count]",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "[Product Name]",
      "url": "[Product URL]"
    }
  ]
}
```

## Keyword Targeting

### Comparison Intent Patterns
| Pattern | Example | Search Volume Signal |
|---------|---------|---------------------|
| `[A] vs [B]` | "Slack vs Teams" | High |
| `[A] alternative` | "Figma alternatives" | High |
| `[A] alternatives [year]` | "Notion alternatives 2026" | High |
| `best [category] tools` | "best project management tools" | High |
| `[A] vs [B] for [use case]` | "AWS vs Azure for startups" | Medium |
| `[A] review [year]` | "Monday.com review 2026" | Medium |
| `[A] vs [B] pricing` | "HubSpot vs Salesforce pricing" | Medium |
| `is [A] better than [B]` | "is Notion better than Confluence" | Medium |

### Title Tag Formulas
- X vs Y: `[A] vs [B]: [Key Differentiator] ([Year])`
- Alternatives: `[N] Best [A] Alternatives in [Year] (Free & Paid)`
- Roundup: `[N] Best [Category] Tools in [Year], Compared & Ranked`

### H1 Patterns
- Match title tag intent
- Include primary keyword naturally
- Keep under 70 characters

## Conversion-Optimized Layouts

### CTA Placement
- **Above fold**: Brief comparison summary with primary CTA
- **After comparison table**: "Try [Your Product] free" CTA
- **Bottom of page**: Final recommendation with CTA
- Avoid aggressive CTAs in competitor description sections (reduces trust)

### Social Proof Sections
- Customer testimonials relevant to comparison criteria
- G2/Capterra/TrustPilot ratings (with source links)
- Case studies showing migration from competitor
- "Switched from [Competitor]" stories

### Pricing Highlights
- Clear pricing comparison table
- Highlight value advantages (not just lowest price)
- Include hidden costs (setup fees, per-user pricing, overage charges)
- Link to full pricing page

### Trust Signals
- "Last updated [date]" timestamp
- Author with relevant expertise
- Methodology disclosure (how comparisons were conducted)
- Disclosure of own product affiliation

## Fairness Guidelines

For detailed fairness thresholds and scoring criteria for competitor content, see `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md`.

Core principles:
- **Accuracy**: All competitor information must be verifiable from public sources
- **No defamation**: Never make false or misleading claims about competitors
- **Cite sources**: Link to competitor websites, review sites, or documentation
- **Timely updates**: Review and update when competitors release major changes
- **Disclose affiliation**: Clearly state which product is yours
- **Balanced presentation**: Acknowledge competitor strengths honestly
- **Pricing accuracy**: Include "as of [date]" disclaimers on all pricing data
- **Feature verification**: Test competitor features where possible, cite documentation otherwise

## Internal Linking

- Link to your own product/service pages from comparison sections
- Cross-link between related comparison pages (e.g., "A vs B" links to "A vs C")
- Link to feature-specific pages when discussing individual features
- Breadcrumb: Home > Comparisons > [This Page]
- Related comparisons section at bottom of page
- Link to case studies and testimonials mentioned in the comparison

## Output

### Comparison Page Template
- `COMPARISON-PAGE.md`: Ready-to-implement page structure with sections
- Feature matrix table
- Content outline with word count targets (minimum 1,500 words)

### Schema Markup
- `comparison-schema.json`: Product/SoftwareApplication/ItemList JSON-LD

### Keyword Strategy
- Primary and secondary keywords
- Related long-tail opportunities
- Content gaps vs existing competitor pages
- DataForSEO keyword gap data (if available)

### Recommendations
- Content improvements for existing comparison pages
- New comparison page opportunities (from gap analysis)
- Schema markup additions
- Conversion optimization suggestions

## Error Handling

| Scenario | Action |
|----------|--------|
| Competitor URL unreachable | Report which competitor URLs failed. Proceed with available data and note gaps in the comparison. |
| Insufficient competitor data (pricing, features unavailable) | Flag missing data points clearly. Use "Not publicly available" in comparison tables rather than guessing. |
| No product/service overlap found | Report that the products serve different markets. Suggest alternative competitors that share feature overlap, or pivot to a category roundup format. |
| DataForSEO unavailable | Fall back to manual WebSearch research for keyword gaps. Note reduced data quality in the report. |
