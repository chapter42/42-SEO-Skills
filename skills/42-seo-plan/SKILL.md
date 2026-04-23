---
name: 42-seo-plan
description: >
  Strategic SEO/GEO planning skill that produces STRATEGY.md with locked decisions,
  prioritized task lists, and wave assignments. Accepts audit scores and Top-25 data
  as input. Industry-specific templates for SaaS, eCommerce, local, publisher, B2B.
  Use when user says "SEO plan", "strategy", "roadmap", "what should we fix first",
  "prioritize", "actieplan".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
version: 2.0.0
tags: [strategy, planning, seo, geo, roadmap]
---

# SEO/GEO Strategic Planner

Produces `STRATEGY.md` with locked decisions, prioritized waves, and concrete task
assignments. This is the bridge between audit data (Phase 1-2) and implementation
(Phase 4). Every decision gets an ID that Phase 4 IMPLEMENT references.

**This skill does NOT audit.** It reads audit outputs and transforms them into
an actionable, prioritized strategy.

---

## Input Requirements

The skill expects these files to exist (produced by earlier phases):

| File | Source | Required |
|------|--------|----------|
| `42-reports/<domain>/reports/DISCOVERY.md` | 42-audit (Phase 1) | Yes |
| `42-reports/<domain>/TOP-25.md` | 42-screaming-frog (Phase 1) | Yes |
| `42-reports/<domain>/INTAKE.md` | Phase 0 intake | Yes |
| `42-reports/<domain>/STATE.md` | Phase 0 init | Yes |

**Optional enrichment sources** (from Phase 2 DIAGNOSE or Phase 3 optional skills):

| File | Source | Enriches |
|------|--------|----------|
| `reports/DIAGNOSIS.md` | Phase 2 deep-dive | Issue severity + prioritization |
| `reports/COMPETITIVE-INTELLIGENCE.md` | 42-competitor-pages | Competitive position section |
| `reports/TOPICAL-MAP.md` | 42-topical-map | Content strategy section |
| `reports/SERP-CLUSTERS.md` | 42-serp-cluster | Keyword grouping in waves |
| `reports/AUDIENCE-ANGLES.md` | 42-audience-angles | Content angle suggestions |
| `reports/PAA-DATA.md` | 42-paa-scraper | FAQ/content opportunities |

---

## Process

### Step 1: Read and Parse Inputs

1. Read `STATE.md` to extract:
   - `business_type` (SaaS, eCommerce, local, publisher, B2B)
   - `capability_tier` (1, 2, or 3)
   - `language` and `target_market`
   - Phase statuses (what data is available)

2. Read `DISCOVERY.md` to extract:
   - SEO Health Score (0-100)
   - GEO Readiness Score (0-100)
   - Per-category scores: technical, content, schema, links, GEO
   - Critical issues list

3. Read `TOP-25.md` to extract:
   - Ranked page list with priority scores
   - User-selected top-5 for deep-dive
   - Striking distance opportunities

4. Read `INTAKE.md` to extract:
   - Business goals and KPIs
   - Budget/timeline constraints
   - Competitors identified
   - Target audience

5. Read any optional enrichment files that exist.

### Step 2: Select Industry Template

Based on `business_type` from STATE.md, apply the matching inline template
(see Industry Templates section below). The template provides:
- Focus areas specific to the business type
- Typical wave assignments
- Industry-specific success criteria
- Common quick wins for that vertical

### Step 3: Build Priority Matrix

Score every issue from DISCOVERY.md and DIAGNOSIS.md (if available) using:

```
Priority Score = (Impact × 0.40) + (Effort_inverse × 0.30) + (Urgency × 0.30)
```

Where:
- **Impact** (1-10): How much does fixing this improve SEO/GEO scores?
- **Effort_inverse** (1-10): 10 = trivial fix, 1 = months of work
- **Urgency** (1-10): 10 = blocking indexing/revenue, 1 = nice-to-have

Assign each issue to a wave:

| Wave | Priority Score | Timeline | Description |
|------|---------------|----------|-------------|
| Wave 1 — Critical | 8.0-10.0 | Week 1-2 | Blocking issues, immediate ROI |
| Wave 2 — High | 6.0-7.9 | Week 2-4 | Strong impact, moderate effort |
| Wave 3 — Medium | 4.0-5.9 | Month 2-3 | Strategic improvements |
| Wave 4 — Low | 1.0-3.9 | Ongoing | Maintenance, polish, experiments |

### Step 4: Draft Locked Decisions

Based on the data analysis, draft 5-10 decisions. Each decision must:
- Be supported by specific audit data (cite scores, numbers, URLs)
- Have a clear rationale
- Be actionable (not vague)
- Map to one or more wave tasks

Present draft decisions to the user for confirmation. Only mark as "locked"
after user approval.

### Step 5: Map Tasks to Skills

Every task in a wave must reference the 42-skill that executes it:

| Skill | Typical wave tasks |
|-------|-------------------|
| `42-technical` | Fix crawlability, canonicals, redirects, mobile issues |
| `42-crawlers` | Unblock AI crawlers in robots.txt |
| `42-llmstxt` | Generate or fix llms.txt |
| `42-structured-data` | Add/fix schema markup |
| `42-content` | Content quality improvements, thin content |
| `42-genai-optimizer` | GEO passage optimization |
| `42-sitemap` | Fix/generate XML sitemap |
| `42-images` | Image optimization (alt, format, lazy loading) |
| `42-meta-optimizer` | Title/meta description optimization |
| `42-internal-links` | Internal link structure improvements |
| `42-hreflang` | Multi-language implementation |
| `42-striking-distance` | Quick-win keyword positioning |
| `42-blog` | Blog content optimization |
| `42-readability` | Readability improvements |
| `42-snippet-optimizer` | Featured snippet optimization |

### Step 6: Generate STRATEGY.md

Write the complete strategy document following the output format below.

### Step 7: Score the Strategy

Apply the strategy quality rubric (see Scoring section) and include the
self-assessment score in the output.

---

## Output Format: STRATEGY.md

Write to: `42-reports/<domain>/reports/STRATEGY.md`

```markdown
# SEO/GEO Strategy — [Domain]

> Generated: [date] | Skill: 42-seo-plan v2.0.0
> Based on: DISCOVERY.md ([date]), TOP-25.md ([date]), INTAKE.md ([date])

## Context

| Attribute | Value |
|-----------|-------|
| Business type | [from INTAKE.md] |
| Capability tier | [1/2/3 from STATE.md] |
| Language/market | [from INTAKE.md] |
| SEO Score | [X]/100 |
| GEO Score | [X]/100 |
| Technical score | [X]/100 |
| Content score | [X]/100 |
| Schema score | [X]/100 |
| Links score | [X]/100 |
| Top-5 focus pages | [URLs from TOP-25 selection] |

### Score Interpretation

[Brief paragraph explaining what the scores mean for this specific site.
Highlight the weakest category and why it matters most. Reference the
industry benchmark from the template.]

## Locked Decisions

Each decision has an ID, is immutable once locked, and is referenced by
Phase 4 IMPLEMENT. Decisions are locked by the user during the interactive
strategy session.

| ID | Decision | Rationale | Locked by |
|----|----------|-----------|-----------|
| D-01 | [e.g., Focus on technical fixes first] | [e.g., Technical score 42/100 is blocking crawl/index] | [user/auto] |
| D-02 | [e.g., Target striking distance keywords] | [e.g., 23 pages at position 4-12 with easy wins] | [user/auto] |
| D-03 | [e.g., Dutch market only, no hreflang] | [e.g., Single-language site per intake] | [user/auto] |
| D-04 | [e.g., Prioritize GEO over link building] | [e.g., AI traffic growing, GEO score 28/100] | [user/auto] |
| D-05 | ... | ... | ... |

## Priority Waves

### Wave 1 — Critical (week 1-2)

> Focus: Remove blockers. Fix what prevents Google and AI engines from
> crawling, indexing, and understanding the site.

| # | Task | Skill | Target | Est. impact | Ref |
|---|------|-------|--------|-------------|-----|
| 1.1 | [e.g., Fix broken canonicals] | 42-technical | Site-wide (14 pages) | High | D-01 |
| 1.2 | [e.g., Unblock AI crawlers] | 42-crawlers | robots.txt | High | D-04 |
| 1.3 | [e.g., Fix critical schema errors] | 42-structured-data | Homepage + top-5 | High | D-01 |
| ... | ... | ... | ... | ... | ... |

### Wave 2 — High (week 2-4)

> Focus: Quick wins. Optimize what already exists for maximum ROI.

| # | Task | Skill | Target | Est. impact | Ref |
|---|------|-------|--------|-------------|-----|
| 2.1 | [e.g., Optimize striking distance pages] | 42-striking-distance | 23 pages pos 4-12 | High | D-02 |
| 2.2 | [e.g., Add missing meta descriptions] | 42-meta-optimizer | 38 pages | Medium | D-01 |
| 2.3 | [e.g., Generate llms.txt] | 42-llmstxt | Site root | Medium | D-04 |
| ... | ... | ... | ... | ... | ... |

### Wave 3 — Medium (month 2-3)

> Focus: Strategic improvements. Content quality, topical authority, GEO.

| # | Task | Skill | Target | Est. impact | Ref |
|---|------|-------|--------|-------------|-----|
| 3.1 | [e.g., Rewrite thin content pages] | 42-content | 12 pages < 300 words | Medium | D-01 |
| 3.2 | [e.g., Build internal link structure] | 42-internal-links | Top-25 pages | Medium | D-02 |
| 3.3 | [e.g., Optimize passages for AI citation] | 42-genai-optimizer | Top-5 pages | Medium | D-04 |
| ... | ... | ... | ... | ... | ... |

### Wave 4 — Low (ongoing)

> Focus: Maintenance, polish, and experimentation.

| # | Task | Skill | Target | Est. impact | Ref |
|---|------|-------|--------|-------------|-----|
| 4.1 | [e.g., Image optimization] | 42-images | Site-wide | Low | — |
| 4.2 | [e.g., Readability improvements] | 42-readability | Blog posts | Low | — |
| 4.3 | [e.g., Content repurposing] | 42-content-repurposer | Top-5 posts | Low | — |
| ... | ... | ... | ... | ... | ... |

## Content Strategy

### Topical Authority
[If 42-topical-map data available: summarize pillar topics, cluster structure,
and content gaps. If not available: recommend running 42-topical-map and
provide preliminary topic suggestions based on INTAKE.md and keyword data.]

### Content Gaps
[Pages competitors have that this site lacks. Based on COMPETITIVE-INTELLIGENCE.md
if available, otherwise based on INTAKE.md competitor URLs and general analysis.]

### Keywords to Target
[Top 10-15 keyword opportunities organized by intent:
- Transactional: [keywords]
- Commercial investigation: [keywords]
- Informational: [keywords]
- Navigational: [keywords if relevant]]

### FAQ/Content Opportunities
[If PAA data available: top question clusters. If not: recommend running
42-paa-scraper for target keywords.]

## Competitive Position

### Share of Voice
[If COMPETITIVE-INTELLIGENCE.md available: summarize visibility share.
If not: note as "pending — run 42-share-of-voice".]

### Key Competitor Gaps
[What competitors do better. What this site does better. Specific pages
or content types to create/improve.]

### Competitive Advantages
[Unique strengths to leverage: brand, expertise, data, UGC, etc.]

## Success Criteria

| KPI | Baseline | Target (3 months) | Target (6 months) |
|-----|----------|-------------------|-------------------|
| SEO Score | [X]/100 | [Y]/100 | [Z]/100 |
| GEO Score | [X]/100 | [Y]/100 | [Z]/100 |
| Technical score | [X]/100 | [Y]/100 | [Z]/100 |
| Content score | [X]/100 | [Y]/100 | [Z]/100 |
| Organic traffic | [X] | +[Y]% | +[Z]% |
| AI citations | [X] | [Y] | [Z] |
| Pages in Top 10 | [X] | [Y] | [Z] |
| Striking distance converted | 0 | [Y] | [Z] |

### Milestone Checkpoints

- **Week 2:** Wave 1 complete. Re-run 42-audit for technical score delta.
- **Week 4:** Wave 2 complete. Check striking distance conversions.
- **Month 2:** Wave 3 in progress. Content improvements measurable.
- **Month 3:** Wave 3 complete. Full re-audit via 42-seo-project verify.
- **Month 6:** Long-term targets. Run 42-share-of-voice for competitive tracking.

## Strategy Quality Score

| Dimension | Score | Notes |
|-----------|-------|-------|
| Data-backed decisions (25%) | [X]/25 | [Are all decisions citing specific audit data?] |
| Completeness (25%) | [X]/25 | [Are all critical issues from DISCOVERY addressed?] |
| Prioritization logic (25%) | [X]/25 | [Is impact/effort scoring consistent?] |
| Feasibility (25%) | [X]/25 | [Realistic given capability tier and timeline?] |
| **Total** | **[X]/100** | |
```

---

## Industry Templates

### SaaS Template

**Typical focus areas:**
- Feature/product pages as primary conversion drivers
- Comparison pages ("X vs Y") for commercial keywords
- Documentation and knowledge base SEO (long-tail)
- Free trial / demo CTA optimization
- Integration pages (partner ecosystem)
- API documentation as developer SEO

**Typical wave assignments:**

| Wave | SaaS-specific tasks |
|------|-------------------|
| 1 | Fix technical SEO on product pages, ensure pricing page is indexable, schema for SoftwareApplication |
| 2 | Optimize feature pages for target keywords, add FAQ schema to comparison pages, striking distance fixes |
| 3 | Build topical authority (blog → product page internal links), create comparison content, documentation SEO |
| 4 | Integration pages, case study optimization, thought leadership content |

**SaaS success benchmarks:**
- Technical score target: 80+
- Feature page word count: 800-1500 words
- Comparison page conversion: track demo requests from organic
- Documentation indexed ratio: 90%+

**SaaS-specific decisions to consider:**
- D: Product-led content vs thought leadership emphasis
- D: Single product focus vs multi-product keyword strategy
- D: Documentation SEO investment level (high for developer tools, low for SMB SaaS)
- D: Comparison page strategy (direct competitor naming vs category comparison)

---

### eCommerce Template

**Typical focus areas:**
- Category page optimization (primary ranking targets)
- Product schema (Product, Offer, AggregateRating, Review)
- Faceted navigation crawl budget management
- Internal linking (category → product → related products)
- Breadcrumb schema and navigation
- Price/availability structured data

**Typical wave assignments:**

| Wave | eCommerce-specific tasks |
|------|------------------------|
| 1 | Fix crawl budget waste (faceted URLs), canonical strategy, Product schema on top-25 products |
| 2 | Category page content optimization, breadcrumb schema, internal linking from category to products |
| 3 | Product description enrichment, review schema, FAQ schema on category pages |
| 4 | Image optimization (product photos), collection page creation, seasonal content |

**eCommerce success benchmarks:**
- Category pages in Top 20: track by target keyword cluster
- Product schema coverage: 95%+ of active products
- Faceted URL crawl waste: < 10% of crawl budget
- Internal link depth: product pages reachable in <= 3 clicks

**eCommerce-specific decisions to consider:**
- D: Category page content strategy (editorial vs product-grid only)
- D: Faceted navigation handling (noindex/canonical/parameter handling)
- D: Review/UGC schema strategy (aggregate vs individual reviews)
- D: Seasonal content calendar alignment

**Reference:** Apply thresholds from `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md` for
product description minimum word count and category page requirements.

---

### Local Template

**Typical focus areas:**
- Google Business Profile (GBP) optimization
- NAP consistency (Name, Address, Phone) across web
- Local schema (LocalBusiness, PostalAddress, GeoCoordinates)
- Location pages (for multi-location businesses)
- Local keyword optimization ("near me", city + service)
- Review management and review schema

**Typical wave assignments:**

| Wave | Local-specific tasks |
|------|---------------------|
| 1 | GBP claim/verify, fix NAP inconsistencies, add LocalBusiness schema |
| 2 | Location page optimization, local keyword targeting, add opening hours schema |
| 3 | Review strategy, local content (area guides, community), citation building |
| 4 | Event schema, seasonal local content, local link opportunities |

**Local success benchmarks:**
- GBP completeness: 100% of fields filled
- NAP consistency: 100% match across top 20 directories
- Local pack visibility: track for top 5 service keywords
- Location page quality: minimum 500 words unique content per location

**Local-specific decisions to consider:**
- D: Single location vs multi-location strategy
- D: Service area pages vs physical location pages
- D: Review acquisition strategy (which platforms to prioritize)
- D: Local content investment (area guides, community involvement)

**Reference:** Apply thresholds from `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md` for
location page minimum content requirements and LocalBusiness schema completeness.

---

### Publisher Template

**Typical focus areas:**
- Article freshness signals (datePublished, dateModified)
- Author E-E-A-T (Person schema, author pages, credentials)
- Google Discover optimization (large images, engaging headlines)
- NewsArticle / Article schema completeness
- Content decay detection and refresh strategy
- Topical authority through comprehensive coverage

**Typical wave assignments:**

| Wave | Publisher-specific tasks |
|------|------------------------|
| 1 | Fix Article schema errors, add dateModified to all articles, author Person schema |
| 2 | Author page optimization (E-E-A-T), Discover image requirements (1200px+), content freshness audit |
| 3 | Content refresh for decaying articles, topical gap filling, internal link restructuring |
| 4 | Syndication strategy, content repurposing, advanced author authority building |

**Publisher success benchmarks:**
- Schema coverage: Article/NewsArticle on 100% of articles
- Author pages: all authors have dedicated bio pages with Person schema
- Content freshness: < 10% of articles older than 12 months without update
- Discover eligibility: 90%+ of articles meet image size requirements

**Publisher-specific decisions to consider:**
- D: Evergreen vs news content balance
- D: Content refresh cadence (monthly, quarterly, on-decay)
- D: Author authority investment level
- D: Discover vs Search as primary traffic source
- D: Paywall/metered content impact on indexing

**Reference:** Apply E-E-A-T scoring from `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md`
and `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-scoring-rubric.md` for author authority assessment.

---

### B2B Template

**Typical focus areas:**
- Thought leadership content (long-form, data-driven)
- Case study optimization (structured, schema-enriched)
- Whitepaper/resource SEO (gated vs ungated strategy)
- Industry-specific keyword targeting
- E-E-A-T through expertise demonstration
- Long sales cycle content mapping (awareness → consideration → decision)

**Typical wave assignments:**

| Wave | B2B-specific tasks |
|------|-------------------|
| 1 | Fix technical SEO on service pages, add Organization schema, fix site architecture |
| 2 | Service page content optimization, case study schema, thought leadership keyword targeting |
| 3 | Whitepaper landing page optimization, industry content hub creation, FAQ schema |
| 4 | Executive author profiles, speaking/event schema, partnership content |

**B2B success benchmarks:**
- Service page rankings: top 10 for primary service keywords
- Case study indexation: 100% indexed with proper schema
- Content hub completion: all pillar topics have 5+ supporting articles
- E-E-A-T signals: author bios, credentials, company about page scoring 70%+

**B2B-specific decisions to consider:**
- D: Gated vs ungated content strategy (SEO tradeoff)
- D: Thought leadership frequency and depth
- D: Case study optimization investment (per case study vs bulk)
- D: Industry vertical content strategy (horizontal vs vertical focus)
- D: Executive personal branding integration

**Reference:** Apply E-E-A-T framework from `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md`
for expertise and authority signal assessment.

---

## Integration with Optional Skills

When available, incorporate outputs from these Phase 3 optional skills:

### 42-competitor-pages
- **Input:** Competitor URLs from INTAKE.md
- **Enriches:** Competitive Position section
- **How:** Adds specific page-level gap analysis, content type comparison,
  and feature/topic coverage gaps to the strategy

### 42-topical-map
- **Input:** Keywords from DISCOVERY.md + keyword research
- **Enriches:** Content Strategy → Topical Authority section
- **How:** Provides pillar → cluster → subtopic hierarchy, identifies content
  gaps as specific Wave 3/4 tasks

### 42-serp-cluster
- **Input:** Target keywords
- **Enriches:** Wave task assignments (keyword grouping)
- **How:** Groups keywords that share SERPs onto the same page, preventing
  cannibalization and informing which pages to optimize together

### 42-audience-angles
- **Input:** Target audience from INTAKE.md
- **Enriches:** Content Strategy section
- **How:** QPAFFCGMIM framework angles inform content creation tasks in
  Wave 3/4 and suggest content angles for existing pages

### 42-paa-scraper
- **Input:** Top keywords from audit
- **Enriches:** Content Strategy → FAQ/Content Opportunities section
- **How:** Question clusters become FAQ schema candidates (Wave 2) and
  content gap tasks (Wave 3)

---

## Strategy Quality Scoring Rubric

Score the generated strategy on four dimensions (total 0-100):

### Data-backed decisions (25 points)

| Score | Criteria |
|-------|----------|
| 25 | Every decision cites specific data (scores, URLs, numbers) from audit |
| 20 | Most decisions cite data, 1-2 are based on general best practice |
| 15 | Mix of data-driven and assumption-based decisions |
| 10 | Mostly best-practice assumptions, few data references |
| 5 | Generic decisions not tied to this specific site |

### Completeness (25 points)

| Score | Criteria |
|-------|----------|
| 25 | All critical/high issues from DISCOVERY addressed in waves |
| 20 | 90%+ of critical issues addressed, all high issues mentioned |
| 15 | Critical issues addressed, some high issues missing |
| 10 | Major gaps in issue coverage |
| 5 | Only addresses surface-level issues |

### Prioritization logic (25 points)

| Score | Criteria |
|-------|----------|
| 25 | Impact/effort scoring consistent, wave assignments logical, dependencies respected |
| 20 | Minor prioritization issues (1-2 tasks in wrong wave) |
| 15 | Some tasks lack clear impact/effort justification |
| 10 | Wave assignments seem arbitrary |
| 5 | No visible prioritization logic |

### Feasibility (25 points)

| Score | Criteria |
|-------|----------|
| 25 | Realistic given capability tier, timeline matches budget, no impossible tasks |
| 20 | Mostly feasible, 1-2 tasks may be ambitious |
| 15 | Timeline optimistic, some tasks need more resources than available |
| 10 | Significant feasibility concerns not addressed |
| 5 | Strategy ignores resource constraints |

---

## Shared Resource References

This skill references the following shared resources for consistent scoring
and recommendations:

| Resource | Path | Used for |
|----------|------|----------|
| E-E-A-T Framework | `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-framework.md` | Author/expertise strategy recommendations |
| E-E-A-T Scoring | `${CLAUDE_PLUGIN_ROOT}/skills/references/eeat-scoring-rubric.md` | Scoring author authority signals |
| Quality Gates | `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md` | Content thresholds (word count, readability, etc.) |
| Schema Types | `${CLAUDE_PLUGIN_ROOT}/skills/references/schema-types.md` | Schema recommendations per business type |
| CWV Thresholds | `${CLAUDE_PLUGIN_ROOT}/skills/references/cwv-thresholds.md` | Core Web Vitals pass/fail targets |

---

## Interactive Strategy Session

The strategy phase is interactive. The skill should:

1. **Present findings first.** Show the user a summary of audit scores,
   top issues, and the top-5 focus pages before proposing decisions.

2. **Propose draft decisions.** Present 5-10 draft decisions with rationale.
   Ask the user to confirm, modify, or reject each one.

3. **Lock decisions explicitly.** Only mark a decision as "locked" after
   user confirmation. Use `[user]` in the "Locked by" column for
   user-confirmed decisions and `[auto]` for data-obvious decisions
   the user does not contest.

4. **Show wave overview.** After decisions are locked, show the wave
   structure with task counts and estimated effort per wave.

5. **Ask for timeline confirmation.** Confirm that the wave timeline
   matches the user's available budget and resources.

6. **Generate and present.** Write STRATEGY.md and show the quality score.

---

## Capability Tier Adjustments

The strategy adapts based on the project's capability tier:

### Tier 1 (Manual — no API keys)
- Wave tasks use WebFetch-based skills only
- No automated keyword research (suggest manual alternatives)
- No SERP clustering or DataForSEO enrichment
- Content strategy based on INTAKE.md and manual research
- Success criteria use relative targets ("+X%") not absolute numbers

### Tier 2 (Basic API — DataForSEO or Gemini)
- Keyword research via DataForSEO available for content strategy
- Embeddings available for semantic analysis
- Can include SERP data in competitive position
- Success criteria can include keyword position targets

### Tier 3 (Full Automation — SF + GSC + APIs)
- Full crawl data informs every wave task with specific URLs and counts
- GSC data provides baseline traffic numbers for success criteria
- Automated re-audit possible for milestone checkpoints
- Content decay data available for refresh prioritization

---

## Output

**Primary output:** `42-reports/<domain>/reports/STRATEGY.md`

**State update:** Set the following in `42-reports/<domain>/STATE.md`:
```yaml
phases:
  strategize:
    status: completed
    decisions_locked: [count]
    waves: 4
    tasks_total: [count]
    strategy_quality_score: [0-100]
```

**Orchestrator handoff:** After STRATEGY.md is written, the 42-seo-project
orchestrator advances to Phase 4 IMPLEMENT, which reads STRATEGY.md to
determine wave contents and task execution order.
