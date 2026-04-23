---
name: 42-ai-visibility
version: 2.0.0
description: >
  Track and analyze AI visibility for brands and websites. Discover which
  prompts and queries AI systems (ChatGPT, Perplexity, Google AI Overviews)
  use to recommend brands, using 6 data sources: GSC long queries, forum
  discussions, top-performing pages, People Also Ask, existing AI citations,
  and competitor queries. Generates grouped prompt clusters with actionable
  insights. Use when user says "AI visibility", "AI tracking", "prompt
  tracking", "AI mentions", "AI citations tracking", "brand visibility AI",
  "ChatGPT mentions", "AI brand monitoring", or "prompt discovery".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
---

# AI Visibility Tracking & Prompt Discovery

Track where and how AI systems mention brands, and discover which prompts
to monitor for AI-powered search visibility.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/42-ai-visibility discover <domain>` | Full prompt discovery across all 6 data sources |
| `/42-ai-visibility gsc <domain>` | Extract long conversational queries from GSC |
| `/42-ai-visibility forums <topic>` | Find real user questions from Reddit/Quora |
| `/42-ai-visibility competitors <domain>` | Find competitor AI mentions you're missing |
| `/42-ai-visibility audit <domain>` | Check current AI visibility across platforms |
| `/42-ai-visibility cluster <topic>` | Group prompts into actionable clusters |

## Core Principle

> AI answers are inconsistent. ChatGPT recommends brand A now, brand B
> five minutes later. Therefore: **never track individual prompts**.
> Group similar questions and analyze the aggregated data.

## The 6 Data Sources

### 1. Long Queries from Google Search Console

Extract conversational, AI-style queries (10+ words).

**Method:**
- Go to GSC > Performance > Search results
- Click + NEW filter > Query > Custom (regex)
- Use regex: `^(?:\S+\s+){9,}\S+$`

**Why it works:** These long-tail queries mirror how people ask AI systems.
They reveal specific intents:
- Country-based solutions ("best CRM for small businesses in the Netherlands")
- Cheaper alternatives ("affordable alternative to [competitor] with API")
- Legacy product issues ("how to fix [product] error that still happens in 2026")

**Output format for GSC analysis:**
```
| Query | Clicks | Impressions | CTR | Position | Intent Category |
```

Group queries by intent category:
- Comparison queries ("X vs Y", "alternative to")
- How-to queries ("how to", "best way to")
- Problem-solving queries ("fix", "solve", "error")
- Recommendation queries ("best", "top", "recommended")

### 2. Forum Discussions via &udm=18

Reddit and Quora show how real people formulate questions.

**Method:**
- Search Google for your topic
- Add `&udm=18` to the URL to filter for forum results only
- This bypasses hoping forum results appear in regular SERPs

**What to extract:**
- Exact question phrasing people use
- Follow-up questions in threads
- Pain points and frustrations mentioned
- Brands/products people recommend to each other
- Common misconceptions or outdated information

**Pro tip:** Search for `[your brand] site:reddit.com` and
`[your competitor] site:reddit.com` to compare mention sentiment.

### 3. Top-Performing Pages

Which pages already convert? Build prompt clusters around those topics.

**Method:**
- Identify top 10-20 pages by conversions (not just traffic)
- For each page, identify the core topic and user intent
- Generate prompt variations that would lead AI to recommend that content
- Cross-reference with actual AI responses for those prompts

**Prompt template for top pages:**
```
For page: [URL]
Topic: [core topic]
Generate 10 prompts a user might ask ChatGPT/Perplexity that should
ideally surface this page or its content as a recommendation.
```

### 4. People Also Ask (PAA) in Google

Natural follow-up questions that reveal query chains.

**Method:**
- Search for your core keywords in Google
- Expand all PAA boxes (click each question to generate more)
- Use the Sprout SEO browser extension to bulk-download PAA from SERPs

**Why it matters:** PAA questions map directly to how AI systems chain
follow-up responses. They reveal:
- The natural progression of user curiosity
- Adjacent topics you should cover
- Gaps in your current content

### 5. Existing AI Visibility

Check where you already appear in AI responses and expand from there.

**Method:**
- Test 20-30 core prompts across ChatGPT, Perplexity, Google AI Overviews
- Document which prompts mention your brand
- Note the context (recommended, compared, mentioned in passing)
- Use the Sprout SEO extension to map Query Fan-Outs and download for analysis

**Track per prompt:**
```
| Prompt | ChatGPT | Perplexity | Google AIO | Mention Type | Sources Cited |
```

**Mention types:**
- Direct recommendation ("I recommend [brand]")
- Comparison inclusion ("Options include [brand], [competitor]...")
- Source citation (content quoted/linked)
- Passing mention (named but not recommended)

### 6. Competitor Queries

Where do competitors appear that you don't?

**Method:**
- Run the same prompt set for competitors
- Identify prompts where competitors are mentioned but you're not
- Analyze WHY they get mentioned (content quality, brand signals, sources)
- Prioritize gaps by business impact

**Gap analysis template:**
```
| Prompt | Competitor Mentioned | Their Source | Your Gap | Priority |
```

## Workflow: Full Prompt Discovery

When user runs `/42-ai-visibility discover <domain>`:

### Step 1: Gather Context
Ask the user:
1. What is the domain/brand to track?
2. What are 3-5 core topics/keywords?
3. Who are 2-3 main competitors?
4. Do they have GSC access? (for data source 1)
5. What is the primary business goal? (leads, sales, awareness)

### Step 2: Research Phase
Run these in parallel where possible:
1. **Forum research** -- Search Reddit/Quora for the core topics
2. **PAA extraction** -- Gather People Also Ask for core keywords
3. **Competitor check** -- Test competitor visibility in AI responses
4. **Current visibility** -- Test brand's current AI mentions

### Step 3: Cluster & Prioritize
Group all discovered prompts into clusters:

```
## Cluster: [Topic Name]
Estimated monthly search intent: [volume indicator]
Current AI visibility: [none / partial / strong]
Business impact: [high / medium / low]

### Prompts in this cluster:
1. [prompt variation 1]
2. [prompt variation 2]
3. [prompt variation 3]
...

### Actionable insights:
- [specific action 1]
- [specific action 2]
```

### Step 4: Generate Report

Output `AI-VISIBILITY-REPORT.md` with:

1. **Executive Summary**
   - Current AI visibility score (0-100 across platforms)
   - Number of prompts discovered and clustered
   - Top 3 opportunities

2. **Prompt Clusters** (grouped by topic)
   - 20-30 prompts minimum per analysis
   - Grouped into 4-6 clusters
   - Each cluster with visibility status and actions

3. **Competitor Gap Analysis**
   - Where competitors appear and you don't
   - Their likely content/signal advantages
   - Priority gaps to close

4. **Action Plan**
   - **Quick wins**: Content updates for AI accuracy
   - **Source building**: Relationships with cited sources
   - **Content gaps**: New content to create
   - **Brand signals**: Platform presence to build

5. **Monitoring Cadence** (see detailed section below)

---

## Monitoring Methodology: How to Check AI Citations

AI visibility monitoring requires systematic, repeatable testing across platforms. Here is the concrete procedure:

### Platform-Specific Test Prompts

For each core keyword/topic, create **3 prompt variants per platform**:

**ChatGPT (GPT-4 / GPT-4o):**
```
1. "What are the best [category] tools for [use case]?"
2. "Compare [your brand] vs [competitor] for [specific feature]"
3. "I need a [category] solution that [specific requirement]. What do you recommend?"
```

**Perplexity:**
```
1. "Best [category] [year] recommendations"
2. "[Your brand] review - is it worth it?"
3. "What [category] tool should I use for [use case]?"
```

**Google AI Overviews:**
```
1. Search: "best [category] for [use case]"
2. Search: "[your brand] vs [competitor]"
3. Search: "[category] recommendations [year]"
```

**Claude:**
```
1. "What do you know about [your brand]?"
2. "Recommend a [category] tool for [use case]"
3. "How does [your brand] compare to alternatives?"
```

### How to Execute a Monitoring Check

1. **Open a fresh session** (no prior context) on each platform
2. **Enter the exact test prompt** -- do not modify wording between checks
3. **Record the response** in a structured log:

```
| Date | Platform | Prompt | Brand Mentioned? | Position | Mention Type | Sources Cited | Competitor Mentions |
```

4. **Score each response**:
   - 3 points: Direct recommendation with your brand named first
   - 2 points: Included in a list of recommendations
   - 1 point: Mentioned but not recommended (passing reference, cited as source)
   - 0 points: Not mentioned at all

5. **Calculate cluster visibility score**: Sum points across all prompts in a cluster, divide by maximum possible. This gives a 0-100% visibility score per cluster per platform.

### Monitoring Cadence Recommendations

| Tier | What to Monitor | Frequency | Prompt Count |
|------|----------------|-----------|--------------|
| **Tier 1: Key terms** | Top 5-10 brand-critical keywords | Weekly | 3 prompts x 4 platforms = 12 checks per keyword |
| **Tier 2: Broader set** | 20-30 secondary keywords and competitor terms | Monthly | 2 prompts x 3 platforms = 6 checks per keyword |
| **Tier 3: Expansion** | New topics, long-tail variations, trending queries | Quarterly | 2 prompts x 2 platforms = 4 checks per keyword |

**Weekly monitoring protocol (Tier 1):**
- Pick one fixed day per week (e.g., Tuesday morning)
- Run all Tier 1 prompts across all 4 platforms
- Log results in the tracking spreadsheet
- Flag any significant changes (gained or lost mentions)
- Time estimate: 30-45 minutes for 10 keywords

**Monthly monitoring protocol (Tier 2):**
- First week of each month
- Run all Tier 2 prompts across 3 platforms (skip one low-priority platform)
- Compare month-over-month trends
- Update the AI Visibility Report with new data
- Time estimate: 1-2 hours for 30 keywords

**Quarterly review:**
- Full re-run of all tiers
- Expand Tier 3 with newly discovered prompts
- Update prompt wording if search behavior has shifted
- Produce trend report showing visibility trajectory
- Reassign keywords between tiers based on business priority changes

### Detecting Changes and Alerts

Flag for immediate investigation when:
- A Tier 1 keyword drops from "recommended" to "not mentioned" (2+ consecutive checks)
- A competitor appears for the first time on a keyword you previously owned
- A new AI platform launches or significantly changes its behavior
- Your content is being cited but with outdated or incorrect information

---

## Key Principles

1. **Start small**: 20-30 prompts around one topic first
2. **Group, don't track individually**: Clusters > individual prompts
3. **Aggregated data wins**: Look for patterns, not single responses
4. **Expand later**: Once one vertical is covered, add the next
5. **Action over perfection**: The goal is actionable insights, not perfect data

## Three Pillars of Action

Every insight should map to one of these actions:

| Pillar | Description | Example |
|--------|-------------|---------|
| **Relationship building** | Connect with sources AI cites frequently | Guest post on a blog that ChatGPT quotes often |
| **Content updating** | Fix outdated info AI is showing about you | Update pricing page AI still shows 2024 prices from |
| **Gap filling** | Create content for topics where you're invisible | Write comparison guide for category AI always discusses |

## Integration with Other SEO Skills

This skill works alongside:
- `/42-seo-agi` -- For optimizing content structure for AI citations
- `/42-qrg` -- For E-E-A-T signals that drive AI trust
- `/42-competitor-pages` -- For creating comparison content that fills gaps
- `/42-page-analysis` -- For per-page optimization of AI-cited content
