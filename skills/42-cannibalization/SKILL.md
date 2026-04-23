---
name: 42-cannibalization
version: 2.0.0
description: >
  Detect keyword cannibalization across all site pages by extracting primary
  keywords from titles and headings, clustering semantically similar targets,
  and flagging pages competing for the same search intent. Works site-wide
  (blog, product, category, landing pages). Supports local-only mode
  (grep-based) and DataForSEO API mode (Page Intersection endpoint at
  ~$0.01/call). Accepts 42-keyword-mapper output as input for pre-built
  keyword-to-URL mappings. Outputs severity-scored report with merge or
  differentiate recommendations. Use when user says "cannibalization",
  "keyword overlap", "competing pages", "duplicate keywords", "cannibalize".
user-invokable: true
argument-hint: "[directory or URL list] [--api] [--keyword-map path/to/keyword-mapper-output.csv]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
---

# Site-Wide Cannibalization -- Keyword Overlap Detection

Detect when multiple pages across your entire site compete for the same search keywords. This is not limited to blog posts -- it covers all indexable page types: blog, product, category, service, landing pages, and more.

## Two Modes

| Mode | Flag | Cost | Data Source |
|------|------|------|-------------|
| Local | (default) | Free | File content analysis via Grep/Read |
| API | `--api` | ~$0.01/call | DataForSEO Page Intersection + Ranked Keywords |

Local mode works without any API keys. API mode requires DataForSEO credentials
set as environment variables: `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`.

## Using 42-keyword-mapper Output as Input

If the user has previously run `42-keyword-mapper`, its output provides a pre-built mapping of keywords to URLs. This significantly improves cannibalization detection:

### How to Use Keyword Mapper Data

1. **Accept the file**: The user provides a CSV or Markdown table from 42-keyword-mapper with columns like: `Keyword`, `Primary URL`, `Secondary URLs`, `Search Volume`, `Intent`.
2. **Parse mappings**: Read each row to build a keyword-to-URL mapping.
3. **Detect conflicts**: Flag any keyword that maps to 2+ URLs as a cannibalization candidate.
4. **Enrich with context**: For each conflict, check whether the keyword mapper already designated a primary URL. If so, the secondary URLs are the cannibalization risk.
5. **Skip local extraction for mapped keywords**: When keyword mapper data is available, skip the manual keyword extraction (Step 2 below) for those keywords. Only extract keywords from pages NOT covered by the mapper output.

**Benefits of keyword mapper input:**
- Pre-validated keyword assignments reduce false positives
- Search volume data is already available (no need for API calls)
- Intent classification helps distinguish genuine cannibalization from multi-intent coverage

---

## Local Mode Workflow

### Step 1: Scan Site Files

Use Glob to find all content files in the target directory:
- Patterns: `**/*.md`, `**/*.mdx`, `**/*.html`, `**/*.tsx`, `**/*.jsx`
- Skip files in `node_modules/`, `.git/`, `drafts/`, `components/`, `layouts/`
- Include product pages, category pages, service pages -- not just blog posts

For URL-based analysis (when user provides a list of URLs or a sitemap):
- Fetch each URL with WebFetch
- Extract content from the HTML response

### Step 2: Extract Primary Keywords

For each page, read and extract keyword signals from:
- **Title tag** or H1 heading (highest weight)
- **H2 headings** (medium weight)
- **First paragraph** (supporting signal)
- **Meta description** if present in frontmatter
- **URL slug** (supporting signal for non-blog pages)

Primary keyword extraction method:
1. Tokenize title and H1 into 1-gram, 2-gram, and 3-gram phrases
2. Score each phrase by frequency across title + H2s + first paragraph
3. Select the top-scoring 2-3 word phrase as the primary keyword
4. Record secondary keywords from H2 headings

### Step 3: Cluster by Similarity

Group pages into clusters using these matching rules (in priority order):

1. **Exact match** - identical primary keyword across 2+ pages
2. **Stem match** - same root word (e.g., "optimize" vs "optimization")
3. **Semantic overlap** - Claude determines that two keywords target the same
   search intent (e.g., "best CRM software" vs "top CRM tools 2026")
4. **Subset match** - one keyword contains another (e.g., "email marketing"
   vs "email marketing for startups")

**Cross-type cannibalization** (unique to site-wide analysis):
- Blog post vs product page targeting the same keyword
- Category page vs landing page with overlapping intent
- Service page vs blog post covering the same topic
- Flag these explicitly as they require different resolution strategies

### Step 4: Score and Flag

For each cluster with 2+ pages, assess severity and generate a recommendation.

### Step 5: Output Report

Display the results table and per-cluster recommendations.

## API Mode Workflow (DataForSEO)

Requires the `--api` flag. Uses WebFetch to call DataForSEO endpoints.

### Endpoints Used

**Page Intersection** - find keywords where multiple URLs rank:
```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/page_intersection/live
Authorization: Basic <base64(login:password)>

{
  "pages": {
    "1": "https://example.com/page-a",
    "2": "https://example.com/page-b"
  },
  "language_code": "en",
  "location_code": 2840
}
```
Cost: ~$0.01 per call. Returns overlapping keywords with position, volume, CPC.

**Ranked Keywords** - get all keywords a single URL ranks for:
```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live

{
  "target": "https://example.com/page-a",
  "language_code": "en",
  "location_code": 2840
}
```

### API Analysis Steps

1. Collect all published URLs from the user (or sitemap)
2. Run Ranked Keywords for each URL to build keyword profiles
3. Run Page Intersection for URL pairs that share keyword clusters
4. Calculate severity using the formula below
5. Output enriched report with search volume and position data

## Severity Scoring

Four severity levels based on overlap signals:

| Level | Criteria | Action Urgency |
|-------|----------|----------------|
| Critical | Same exact keyword, both pages in top 20 | Immediate |
| High | Same keyword cluster, one page outranks the other | This week |
| Medium | Related keywords with partial SERP overlap | This month |
| Low | Semantic similarity but different confirmed intents | Monitor |

### Severity Formula (API Mode)

```
severity_score = overlap_count x avg_search_volume x (1 / position_gap)
```

Where:
- `overlap_count` = number of shared ranking keywords
- `avg_search_volume` = mean monthly volume of shared keywords
- `position_gap` = absolute difference in average ranking position (min 1)

Higher score = more urgent cannibalization problem.

### Severity Heuristic (Local Mode)

Without SERP data, use a simplified scoring:
- **Critical**: Exact primary keyword match between pages
- **High**: Stem match on primary keyword, or 3+ shared H2 keywords
- **Medium**: Semantic overlap on primary keyword
- **Low**: Subset match only, or shared secondary keywords

## Output Format

### Summary Table

```
| Page A | Page B | Page Types | Shared Keywords | Severity | Recommendation |
|--------|--------|------------|-----------------|----------|----------------|
| /best-crm-tools | /top-crm-software | blog vs blog | best crm, crm tools | Critical | MERGE |
| /crm-features | /blog/crm-guide | product vs blog | crm software, crm | High | DIFFERENTIATE |
| /email-tips | /email-marketing-guide | blog vs blog | email marketing | High | DIFFERENTIATE |
| /seo-basics | /seo-for-beginners | blog vs blog | seo basics | Critical | CANONICAL |
| /services/seo | /blog/what-is-seo | service vs blog | seo | Medium | DIFFERENTIATE |
```

### Per-Cluster Detail

For each flagged cluster, provide:
- Both page titles, URLs, and page types
- Full list of overlapping keywords (with volume if API mode)
- Which page is stronger (more comprehensive, better structured, higher authority)
- Specific recommendation with rationale
- Whether 42-keyword-mapper already assigned a primary URL

## Recommendations

Five possible actions for each cannibalization cluster:

### MERGE
When both pages are thin or cover the same intent with similar depth.
- Combine the best content from both into one comprehensive page
- 301 redirect the weaker URL to the merged page
- Preserve all internal links pointing to either URL

### DIFFERENTIATE
When pages serve different intents but keyword targeting overlaps.
- Shift the primary keyword of the weaker page to a related long-tail
- Update the title, H1, and meta description to reflect the new focus
- Add internal links between the two pages to signal distinct topics

### CANONICAL
When one page is clearly the authority and the other is a lesser duplicate.
- Add `rel="canonical"` on the weaker page pointing to the authority
- Consider noindexing the weaker page if it adds no unique value
- Link from the weaker page to the authority page

### RESTRUCTURE
When a blog post and a product/service page compete (cross-type cannibalization).
- The product/service page should own the transactional keyword
- The blog post should shift to informational intent (how-to, guide, comparison)
- Add a clear internal link from the blog post to the product/service page
- Update the blog post's title and H1 to reflect informational framing

### NO ACTION
When intent is genuinely different despite surface-level keyword similarity.
- Document the reasoning for future audits
- Monitor rankings quarterly for any position changes
- Re-evaluate if either page drops in rankings

## Error Handling

- **No content files found**: If the directory contains no content files, report "No content files found in [directory]" and suggest checking the path
- **DataForSEO credentials missing**: In API mode, if credentials are not configured, fall back to local mode automatically and notify the user
- **API rate limits**: DataForSEO has per-minute rate limits. If a 429 response is received, wait and retry once. If it persists, switch to local mode for remaining URLs
- **WebFetch failures**: If a source URL is unreachable, skip it and note "Unable to verify - source unavailable" in the report
- **Single-page directory**: If only one page exists, report "Cannibalization analysis requires at least 2 pages" and exit gracefully
- **Keyword mapper file not found**: If `--keyword-map` path is invalid, warn and proceed with standard extraction
