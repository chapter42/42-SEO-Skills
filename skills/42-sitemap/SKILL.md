---
name: 42-sitemap
version: 2.0.0
description: >
  Analyze existing XML sitemaps or generate new ones with industry-specific
  guidance. Validates format, URLs, structure, and cross-references with crawl
  data. Covers standard, image, video, and news sitemaps. Use when user says
  "sitemap", "generate sitemap", "sitemap issues", or "XML sitemap".
---

# Sitemap Analysis & Generation

## Mode 1: Analyze Existing Sitemap

### Step 1: Fetch and Parse Sitemap

1. Fetch the sitemap URL (typically `/sitemap.xml` or `/sitemap_index.xml`)
2. If a sitemap index, fetch each child sitemap
3. Parse all `<url>` entries, recording `<loc>`, `<lastmod>`, and any extensions (image, video, news namespaces)
4. Count total URLs across all sitemaps

### Step 2: Validate Format and Protocol Compliance

Run these checks against every sitemap file:

| Check | Rule | Severity |
|-------|------|----------|
| Valid XML | Well-formed XML, correct namespace declaration | Critical |
| URL count | < 50,000 per file (protocol limit) | Critical |
| File size | < 50MB uncompressed per file | Critical |
| HTTPS only | No HTTP URLs in sitemap | High |
| No fragments | No `#anchor` in URLs | Medium |
| No parameters | Flag URLs with query strings (unless intentional) | Low |
| Encoding | UTF-8, properly escaped special characters | Medium |

### Step 3: Validate URL Status

For each URL (or a representative sample for large sitemaps):

1. Check HTTP status code -- all should return 200
2. Flag redirected URLs (301/302) -- update to final destination
3. Flag non-200 URLs (404, 410, 500) -- remove from sitemap
4. Check canonical tag on each URL -- must match the sitemap URL
5. Check meta robots -- no `noindex` URLs should be in sitemap

### Step 4: Assess Quality Signals

| Signal | What to Check | Action |
|--------|--------------|--------|
| `<lastmod>` accuracy | Are dates realistic and varied? | Flag if all identical or clearly fake |
| Deprecated tags | `<priority>` and `<changefreq>` present? | Recommend removal (ignored by Google) |
| Non-canonical URLs | URLs that canonicalize elsewhere | Remove from sitemap |
| Noindexed URLs | URLs with `noindex` directive | Remove from sitemap |
| Sitemap in robots.txt | `Sitemap:` directive present | Add if missing |

### Step 5: Cross-Reference with Crawl Data

If Screaming Frog crawl data is available, compare:

1. **URLs in sitemap but NOT crawled**: These may be orphan pages (no internal links pointing to them). Investigate whether they are linked from the site or only discoverable via sitemap.
2. **URLs crawled but NOT in sitemap**: These are missing from the sitemap. Add indexable, canonical, 200-status pages to the sitemap.
3. **Discrepancy report**:

```
| Category | Count | Action |
|----------|-------|--------|
| In sitemap + crawled (healthy) | XXX | No action |
| In sitemap, not crawled (orphans) | XX | Add internal links or remove |
| Crawled, not in sitemap (missing) | XX | Add to sitemap |
| In sitemap, non-200 | XX | Remove or fix |
| In sitemap, noindexed | XX | Remove from sitemap |
```

**How to get SF crawl data**: Export from Screaming Frog > Bulk Export > All URLs, or use the Internal tab CSV. The `Address` column contains crawled URLs. Match against sitemap `<loc>` entries.

### Step 6: Output Validation Report

Produce a `VALIDATION-REPORT.md` with:
- Total URL count across all sitemaps
- Pass/fail for each validation check
- Issues list sorted by severity (Critical > High > Medium > Low)
- Crawl data discrepancy table (if SF data provided)
- Specific fix recommendations

---

## Mode 2: Generate New Sitemap

### Step 1: Determine Site Type and Structure

1. Ask for business type (or auto-detect from existing site)
2. Identify content types: pages, blog posts, products, categories, images, videos
3. Estimate total URL count to determine if sitemap index is needed

### Step 2: Plan Sitemap Architecture

Decide on sitemap split strategy:

**When to use a sitemap index:**
- Total URLs > 10,000 (recommended) or > 50,000 (required)
- Multiple distinct content types
- Different update cadences per content type

**Split by content type (recommended for most sites):**
```
sitemap_index.xml
  sitemap-pages.xml        -- static pages, about, contact, service pages
  sitemap-blog.xml         -- blog posts / articles
  sitemap-products.xml     -- product pages (e-commerce)
  sitemap-categories.xml   -- category / collection pages
  sitemap-images.xml       -- image sitemap (optional, see below)
  sitemap-videos.xml       -- video sitemap (optional, see below)
  sitemap-news.xml         -- news sitemap (publishers only)
```

**Split by URL range (for very large single-type sites):**
- Use when a single content type exceeds 50,000 URLs
- Split alphabetically or by ID range: `sitemap-products-1.xml`, `sitemap-products-2.xml`

### Step 3: Apply Quality Gates

Before generating URLs:
- WARNING at 30+ location pages (require 60%+ unique content)
- HARD STOP at 50+ location pages (require justification)
- Only include indexable, canonical, 200-status URLs
- Exclude URLs behind login, search result pages, paginated archives, faceted navigation

### Step 4: Generate XML Files

Generate valid XML with correct namespace declarations for each sitemap type.

### Step 5: Configure Lastmod and Update Cadence

| Content Type | Lastmod Source | Recommended Update Cadence |
|-------------|---------------|---------------------------|
| Static pages | CMS last-modified date | Update sitemap when page content changes |
| Blog posts | Publication or last-edit date | Regenerate daily or on publish |
| Products | Price/stock change date | Regenerate daily for active catalogs |
| Categories | Last product added/removed date | Regenerate weekly |
| News articles | Publication timestamp (required) | Regenerate every 15 minutes |

**Lastmod rules:**
- Use actual modification dates, never hardcode a single date for all URLs
- Use W3C Datetime format: `YYYY-MM-DD` or `YYYY-MM-DDThh:mm:ss+00:00`
- Update lastmod ONLY when content meaningfully changes (not on every deploy)
- Google uses lastmod as a crawl priority signal -- accurate dates improve crawl efficiency

### Step 6: Submit and Document

1. Add `Sitemap: https://example.com/sitemap_index.xml` to robots.txt
2. Submit in Google Search Console > Sitemaps
3. Generate `STRUCTURE.md` documenting the sitemap architecture

---

## Sitemap Types Reference

### Standard Sitemap
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2026-02-07</lastmod>
  </url>
</urlset>
```

### Sitemap Index
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
    <lastmod>2026-02-07</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-blog.xml</loc>
    <lastmod>2026-04-10</lastmod>
  </sitemap>
</sitemapindex>
```

### Image Sitemap

Use the image sitemap extension to help search engines discover images that may not be found through crawling (e.g., JavaScript-loaded images, images in carousels).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://example.com/product/blue-shoes</loc>
    <image:image>
      <image:loc>https://example.com/images/blue-shoes-front.webp</image:loc>
      <image:caption>Front view of blue running shoes Model X</image:caption>
      <image:title>Blue Running Shoes Model X</image:title>
    </image:image>
    <image:image>
      <image:loc>https://example.com/images/blue-shoes-side.webp</image:loc>
      <image:caption>Side profile of blue running shoes Model X</image:caption>
    </image:image>
  </url>
</urlset>
```

**When to use image sitemaps:**
- E-commerce sites with product photography
- Sites using JavaScript to load images (not in initial HTML)
- Image-heavy portfolios or galleries
- Sites where images are on a CDN subdomain

Up to 1,000 `<image:image>` entries per `<url>`.

### Video Sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
    <loc>https://example.com/videos/product-demo</loc>
    <video:video>
      <video:thumbnail_loc>https://example.com/thumbs/demo.jpg</video:thumbnail_loc>
      <video:title>Product Demo - Model X Running Shoes</video:title>
      <video:description>Watch a 2-minute demo of Model X features including cushioning and grip.</video:description>
      <video:content_loc>https://example.com/video/demo.mp4</video:content_loc>
      <video:duration>120</video:duration>
      <video:publication_date>2026-03-15</video:publication_date>
    </video:video>
  </url>
</urlset>
```

**Required fields**: `thumbnail_loc`, `title`, `description`, and either `content_loc` or `player_loc`.

**When to use video sitemaps:**
- Sites hosting their own videos (not just YouTube embeds)
- Product demo pages, tutorial sites, course platforms
- Sites wanting video rich results in Google Search

### News Sitemap

For Google News publishers only. Articles must be less than 2 days old.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  <url>
    <loc>https://example.com/news/breaking-story</loc>
    <news:news>
      <news:publication>
        <news:name>Example News</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>2026-04-11T08:00:00+00:00</news:publication_date>
      <news:title>Breaking: Major Industry Development</news:title>
    </news:news>
  </url>
</urlset>
```

**News sitemap rules:**
- Only include articles published in the last 48 hours
- Regenerate every 15 minutes during publishing hours
- Maximum 1,000 URLs per news sitemap
- Must be registered as a Google News source

---

## Safe Programmatic Pages (OK at scale)

These page types can safely generate large URL counts:

- Integration pages (with real setup docs)
- Template/tool pages (with downloadable content)
- Glossary pages (200+ word definitions)
- Product pages (unique specs, reviews)
- User profile pages (user-generated content)

## Penalty Risk (avoid at scale)

- Location pages with only city name swapped
- "Best [tool] for [industry]" without industry-specific value
- "[Competitor] alternative" without real comparison data
- AI-generated pages without human review and unique value

---

## Industry-Specific Sitemap Templates

### E-commerce

```
sitemap_index.xml
  sitemap-categories.xml     -- all category and subcategory pages
  sitemap-products.xml       -- all product pages (split if > 50k)
  sitemap-brands.xml         -- brand landing pages
  sitemap-blog.xml           -- buying guides, reviews, how-tos
  sitemap-images.xml         -- product photography
```

### SaaS / B2B

```
sitemap_index.xml
  sitemap-pages.xml          -- landing pages, features, pricing
  sitemap-blog.xml           -- content marketing articles
  sitemap-integrations.xml   -- integration pages
  sitemap-docs.xml           -- documentation / help center
  sitemap-comparisons.xml    -- vs pages, alternatives pages
```

### Publisher / News

```
sitemap_index.xml
  sitemap-news.xml           -- last 48h articles (news extension)
  sitemap-articles.xml       -- evergreen articles archive
  sitemap-authors.xml        -- author profile pages
  sitemap-categories.xml     -- topic/section pages
  sitemap-videos.xml         -- video content
```

### Local Business (multi-location)

```
sitemap_index.xml
  sitemap-pages.xml          -- main pages, about, services
  sitemap-locations.xml      -- individual location pages (only if unique content)
  sitemap-blog.xml           -- local content, guides
  sitemap-services.xml       -- service-specific landing pages
```

---

## Output

### For Analysis
- `VALIDATION-REPORT.md` -- analysis results with severity-sorted issues
- Crawl data discrepancy table (if SF data available)
- Recommendations with specific fix actions

### For Generation
- `sitemap.xml` or `sitemap_index.xml` (with child sitemaps)
- `STRUCTURE.md` -- site architecture documentation
- URL count and organization summary
- Lastmod cadence recommendations per content type
