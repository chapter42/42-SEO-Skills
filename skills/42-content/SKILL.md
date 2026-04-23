---
name: 42-content
description: >
  Unified content quality audit with dual SEO/GEO scoring. Evaluates E-E-A-T signals,
  readability, keyword optimization, passage-level AI extractability, entity consistency,
  and citation-worthiness. References eeat-framework.md and quality-gates.md.
  Use when user says "content quality", "content audit", "E-E-A-T", "content analysis",
  "is my content good", "AI citability", "passage optimization".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
version: 2.0.0
tags: [content, seo, geo, eeat, readability, citability]
---

# Unified Content Quality Audit — Dual SEO/GEO Scoring

## Purpose

Content quality determines both Google rankings and AI citation likelihood. This skill audits content through two complementary scoring dimensions:

- **SEO Content Score (0-100):** Keyword optimization, readability, E-E-A-T signals, content structure, internal/external link quality
- **GEO Content Score (0-100):** Passage-level AI extractability, E-E-A-T signals, entity consistency, passage quality, content freshness

E-E-A-T is the shared foundation scored in both dimensions. Default mode (`--full`) reports both scores side by side.

---

## Commands

```
/42:content --full <url>   # Both SEO and GEO scoring (default)
/42:content --seo <url>    # Traditional content quality — keyword focus, readability, length, E-E-A-T
/42:content --geo <url>    # AI citability — passage structure, entity clarity, extractability, brand signals
/42:content <url>          # Same as --full
```

---

## Mode Behavior

| Aspect | `--full` (default) | `--seo` | `--geo` |
|--------|-------------------|---------|---------|
| E-E-A-T scoring | Full (shared) | Full (shared) | Full (shared) |
| Keyword optimization | Yes | Yes (prominent) | Context note only |
| Readability scores | Yes | Yes (prominent) | Yes |
| Content length vs. competitors | Yes | Yes | Minimal |
| Internal/external link quality | Yes | Yes (prominent) | Minimal |
| Passage-level extractability | Yes | Minimal | Yes (prominent) |
| Entity density and consistency | Yes | Minimal | Yes (prominent) |
| Answer-first structure (BLUF) | Yes | Minimal | Yes (prominent) |
| Citation-worthiness signals | Yes | Minimal | Yes (prominent) |
| Content freshness | Yes | Yes | Yes (weighted heavier) |
| Dual score table | Both columns | SEO column only | GEO column only |

---

## How to Use This Skill

1. Fetch the target page(s) using WebFetch
2. Score E-E-A-T across the 4 dimensions (shared foundation)
3. Run SEO-specific checks (keywords, readability, links, multimedia)
4. Run GEO-specific checks (passage extractability, entities, BLUF, citation signals)
5. Assess content freshness per `references/quality-gates.md` thresholds
6. Calculate dual scores and generate the output report

---

## Part 1: E-E-A-T Assessment (Shared Foundation)

Reference: `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md` — December 2025 E-E-A-T update (now ALL queries, not just YMYL).

E-E-A-T is scored identically in both dimensions. The weights below reflect the eeat-framework.md canonical weights:

| Dimension | Weight | Focus |
|-----------|--------|-------|
| Experience | 20% | First-person narrative, original photos, process documentation, case studies with specific results |
| Expertise | 25% | Author credentials, technical depth, methodology, data-backed claims, specialized terminology |
| Authoritativeness | 25% | Citations by others, backlinks from authoritative sources, media mentions, brand recognition, Wikipedia |
| Trustworthiness | 30% | Transparency, sources, contact info, privacy policy, HTTPS, editorial standards, corrections policy |

### Experience (20%)

First-hand knowledge and direct involvement. AI can generate expertise-sounding content but cannot fabricate genuine experience — this is the key differentiator after the December 2025 core update.

**Signals to evaluate:**
- First-person accounts ("I tested...", "We implemented...", "In our experience...")
- Original research or data not available elsewhere
- Case studies with specific results and numbers
- Screenshots, photos, or evidence of direct use (not stock images)
- Specific examples from personal experience
- Process documentation showing actual work done (not just outcomes)

**Weak Experience flags:**
- Content that only summarizes other sources without adding new perspective
- Generic advice that could apply to any situation
- No mention of actual usage, testing, or direct involvement
- Hedging language suggesting lack of direct knowledge ("reportedly", "supposedly")

### Expertise (25%)

Demonstrated knowledge depth and professional competence.

**Signals to evaluate:**
- Author credentials visible (bio, degrees, certifications, dedicated author page)
- Technical depth appropriate to topic — thorough treatment, not superficial
- Methodology explanation (how conclusions were reached)
- Data-backed claims (statistics, research citations)
- Industry-specific terminology used correctly
- Up-to-date with current developments in the field

**Weak Expertise flags:**
- Claims without supporting evidence or sources
- Surface-level coverage of complex topics
- Misuse of technical terminology
- No visible author or author without relevant credentials

### Authoritativeness (25%)

Recognition by others as a credible source.

**Signals to evaluate:**
- Inbound citations from authoritative sources
- Author quoted or cited in press/media
- Industry awards or recognition
- Speaker credentials (conferences, events)
- Published in peer-reviewed or respected outlets
- Comprehensive topic coverage (topical authority — site covers topic with depth and breadth)
- Brand mentioned on Wikipedia or authoritative references

**Weak Authoritativeness flags:**
- Single-topic site with no depth of coverage
- No external validation of expertise claims
- No backlinks from authoritative sources
- Self-proclaimed "expert" without evidence

### Trustworthiness (30%)

The most important E-E-A-T factor. Overall reliability and transparency.

**Signals to evaluate:**
- Contact information visible (physical address, phone, email)
- Privacy policy and terms of service present
- HTTPS with valid certificate
- Editorial standards or corrections policy documented
- Transparent about business model and conflicts of interest
- Customer reviews and testimonials from real customers
- Accurate claims (no misinformation detected)
- Clear affiliate/sponsorship disclosures
- Date stamps, transparent corrections

**Weak Trustworthiness flags:**
- No contact information or physical address
- Missing privacy policy or terms
- Undisclosed affiliate links or sponsored content
- Claims that are verifiably false or misleading

---

## Part 2: SEO Dimension

### 2.1 Keyword Presence and Placement

- Primary keyword in title tag (near the beginning)
- Primary keyword in H1
- Primary keyword in first 100 words
- Primary keyword in at least one H2
- Primary keyword in meta description
- Primary keyword in URL slug (or close variant)
- Natural density: 1-3% (ceiling, not target)
- Semantic variations present (LSI keywords)
- No keyword stuffing

### 2.2 Content Length vs. Competitors

Reference: `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md` — minimum word counts by page type.

These are **topical coverage floors, not targets**. Google has confirmed word count is NOT a direct ranking factor.

| Page Type | Minimum | Ideal Range | Notes |
|-----------|---------|-------------|-------|
| Homepage | 500 | 500-1,500 | Clear value proposition |
| Service / Feature Page | 800 | 800-2,000 | Detailed offering explanation |
| Blog Post | 1,500 | 1,500-3,000 | Thorough but focused |
| Product Page | 400 | 500-1,500 | Unique descriptions, specs |
| Location Page (Primary) | 600 | 600-1,000 | 60%+ unique content |
| Location Page (Secondary) | 500 | 500-800 | 40%+ unique content |
| FAQ Page | 800 | 1,000-2,500 | Thorough answers |
| About Page | 400 | 500-1,000 | Company story, credentials |

### 2.3 Readability Scores

- **Flesch Reading Ease:** Target 60-70 for general audience (8th-9th grade level)
- **Gunning Fog Index:** Target 8-12 for general audience
- **SMOG Index:** Target 8-10 for general audience
- Average sentence length: 15-20 words ideal
- Average paragraph length: 2-4 sentences
- Passive voice: < 15% of sentences
- Jargon: defined when first used

> **Note:** Readability scores are NOT direct Google ranking factors (John Mueller confirmed). Use as content quality indicators, not SEO metrics to optimize directly.

### 2.4 Content Structure

- Logical heading hierarchy: H1 -> H2 -> H3 (no skipped levels)
- One H1 per page
- Scannable sections with descriptive headings
- Bullet/numbered lists where appropriate
- Table of contents for long-form content (1,500+ words)
- Tables for comparative data

### 2.5 Internal/External Link Quality

**Internal links:**
- 3-5 relevant internal links per 1,000 words (per quality-gates.md guidelines)
- Descriptive anchor text (not "click here")
- Topic cluster structure: pillar page linked to/from all subtopic pages
- No orphan pages

**External links:**
- Cite authoritative sources (reinforces expertise and trust)
- Reasonable count (2-5 per 1,000 words)
- No broken external links
- Open in new tab for user experience

### 2.6 Multimedia

- Relevant images with proper alt text (10-125 characters, descriptive, not keyword-stuffed)
- Appropriate file format (WebP/AVIF preferred)
- Video with transcripts where appropriate
- Infographics for complex data
- Charts/graphs for statistics

### 2.7 Uniqueness and Information Gain

- Content provides unique value not available from other sources
- Original data, analysis, or perspective
- Not a rehash of top-ranking competitors
- Passes uniqueness threshold: 80%+ unique content for primary pages

---

## Part 3: GEO Dimension

### 3.1 Passage-Level Extractability

AI platforms extract content at the paragraph/passage level. Each passage must be a self-contained unit of meaning.

**Optimal passage structure (40-60 word citation capsules):**
- Each major H2 section should contain a **citation capsule**: a 40-60 word definitive statement that AI systems can extract as a standalone answer
- Self-contained (makes sense without surrounding text)
- Contains a specific claim or fact
- Includes attribution or data point
- Written in declarative voice (not hedging)

**Optimal paragraph structure:**
- 2-4 sentences per paragraph (1-sentence paragraphs are weak; 5+ are hard to extract)
- One idea per paragraph — do not mix topics
- Lead with the key claim — first sentence contains the main point
- Support with evidence — remaining sentences provide data, examples, or context
- Each paragraph should make sense if extracted in isolation

### 3.2 Semantic Triples (Subject-Predicate-Object Clarity)

AI systems parse content into semantic triples. Content with clear subject-predicate-object patterns is more extractable.

**What to check:**
- Key claims use explicit subject-predicate-object structure
- Avoid ambiguous pronouns ("it", "this", "they") at the start of key passages
- Named entities are clearly identified (not just "the company" or "the product")
- Relationships between entities are stated explicitly, not implied

**Example:**
- Weak: "It has been shown to improve results significantly."
- Strong: "HubSpot's 2025 study found that personalized email subject lines increase open rates by 26%."

### 3.3 Entity Density and Consistency

- Key entities (brand, products, people, concepts) are named consistently throughout
- No switching between synonyms for the same entity in key passages (confuses AI extraction)
- Entity density: important entities should appear in H1, first paragraph, and at least every 300 words
- Schema markup supports entity identification (Organization, Person, Product)

### 3.4 Answer-First Structure (BLUF)

BLUF = Bottom Line Up Front. AI systems preferentially extract content that leads with the direct answer.

**What to check:**
- Direct answer appears in the first 150 words of the page
- Each H2 section leads with its key takeaway before providing supporting detail
- No "burying the lede" — the most important information comes first
- Question-based headings are answered immediately in the first sentence after the heading

### 3.5 Question-Based Headings (Match AI Fanout Queries)

AI platforms decompose user queries into sub-questions. Content with question-based headings maps directly to these fanout queries.

**Target:** 60-70% of H2 headings on informational content should be phrased as questions.

**What to check:**
- H2 headings use natural question phrasing ("How does X work?" not "X Functionality")
- Questions match the way users and AI systems phrase queries
- Each question heading is followed by a direct, substantive answer
- Questions cover the full scope of the topic (no obvious gaps)

### 3.6 Citation-Worthiness Signals

Content that AI platforms choose to cite shares specific characteristics:

| Signal | What to Check |
|--------|--------------|
| Quantified claims | Statistics, percentages, specific numbers with sources |
| Expert credentials | Named author with relevant qualifications visible on page |
| Primary sources | Original research, surveys, experiments, proprietary data |
| Recency | Updated within 30 days for key pages (76.4% of top AI citations are from recent content) |
| Specificity | Named products, companies, dates, locations — not generic advice |
| Declarative voice | "X is Y" not "X might be Y" or "X could potentially be Y" |
| Source attribution | Claims linked to specific studies, reports, or named experts |

### 3.7 Content Freshness (Weighted Heavier for GEO)

Reference: `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md` — content freshness requirements.

| Criterion | Score | Assessment |
|-----------|-------|-----------|
| Updated within 30 days | Excellent | Optimal for AI citation |
| Updated within 3 months | Good | Still competitive |
| Updated within 6 months | Acceptable | May lose citations to fresher content |
| Updated within 12 months | Warning | Review and refresh |
| No date or 12+ months old | Critical | AI platforms deprioritize |

**Required elements:**
- Visible `datePublished` and `dateModified` in content AND structured data
- Specific dates (January 15, 2026) not vague ("recently")
- Key pages (homepage, top service pages, pillar content) should be updated within 30 days

**Evergreen exceptions:** Content covering fundamental concepts (physics, legal definitions, mathematical principles) is exempt from aggressive freshness requirements if clearly labeled as reference material and free of time-dependent claims.

---

## Part 4: AI Content Assessment (Shared)

### AI-Generated Content Policy

AI-generated content is **acceptable** per Google's guidance (March 2024 clarification) as long as it demonstrates genuine E-E-A-T signals and has human oversight. The Helpful Content System was merged into Google's core ranking algorithm during the March 2024 core update — helpfulness signals are now weighted within every core update.

### Signs of Low-Quality AI Content (Flag These)

| Signal | Description |
|--------|------------|
| Generic phrasing | "In today's fast-paced world...", "It's important to note that..." |
| No original insight | Content only rephrases widely available information |
| Lack of first-hand experience | No personal anecdotes, case studies, or specific examples |
| Perfect but empty structure | Well-formatted headings with shallow content beneath |
| No specific examples | Abstract explanations without concrete instances |
| Repetitive conclusions | Each section ends with the same point |
| Hedging overload | "Generally speaking", "In most cases" without specifying which |
| Missing human voice | No opinions, preferences, or professional judgment |
| Filler content | Paragraphs that could be deleted without losing information |
| No data or sources | Claims presented as facts without attribution |

### Signs of High-Quality Content (Regardless of Production Method)

| Signal | Description |
|--------|------------|
| Original data | Surveys, experiments, benchmarks, proprietary analysis |
| Specific examples | Named products, companies, dates, numbers |
| Contrarian or nuanced views | Disagreement with conventional wisdom, backed by reasoning |
| First-person experience | "When I tested this..." or "Our team found..." |
| Updated information | References to recent events, current data |
| Expert opinion | Clear professional judgment, not just facts |
| Practical recommendations | Specific, actionable advice |
| Trade-offs acknowledged | "This works well for X but not for Y because..." |

---

## Dual Scoring

### SEO Content Score (0-100)

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| Keyword optimization | 25% | Placement, density, semantic variations, intent alignment |
| Readability | 20% | Flesch, Gunning, SMOG, sentence/paragraph length, passive voice |
| E-E-A-T signals | 25% | Experience 20%, Expertise 25%, Authoritativeness 25%, Trustworthiness 30% |
| Content structure | 15% | Heading hierarchy, word count vs. benchmarks, lists, ToC |
| Links | 15% | Internal link density, anchor text, external citations, broken links |

### GEO Content Score (0-100)

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| Extractability | 25% | Passage length, self-containment, citation capsules, BLUF structure |
| E-E-A-T signals | 25% | Same weights as SEO — shared foundation |
| Entity clarity | 20% | Semantic triples, entity consistency, named entity density, schema support |
| Passage quality | 15% | Question-based headings, declarative voice, specificity, data density |
| Freshness | 15% | Last update date, dateModified in structured data, 30-day threshold |

### Topical Authority Modifier (GEO only)

| Level | Description | Score Impact |
|-------|-------------|-------------|
| Authority | 20+ pages covering topic comprehensively, strong clustering | +10 bonus |
| Developing | 10-20 pages with some clustering | +5 bonus |
| Emerging | 5-10 pages on topic, limited clustering | +0 |
| Thin | < 5 pages, no clustering | -5 penalty |

Final GEO Score = GEO Content Score + Topical Authority Modifier (capped at 100).

---

## Quality Gates

Reference: `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md`

Apply the following gates before scoring. Pages that fail a gate receive an automatic flag:

| Gate | Threshold | Action |
|------|-----------|--------|
| Minimum word count | Per page type (see Part 2.2) | Flag as "thin content" if below minimum |
| Location page uniqueness | 60%+ unique for primary, 40%+ for secondary | Flag as "doorway page risk" if below |
| Location page volume | Warning at 30+, hard stop at 50+ | Flag and require justification |
| Title tag length | 30-60 characters | Flag if outside range |
| Meta description length | 120-160 characters | Flag if outside range |
| Image alt text | All non-decorative images | Flag missing alt text |
| HTTPS | Valid certificate required | Flag if missing |
| Publication date | Must be visible | Flag if absent |

---

## Output Format

### Default Mode (`--full`) and Mode-Specific Reports

```markdown
## Content Analysis — [URL]

| Dimension | SEO Score | GEO Score |
|-----------|-----------|-----------|
| E-E-A-T | 72 | 68 |
| Structure | 85 | 60 |
| Readability | 78 | 78 |
| Keywords/Entities | 65 | 70 |
| Links/Citations | 80 | 55 |

**Overall SEO Content Score: X/100**
**Overall GEO Content Score: X/100**

### E-E-A-T Breakdown

| Factor | Score | Weight | Key Signals |
|--------|-------|--------|-------------|
| Experience | XX | 20% | [One-line finding] |
| Expertise | XX | 25% | [One-line finding] |
| Authoritativeness | XX | 25% | [One-line finding] |
| Trustworthiness | XX | 30% | [One-line finding] |

### Key Findings

[Top 3-5 findings across both dimensions, ordered by impact]

### Quality Gate Flags

[Any gates that were triggered — thin content, missing dates, etc.]

### Recommendations

#### SEO Quick Wins
1. [Specific, actionable recommendation with expected impact]
2. [...]
3. [...]

#### GEO Quick Wins
1. [Specific, actionable recommendation with expected impact]
2. [...]
3. [...]

### Content Freshness

| Page | Published | Last Updated | Status |
|------|----------|-------------|--------|
| [URL] | [Date] | [Date] | [Current/Stale/No Date] |

### Most Citable Passages (GEO)

[Top 3-5 passages AI platforms are most likely to cite, with reasons]

### Citation Capsule Gaps (GEO)

[H2 sections missing a 40-60 word definitive statement]

### AI Content Assessment

[Low-quality AI content patterns detected, if any, with specific examples]
```

### `--seo` Mode

Same structure but:
- GEO Score column hidden from the dual score table
- GEO Quick Wins section omitted
- Citability and passage sections replaced with one-line summaries
- Keyword analysis is prominent

### `--geo` Mode

Same structure but:
- SEO Score column hidden from the dual score table
- SEO Quick Wins section omitted
- Keyword section replaced with context note ("improves discoverability, not citation")
- Passage architecture and citability sections are prominent
- Topical Authority modifier shown with final score

---

## DataForSEO Integration (Optional — SEO mode)

If DataForSEO MCP tools are available, enhance keyword analysis:

| Tool | Purpose |
|------|---------|
| `kw_data_google_ads_search_volume` | Real keyword volume data |
| `dataforseo_labs_bulk_keyword_difficulty` | Difficulty scores |
| `dataforseo_labs_search_intent` | Intent classification |
| `content_analysis_summary` | Content quality analysis |

These are optional enrichments — the audit works fully without them.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess page content. Suggest the user verify the URL and try again. |
| Content behind paywall (402/403, login wall) | Report that content is not publicly accessible. Analyze only the visible portion (meta tags, headers) and note the limitation. |
| Thin content (fewer than 100 words retrievable) | Report findings as-is. Flag the page as potentially JavaScript-rendered or gated. Suggest the user provide the full text directly. |
| No structured data found | Note the absence. Score entity clarity based on on-page signals only. Recommend schema implementation. |

---

## Cross-References

- **E-E-A-T scoring details** — `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md`
- **Content quality gates and thresholds** — `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md`
- **Deep passage-level citability scoring** (0-100 rubric) — `/geo-citability`
- **Content rewriting for AI extractability** — `/42-genai-optimizer`
- **Schema markup** (Article, Person, Organization) — `/42:structured-data`
- **Full SEO audit** — `/42:seo`
- **Full GEO audit** — `/42:geo`
