---
name: 42-blog
description: >
  Unified blog audit covering on-page SEO, AI citation optimization, and
  Article/BlogPosting schema generation. Submodes: --seo, --geo, --schema, --all.
  Use when user says "blog audit", "blog SEO", "blog check", "article schema",
  "blog optimization".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
version: 2.0.0
tags: [blog, seo, geo, schema, content]
---

# 42-blog -- Unified Blog Audit

Comprehensive blog audit combining on-page SEO validation, AI citation
optimization, and JSON-LD schema generation into a single consolidated report.

## Usage

```
/42:blog --seo <url|file>      On-page SEO checklist
/42:blog --geo <url|file>      AI citation optimization audit
/42:blog --schema <url|file>   Blog JSON-LD generation
/42:blog --all <url|file>      All three modes (default)
```

When no flag is provided, run all three modes (`--all`).

---

## Step 1: Read Content (All Modes)

Read the target file or fetch the URL with WebFetch and extract everything
needed across all three modes:

- **Frontmatter** -- title, description, date, lastUpdated, author, tags,
  canonical, og:image, slug/URL
- **Heading structure** -- H1, H2, H3 hierarchy with full text
- **Body content** -- Full text, word count, individual paragraph word counts
- **Links** -- All internal and external links with anchor text
- **Meta tags** -- OG tags, Twitter Card tags, canonical URL
- **FAQ sections** -- Question-answer pairs
- **Schema markup** -- Existing JSON-LD, microdata, RDFa
- **Images** -- Cover image URL, dimensions, alt text; inline images
- **Content patterns** -- TL;DR boxes, comparison tables, ordered lists,
  definition formatting, citation capsules
- **Technical** -- robots.txt directives, static HTML check, page size
- **Author info** -- Name, job title, social links, credentials, organization

Use Grep and Glob to scan the project for related blog content (bidirectional
link checks, organization defaults, author data).

---

# MODE: --seo (On-Page SEO Checklist)

## SEO-1: Title Tag Validation

| Check | Pass Criteria |
|-------|---------------|
| Character count | 40-60 characters (no truncation in SERPs) |
| Keyword placement | Primary keyword in first half of title |
| Power word | Contains at least one power word (Guide, Best, How, Why, Essential, Proven, Complete) |
| Truncation risk | No critical meaning lost if truncated at 60 chars |
| Uniqueness | Not generic -- specific to the content |

## SEO-2: Meta Description

| Check | Pass Criteria |
|-------|---------------|
| Character count | 150-160 characters |
| Statistic included | Contains at least one specific number or data point |
| Value proposition | Ends with clear reader benefit or value proposition |
| Keyword presence | Primary keyword appears naturally (not stuffed) |
| No keyword stuffing | Keyword appears at most once |
| Call to action | Implies action (learn, discover, find out, see) |

## SEO-3: Heading Hierarchy

| Check | Pass Criteria |
|-------|---------------|
| Single H1 | Exactly one H1 tag (the title) |
| No skipped levels | H1 -> H2 -> H3, never H1 -> H3 or H2 -> H4 |
| Keyword in headings | Primary keyword in 2-3 headings (natural, not forced) |
| Question format | 60-70% of H2 headings are questions |
| H2 count | 6-8 H2 sections for a standard blog post |
| Heading length | Each heading under 70 characters |

## SEO-4: Internal Links

| Check | Pass Criteria |
|-------|---------------|
| Link count | 3-10 internal links per post |
| Anchor text | Descriptive (not "click here" or "read more") |
| Bidirectional | Check if linked pages also link back (flag if not) |
| No orphan status | Post links to at least 3 other pages on the site |
| Link distribution | Links spread across the post, not clustered |
| No self-links | Post does not link to itself |

Use Grep and Glob to scan the project for existing blog content and verify
bidirectional linking where possible.

## SEO-4.5: Link Deduplication

| Check | Pass Criteria |
|-------|---------------|
| No duplicate URLs | Each URL appears at most once in body content |
| Best instance kept | If duplicates exist, keep the one with most descriptive anchor text |
| Navigation exempt | Header/footer nav links don't count toward body dedup |
| Fragment normalization | URLs with different #fragments treated as same URL |

For each duplicate found:
1. Normalize URLs (strip trailing slashes, query parameters, fragments)
2. Score each instance by anchor text descriptiveness (keyword-rich > generic)
3. Recommend keeping the highest-scored instance, removing others
4. Deduct 1 point per duplicate from SEO Optimization score

Google records 1-2 anchor texts per URL per page (Zyppy 2023). Optimal: link to
same URL once in body content; 5-10 internal links per 2,000 words; max ~50
total links per page.

## SEO-5: External Links

| Check | Pass Criteria |
|-------|---------------|
| Source tier | Links to tier 1-3 sources only (authoritative, not SEO blogs) |
| Broken links | Use WebFetch to verify top external links are reachable |
| Rel attributes | External links have appropriate rel attributes (nofollow for sponsored/UGC) |
| Link count | At least 3 external links to authoritative sources |
| No competitor links | Not linking to direct competitors unnecessarily |

## SEO-6: Canonical URL

| Check | Pass Criteria |
|-------|---------------|
| Present | Canonical URL is defined in frontmatter or meta tags |
| Correct format | Full absolute URL (https://domain.com/path) |
| Trailing slash | Consistent with site convention (no mixed trailing slashes) |
| Self-referencing | Canonical points to the page itself (unless intentional cross-domain) |

## SEO-7: OG Meta Tags

| Check | Pass Criteria |
|-------|---------------|
| og:title | Present, matches or complements the title tag |
| og:description | Present, 150-160 characters, compelling for social sharing |
| og:image | Present, 1200x630 minimum dimensions, absolute URL |
| og:type | Set to "article" for blog posts |
| og:url | Present, matches canonical URL |
| og:site_name | Present, matches site/brand name |

## SEO-8: Twitter Card

| Check | Pass Criteria |
|-------|---------------|
| twitter:card | Set to "summary_large_image" for blog posts |
| twitter:title | Present, under 70 characters |
| twitter:description | Present, under 200 characters |
| twitter:image | Present, same as or similar to og:image |
| twitter:site | Present if the site has a Twitter/X account |

## SEO-9: URL Structure

| Check | Pass Criteria |
|-------|---------------|
| Length | Short -- under 75 characters for the path portion |
| Keyword presence | Primary keyword or close variant in the URL slug |
| No dates | URL does not contain /2025/ or /2026/ date segments |
| No special characters | Only lowercase letters, numbers, and hyphens |
| Lowercase | Entire URL path is lowercase |
| No stop words | Minimal use of "the", "a", "and", "of" in slug |
| No file extension | No .html or .php in the URL (clean URLs) |

---

# MODE: --geo (AI Citation Optimization)

Reference benchmarks throughout this mode:
- Only 12% of sources cited match across ChatGPT, Perplexity, and AI Overviews
- 80% of LLM citations don't rank in Google's top 100
- Brands 6.5x more likely cited through third-party sources
- 120-180 word sections get 70% more ChatGPT citations
- Comparison tables with `<thead>` achieve 47% higher AI citation rates
- Content freshness: 76.4% of top citations updated within 30 days

## GEO-1: Passage-Level Citability (4 pts)

Check each section between headings for AI-extractable passages:

| Check | Criteria |
|-------|----------|
| Word count | Each section contains 120-180 word self-contained passages |
| Context independence | Each passage makes sense extracted from surrounding context |
| Claim structure | Passages contain: specific claim + supporting evidence + source attribution |
| Completeness | Passage answers a question without requiring reader to read adjacent sections |

**Scoring:**
- 4 pts: 80%+ sections have citable passages
- 3 pts: 60-79%
- 2 pts: 40-59%
- 1 pt: 20-39%
- 0 pts: <20%

## GEO-2: Q&A Formatting (3 pts)

| Check | Criteria |
|-------|----------|
| Question headings | 60-70% of H2s are phrased as questions |
| Answer-first format | Opening paragraph under each H2 provides a direct answer |
| FAQ section | Dedicated FAQ section with structured question-answer pairs |

**Scoring:**
- 3 pts: All three criteria met
- 2 pts: Two criteria met
- 1 pt: One criterion met
- 0 pts: None met

## GEO-3: Entity Clarity (3 pts)

| Check | Criteria |
|-------|----------|
| Canonical topic | One unambiguous primary topic per page |
| Consistent naming | Same entity name used throughout (no confusing synonyms) |
| Intro statement | Clear topic statement in the introduction paragraph |
| Title-content match | Title accurately reflects the content focus |

**Scoring:**
- 3 pts: All four criteria met
- 2 pts: Three criteria met
- 1 pt: One or two criteria met
- 0 pts: None met

## GEO-4: Content Structure for Extraction (3 pts)

| Check | Criteria |
|-------|----------|
| TL;DR box | 40-60 word standalone summary present at top |
| Comparison tables | Tables with proper HTML `<thead>` (47% higher citation rate) |
| Ordered lists | Numbered lists for processes and step-by-step instructions |
| Definition formatting | Key terms formatted with clear definition patterns |
| Citation capsules | 40-60 word definitive statements in each major section |

**Scoring:**
- 3 pts: 4-5 elements present
- 2 pts: 3 elements present
- 1 pt: 1-2 elements present
- 0 pts: None present

## GEO-5: AI Crawler Accessibility (2 pts)

| Check | Criteria |
|-------|----------|
| Static HTML | Content rendered in static HTML, not behind JavaScript |
| robots.txt | Allows AI crawlers: GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot |
| Schema in HTML | Schema markup in static HTML, not JS-injected |
| Page size | Reasonable page size within AI crawler limits |

**Scoring:**
- 2 pts: All criteria met
- 1 pt: Most criteria met but one issue
- 0 pts: Multiple issues blocking AI crawlers

## GEO-6: E-E-A-T Author Signals

Cross-reference with the E-E-A-T framework (`${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md`).
E-E-A-T now applies to ALL competitive queries (December 2025 core update).

| Check | Criteria |
|-------|----------|
| Author byline | Visible author name with credentials |
| Author bio | Bio with relevant experience, credentials, social links |
| Experience signals | First-person narrative, original photos, specific examples |
| Expertise signals | Technical accuracy, specialized vocabulary, up-to-date claims |
| ProfilePage schema | Author profile page with Person schema and sameAs links |

Flag missing E-E-A-T signals as high-priority fixes -- anonymous or generic
authorship is penalized even for non-YMYL content since December 2025.

## GEO-7: Platform-Specific Analysis

Evaluate the post for each AI platform's citation preferences:

**ChatGPT:**
- Favors "Best X" listicles (43.8% of citations)
- Prefers well-cited, authoritative content
- Recency matters -- recent updates get priority
- Domain authority influences citation likelihood

**Perplexity:**
- Favors Reddit sources (6.6% of all citations)
- Rapid content decay: 2-3 day citation window
- Freshness is the most critical factor
- Community-validated content preferred

**Google AI Overviews:**
- Favors Google properties (23% of citations)
- High Domain Rating strongly correlated with citation
- Present in 49% of SERPs
- Prefers content that already ranks well organically

For each platform provide: current citability rating (High/Medium/Low), specific
improvements, and content format recommendations.

## GEO-8: Generate Citation Capsules

For each H2 section, write a citation capsule:
- **Length**: 40-60 words, self-contained
- **Structure**: Specific claim + data point + source attribution
- **Purpose**: A passage AI could directly quote as a citation
- **Format**: Present as a suggested addition the author can embed

Example:
```
According to [Source], [specific claim with number]. This represents
[context/comparison], making it [significance]. [Supporting detail
that reinforces the claim].
```

Generate one capsule per H2 section. Label each with the section heading it
belongs under.

## GEO-9: Calculate AI Citation Readiness Score (0-100)

Map the 15-point subcategory scores to a 0-100 display score:

| Category | Raw Points | Display Weight | Max Display Score |
|----------|-----------|----------------|-------------------|
| Passage-Level Citability | /4 | x6.75 | 27 |
| Q&A Formatting | /3 | x6.67 | 20 |
| Entity Clarity | /3 | x6.67 | 20 |
| Content Structure | /3 | x6.67 | 20 |
| AI Crawler Accessibility | /2 | x6.5 | 13 |
| **Total** | **/15** | | **100** |

Rating thresholds:
- 90-100: Excellent -- highly citable by AI systems
- 70-89: Good -- citable with minor improvements
- 50-69: Needs Work -- significant gaps in citability
- Below 50: Poor -- major restructuring needed

---

# MODE: --schema (Blog JSON-LD Generation)

Reference `${CLAUDE_PLUGIN_ROOT}/skills/references/schema-types.md` for current type status. Always
use JSON-LD format. Content with proper schema has ~2.5x higher chance of
appearing in AI-generated answers.

## SCHEMA-1: Generate BlogPosting

```json
{
  "@type": "BlogPosting",
  "@id": "{siteUrl}/blog/{slug}#article",
  "headline": "Post title (max 110 chars)",
  "description": "Meta description (150-160 chars)",
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "author": { "@id": "{siteUrl}/author/{author-slug}#person" },
  "publisher": { "@id": "{siteUrl}#organization" },
  "image": { "@id": "{siteUrl}/blog/{slug}#primaryimage" },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{siteUrl}/blog/{slug}"
  },
  "wordCount": 2400,
  "articleBody": "First 200 characters of content as excerpt..."
}
```

Required: @type, headline, datePublished, author, publisher, image.
Recommended: description, dateModified, mainEntityOfPage, wordCount, articleBody.

## SCHEMA-2: Generate Person

Author schema with stable @id for cross-referencing. Include E-E-A-T signals
(see `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md`):

```json
{
  "@type": "Person",
  "@id": "{siteUrl}/author/{author-slug}#person",
  "name": "Author Name",
  "jobTitle": "Role or Title",
  "url": "{siteUrl}/author/{author-slug}",
  "sameAs": [
    "https://twitter.com/handle",
    "https://linkedin.com/in/handle",
    "https://github.com/handle"
  ]
}
```

Optional (include when available): `alumniOf`, `worksFor` (reference
Organization @id if same entity).

## SCHEMA-3: Generate Organization

```json
{
  "@type": "Organization",
  "@id": "{siteUrl}#organization",
  "name": "Organization Name",
  "url": "{siteUrl}",
  "logo": {
    "@type": "ImageObject",
    "url": "{siteUrl}/logo.png",
    "width": 600,
    "height": 60
  },
  "sameAs": [
    "https://twitter.com/org",
    "https://linkedin.com/company/org",
    "https://github.com/org"
  ]
}
```

Logo: 112x112px minimum, 600px wide maximum. Rectangular logos preferred for
BlogPosting publishers.

## SCHEMA-4: Generate BreadcrumbList

```json
{
  "@type": "BreadcrumbList",
  "@id": "{siteUrl}/blog/{slug}#breadcrumb",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "{siteUrl}" },
    { "@type": "ListItem", "position": 2, "name": "Category Name", "item": "{siteUrl}/blog/category/{category-slug}" },
    { "@type": "ListItem", "position": 3, "name": "Post Title", "item": "{siteUrl}/blog/{slug}" }
  ]
}
```

If no category is available, use "Blog" as the second item with `{siteUrl}/blog`.

## SCHEMA-5: Generate FAQPage

Extract Q&A pairs from the blog post's FAQ section:

```json
{
  "@type": "FAQPage",
  "@id": "{siteUrl}/blog/{slug}#faq",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The complete answer text (40-60 words with statistic)."
      }
    }
  ]
}
```

**Important:** Google restricted FAQ rich results to government and health sites
(August 2023). However, FAQPage schema still provides value because:
- AI systems (ChatGPT, Perplexity, Gemini) extract FAQ data for citations
- It structures content for future rich result eligibility changes
- It improves content organization signals

Only generate if the post contains an FAQ section with at least 2 questions.

## SCHEMA-6: Generate ImageObject

```json
{
  "@type": "ImageObject",
  "@id": "{siteUrl}/blog/{slug}#primaryimage",
  "url": "https://cdn.example.com/image.jpg",
  "width": 1200,
  "height": 630,
  "caption": "Descriptive caption matching alt text"
}
```

Image requirements: URL must be crawlable, width/height must reflect actual
dimensions, caption should match alt text. Preferred: 1200x630 or 1920x1080.

## SCHEMA-7: Validate and Warn

**NEVER use these deprecated types:**
- HowTo -- Deprecated September 2023
- SpecialAnnouncement -- Deprecated July 2025
- Practice Problem -- Deprecated (education)
- Dataset -- Deprecated for general use
- Sitelinks Search Box -- Deprecated
- Q&A -- Deprecated January 2026 (distinct from FAQPage)

**Validation checks:**
1. All @id references resolve to entities within the @graph
2. dateModified >= datePublished
3. headline <= 110 characters
4. description between 50-160 characters
5. All URLs are absolute (not relative)
6. Image dimensions are positive integers
7. BreadcrumbList positions are sequential starting from 1
8. FAQPage has at least 2 questions (if included)

Pages using 3+ schema types have ~13% higher AI citation likelihood. This skill
generates up to 6 types (BlogPosting, Person, Organization, BreadcrumbList,
FAQPage, ImageObject) to maximize both search engine understanding and AI
extraction.

## SCHEMA-8: Output Combined @graph

Combine all schemas into a single `<script>` tag:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "BlogPosting", ... },
    { "@type": "Person", ... },
    { "@type": "Organization", ... },
    { "@type": "BreadcrumbList", ... },
    { "@type": "FAQPage", ... },
    { "@type": "ImageObject", ... }
  ]
}
</script>
```

**@graph pattern benefits:**
- Single script tag -- cleaner HTML
- Entity linking via stable @id references
- Google and AI systems parse @graph arrays correctly
- Easier to maintain as a single block

**Output options:**
- **Embedded HTML** -- Ready to paste into `<head>` or before `</body>`
- **Standalone JSON** -- For CMS schema fields or API injection
- **MDX component** -- If the project uses MDX, wrap in a component

---

# Report Generation

## Consolidated Report Format

Output a single consolidated report with clearly labeled sections per mode.
Only include sections for modes that were requested.

```
# Blog Audit Report: [Title]

**URL/File**: [path or URL]
**Date**: [audit date]
**Modes**: [--seo, --geo, --schema, or --all]

---

## SEO Validation (--seo)

**Overall**: [X/Y checks passed] -- [PASS / NEEDS WORK / FAIL]

### Results

| # | Check | Status | Details | Fix |
|---|-------|--------|---------|-----|
| 1 | Title length | PASS | 52 chars | - |
| 2 | Title keyword | PASS | "keyword" in first half | - |
| 3 | Title power word | FAIL | No power word found | Add "Guide" or "Complete" |
| ... | ... | ... | ... | ... |

### Priority SEO Fixes
1. [Most impactful fix]
2. [Second most impactful]
3. [Third most impactful]

---

## AI Citation Readiness (--geo)

**AI Citation Readiness Score: [X]/100** -- [Rating]

### Score Breakdown
| Category | Raw | Display | Max |
|----------|-----|---------|-----|
| Passage-Level Citability | X/4 | X | 27 |
| Q&A Formatting | X/3 | X | 20 |
| Entity Clarity | X/3 | X | 20 |
| Content Structure | X/3 | X | 20 |
| AI Crawler Accessibility | X/2 | X | 13 |
| **Total** | **X/15** | **X** | **100** |

### Per-Section Citability
| Section (H2) | Word Count | Self-Contained | Claim+Evidence | Citable |
|---------------|-----------|----------------|----------------|---------|
| [heading] | [N] | Yes/No | Yes/No | Yes/No |

### E-E-A-T Author Signals
| Signal | Status | Recommendation |
|--------|--------|----------------|
| Author byline | [status] | [recommendation] |
| Author bio | [status] | [recommendation] |
| Experience signals | [status] | [recommendation] |
| ProfilePage schema | [status] | [recommendation] |

### Platform-Specific Optimization
#### ChatGPT
- Citability: [High/Medium/Low]
- [specific recommendations]

#### Perplexity
- Citability: [High/Medium/Low]
- [specific recommendations]

#### Google AI Overviews
- Citability: [High/Medium/Low]
- [specific recommendations]

### Generated Citation Capsules

#### [H2 Section 1]
> [40-60 word citation capsule]

#### [H2 Section 2]
> [40-60 word citation capsule]

### Priority GEO Fixes
1. [Most impactful improvement]
2. [Second most impactful]
3. [Third most impactful]

---

## JSON-LD Schema (--schema)

### Validation Results
| Check | Status | Details |
|-------|--------|---------|
| @id references resolve | PASS/FAIL | [details] |
| dateModified >= datePublished | PASS/FAIL | [details] |
| headline length | PASS/FAIL | [X chars] |
| ... | ... | ... |

### Deprecated Type Warnings
- [Any deprecated types found in existing markup]

### Generated Schema
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [...]
}
</script>

---

## Combined Priority Actions

1. [Highest-impact action across all modes]
2. [Second highest]
3. [Third highest]
4. [Fourth highest]
5. [Fifth highest]

### Notes
- [Cross-mode observations, e.g., schema improvements that also boost GEO]
- [Any issues not captured by individual checks]
```

### Status Values

- **PASS** -- Meets the criteria
- **FAIL** -- Does not meet the criteria, fix provided
- **WARN** -- Partially meets criteria or edge case, recommendation provided
- **N/A** -- Not applicable (e.g., no Twitter Card if site has no X account)

### Cross-Mode Synergies

When running `--all`, highlight synergies between modes:
- FAQ schema (--schema) improves Q&A Formatting score (--geo)
- Question-format H2s (--seo heading check) improve AI citability (--geo)
- Author Person schema (--schema) strengthens E-E-A-T signals (--geo)
- OG meta tags (--seo) provide fallback data for schema generation (--schema)
- Internal linking quality (--seo) affects domain authority and AI citation
  likelihood (--geo)
