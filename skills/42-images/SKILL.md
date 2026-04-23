---
name: 42-images
version: 2.0.0
description: >
  Image optimization analysis for SEO and performance. Checks alt text, file
  sizes, formats, responsive images, lazy loading, and CLS prevention. Supports
  batch analysis from Screaming Frog CSV exports, CDN optimization, and AI image
  SEO. Use when user says "image optimization", "alt text", "image SEO",
  "image size", or "image audit".
---

# Image Optimization Analysis

## Checks

### Alt Text
- Present on all `<img>` elements (except decorative: `role="presentation"`)
- Descriptive: describes the image content, not "image.jpg" or "photo"
- Includes relevant keywords where natural, not keyword-stuffed
- Length: 10-125 characters

**Good examples:**
- "Professional plumber repairing kitchen sink faucet"
- "Red 2024 Toyota Camry sedan front view"
- "Team meeting in modern office conference room"

**Bad examples:**
- "image.jpg" (filename, not description)
- "plumber plumbing plumber services" (keyword stuffing)
- "Click here" (not descriptive)

### File Size

**Tiered thresholds by image category:**

| Image Category | Target | Warning | Critical |
|----------------|--------|---------|----------|
| Thumbnails | < 50KB | > 100KB | > 200KB |
| Content images | < 100KB | > 200KB | > 500KB |
| Hero/banner images | < 200KB | > 300KB | > 700KB |

Recommend compression to target thresholds where possible without quality loss.

### Format
| Format | Browser Support | Use Case |
|--------|-----------------|----------|
| WebP | 97%+ | Default recommendation |
| AVIF | 92%+ | Best compression, newer |
| JPEG | 100% | Fallback for photos |
| PNG | 100% | Graphics with transparency |
| SVG | 100% | Icons, logos, illustrations |

Recommend WebP/AVIF over JPEG/PNG. Check for `<picture>` element with format fallbacks.

#### Recommended `<picture>` Element Pattern

Use progressive enhancement with the most efficient format first:

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Descriptive alt text" width="800" height="600" loading="lazy" decoding="async">
</picture>
```

The browser will use the first supported format. Current browser support: AVIF 93.8%, WebP 95.3%.

#### JPEG XL -- Emerging Format

In November 2025, Google's Chromium team reversed its 2022 decision and announced it will restore JPEG XL support in Chrome using a Rust-based decoder. The implementation is feature-complete but not yet in Chrome stable. JPEG XL offers lossless JPEG recompression (~20% savings with zero quality loss) and competitive lossy compression. Not yet practical for web deployment, but worth monitoring for future adoption.

### Responsive Images
- `srcset` attribute for multiple sizes
- `sizes` attribute matching layout breakpoints
- Appropriate resolution for device pixel ratios

```html
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Description"
>
```

### Lazy Loading
- `loading="lazy"` on below-fold images
- Do NOT lazy-load above-fold/hero images (hurts LCP)
- Check for native vs JavaScript-based lazy loading

```html
<!-- Below fold - lazy load -->
<img src="photo.jpg" loading="lazy" alt="Description">

<!-- Above fold - eager load (default) -->
<img src="hero.jpg" alt="Hero image">
```

### `fetchpriority="high"` for LCP Images

Add `fetchpriority="high"` to your hero/LCP image to prioritize its download in the browser's network queue:

```html
<img src="hero.webp" fetchpriority="high" alt="Hero image description" width="1200" height="630">
```

**Critical:** Do NOT lazy-load above-the-fold/LCP images. Using `loading="lazy"` on LCP images directly harms LCP scores. Reserve `loading="lazy"` for below-the-fold images only.

### `decoding="async"` for Non-LCP Images

Add `decoding="async"` to non-LCP images to prevent image decoding from blocking the main thread:

```html
<img src="photo.webp" alt="Description" width="600" height="400" loading="lazy" decoding="async">
```

### CLS Prevention
- `width` and `height` attributes set on all `<img>` elements
- `aspect-ratio` CSS as alternative
- Flag images without dimensions

```html
<!-- Good - dimensions set -->
<img src="photo.jpg" width="800" height="600" alt="Description">

<!-- Good - CSS aspect ratio -->
<img src="photo.jpg" style="aspect-ratio: 4/3" alt="Description">

<!-- Bad - no dimensions -->
<img src="photo.jpg" alt="Description">
```

### File Names
- Descriptive: `blue-running-shoes.webp` not `IMG_1234.jpg`
- Hyphenated, lowercase, no special characters
- Include relevant keywords

### CDN Usage
- Check if images served from CDN (different domain, CDN headers)
- Recommend CDN for image-heavy sites
- Check for edge caching headers

---

## Batch Analysis from Screaming Frog

When the user provides a Screaming Frog CSV export from the **Images tab**, use it for bulk analysis instead of crawling page-by-page.

### How to Use SF Image Export

1. **Expected file**: CSV exported from Screaming Frog > Images tab (or Internal > Images)
2. **Key columns to parse**:
   - `Address` -- the image URL
   - `Alt Text` -- current alt text (empty = missing)
   - `Size (Bytes)` -- file size for threshold checks
   - `Status Code` -- flag non-200 images (broken images)
   - `Type` -- image MIME type (check for non-WebP/AVIF)
   - `Width` / `Height` -- dimensions (0 or empty = missing dimensions)
   - `Found At` -- which pages reference this image
   - `Missing Alt Text` -- pre-flagged by SF

3. **Batch analysis workflow**:
   - Read the CSV with the Read tool
   - Group images by issue type: missing alt text, oversized, wrong format, missing dimensions, broken (non-200)
   - Calculate total potential savings (sum of oversized images minus target sizes)
   - Cross-reference `Found At` to identify which pages have the most image issues
   - Produce prioritized report sorted by page impact (pages with most issues first)

4. **Output additions for batch mode**:
   - Total images analyzed count
   - Breakdown by issue type with counts and percentages
   - Top 10 worst offenders (largest files, most missing alt texts per page)
   - Estimated total savings from format conversion and compression

---

## CDN Optimization Recommendations

When images are not served from a CDN, or when CDN configuration can be improved, recommend one of these approaches:

### Cloudinary

Best for: sites needing automatic format negotiation and responsive image transforms.

- **Auto-format**: Use `f_auto` to serve WebP/AVIF automatically based on browser support
- **Auto-quality**: Use `q_auto` for perceptual quality optimization
- **Responsive breakpoints**: Use the responsive breakpoints API to generate optimal srcset widths
- **URL pattern**: `https://res.cloudinary.com/{cloud}/image/upload/f_auto,q_auto,w_800/{image_id}`
- **Lazy transformations**: Images are transformed on first request and cached at the edge

### Imgix

Best for: sites needing real-time image processing with fine-grained control.

- **Auto-format**: Use `auto=format` parameter
- **Responsive**: Use `srcset` generation via client libraries or URL API
- **URL pattern**: `https://{source}.imgix.net/{path}?auto=format,compress&w=800`
- **Purge API**: Instant cache invalidation when source images change

### AWS CloudFront + S3

Best for: sites already on AWS that need cost-effective global distribution.

- **Origin**: S3 bucket with original images
- **Lambda@Edge or CloudFront Functions**: Auto-convert to WebP/AVIF on the fly based on `Accept` header
- **Cache policy**: Set long TTLs (1 year) with versioned filenames for instant invalidation
- **Recommended setup**: Use `image-handler` solution (AWS-provided) for on-the-fly resizing and format conversion

### CDN Checklist

| Check | What to Verify |
|-------|---------------|
| Cache headers | `Cache-Control: max-age=31536000, immutable` for versioned assets |
| Content negotiation | CDN serves WebP/AVIF based on `Accept` header |
| Compression | Brotli or gzip for SVG; skip for already-compressed formats |
| Geographic coverage | Edge nodes in markets where the site's audience lives |
| Invalidation | Ability to purge specific URLs or by tag/prefix |

---

## AI Image SEO

### Structured Data for Product Images

For e-commerce and product pages, add `ImageObject` schema to help search engines and AI systems understand image context:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Blue Running Shoes Model X",
  "image": [
    {
      "@type": "ImageObject",
      "url": "https://example.com/images/blue-running-shoes-front.webp",
      "caption": "Front view of Blue Running Shoes Model X",
      "width": 1200,
      "height": 800,
      "encodingFormat": "image/webp"
    },
    {
      "@type": "ImageObject",
      "url": "https://example.com/images/blue-running-shoes-side.webp",
      "caption": "Side profile showing cushioned sole of Model X",
      "width": 1200,
      "height": 800,
      "encodingFormat": "image/webp"
    }
  ]
}
```

### Figure Captions for AI Understanding

Use `<figure>` and `<figcaption>` to provide context that both users and AI systems can parse:

```html
<figure>
  <picture>
    <source srcset="chart-conversion-rates.avif" type="image/avif">
    <source srcset="chart-conversion-rates.webp" type="image/webp">
    <img src="chart-conversion-rates.png" alt="Bar chart comparing conversion rates across 5 landing page variants" width="900" height="500" loading="lazy" decoding="async">
  </picture>
  <figcaption>Conversion rates by landing page variant (Q1 2026). Variant C outperformed control by 34%.</figcaption>
</figure>
```

**Why this matters for AI**: LLMs and multimodal models use `figcaption` text as primary context for understanding what an image shows. A descriptive caption significantly increases the chance that AI systems cite your visual content correctly.

### AI Image Optimization Checklist

| Signal | Implementation |
|--------|---------------|
| Alt text | Descriptive, keyword-relevant, 10-125 characters |
| Figcaption | Contextual caption explaining significance, not just restating alt text |
| ImageObject schema | `caption`, `url`, `width`, `height`, `encodingFormat` properties |
| Open Graph image | `og:image` with proper dimensions for social and AI preview cards |
| Image sitemap | Include images in XML sitemap with `<image:caption>` tags |

---

## Cross-Reference

For deeper image performance optimization (LCP impact, render-blocking analysis, Core Web Vitals), see `${CLAUDE_PLUGIN_ROOT}/skills/references/web-quality/performance/SKILL.md`.

---

## Output

### Image Audit Summary

| Metric | Status | Count |
|--------|--------|-------|
| Total Images | - | XX |
| Missing Alt Text | X | XX |
| Oversized (>200KB) | ! | XX |
| Wrong Format | ! | XX |
| No Dimensions | ! | XX |
| Not Lazy Loaded | ! | XX |

### Prioritized Optimization List

Sorted by file size impact (largest savings first):

| Image | Current Size | Format | Issues | Est. Savings |
|-------|--------------|--------|--------|--------------|
| ... | ... | ... | ... | ... |

### Recommendations
1. Convert X images to WebP format (est. XX KB savings)
2. Add alt text to X images
3. Add dimensions to X images
4. Enable lazy loading on X below-fold images
5. Compress X oversized images
6. Add `<figcaption>` to key content images for AI understanding
7. Add ImageObject schema to product images
8. Configure CDN auto-format negotiation (if not already in place)
