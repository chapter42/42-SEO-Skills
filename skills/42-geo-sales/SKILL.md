---
name: 42-geo-sales
description: >
  GEO sales pipeline management and proposal generation. CRM-lite prospect tracking
  with JSON storage, automatic proposal generation from audit data with pricing tiers
  and ROI projections. Use when user says "prospect", "proposal", "offerte",
  "pipeline", "sales", "client management".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
version: 2.0.0
tags: [sales, prospect, proposal, crm, geo]
---

# GEO Sales — Pipeline & Proposal Manager

## Purpose

Unified sales tool for GEO agencies. Manages the full sales lifecycle from lead discovery through proposal delivery, combining CRM-lite prospect tracking with automatic proposal generation from audit data.

All data is stored in `~/.geo-prospects/` (persistent across sessions).

---

## Commands

| Command | What It Does |
|---------|-------------|
| `/42:geo-sales --prospect add <domain>` | Create new prospect (interactive prompts) |
| `/42:geo-sales --prospect list [status]` | List all prospects or filter by status |
| `/42:geo-sales --prospect show <id-or-domain>` | Full prospect detail with history |
| `/42:geo-sales --prospect update <domain>` | Update prospect status |
| `/42:geo-sales --prospect audit <id-or-domain>` | Run quick GEO audit and save to prospect record |
| `/42:geo-sales --prospect note <id-or-domain> "<text>"` | Add interaction note with timestamp |
| `/42:geo-sales --prospect won <id-or-domain> <monthly-value>` | Mark as won, set contract value |
| `/42:geo-sales --prospect lost <id-or-domain> "<reason>"` | Mark as lost with reason |
| `/42:geo-sales --proposal <domain>` | Generate client proposal from audit data |
| `/42:geo-sales --pipeline` | Pipeline overview with stages and revenue |

**Examples:**
```
/42:geo-sales --prospect add electron-srl.com
/42:geo-sales --prospect list qualified
/42:geo-sales --prospect update electron-srl.com
/42:geo-sales --proposal electron-srl.com
/42:geo-sales --pipeline
```

---

## Storage Structure

All data stored in `~/.geo-prospects/`:
```
~/.geo-prospects/
├── prospects.json          # Main CRM database
├── audits/                 # Quick audit snapshots
│   └── electron-srl.com-2026-03-12.md
└── proposals/              # Generated proposals
    └── electron-srl.com-proposal-2026-03-12.md
```

Create directory if it does not exist: `mkdir -p ~/.geo-prospects/audits ~/.geo-prospects/proposals`

---

## Data Structure

Each prospect is stored as a JSON record in `prospects.json`:

```json
{
  "id": "PRO-001",
  "company": "Electron Srl",
  "domain": "electron-srl.com",
  "contact_email": "info@electron-srl.com",
  "contact_name": "",
  "industry": "Educational Equipment Manufacturing",
  "country": "Italy",
  "status": "qualified",
  "geo_score": 32,
  "audit_date": "2026-03-12",
  "audit_file": "~/.geo-prospects/audits/electron-srl.com-2026-03-12.md",
  "proposal_file": "~/.geo-prospects/proposals/electron-srl.com-proposal-2026-03-12.md",
  "monthly_value": 0,
  "contract_start": null,
  "contract_months": 0,
  "notes": [
    {
      "date": "2026-03-12",
      "text": "Initial GEO quick scan. Score 32/100 - Critical tier. Strong candidate for GEO services."
    }
  ],
  "created_at": "2026-03-12",
  "updated_at": "2026-03-12"
}
```

---

## Pipeline Stage Definitions

| Status | Meaning | Typical Next Action |
|--------|---------|---------------------|
| `lead` | Discovered, not yet contacted | Run quick audit, assess opportunity |
| `qualified` | Audit done, confirmed pain points | Generate proposal |
| `proposal` | Proposal sent, awaiting decision | Follow up, answer questions |
| `won` | Contract signed, active client | Run full audit, start onboarding |
| `lost` | Deal closed lost | Log reason for future reference |

---

## Orchestration: Prospect Management

### `--prospect add <domain>`

1. Check if `~/.geo-prospects/prospects.json` exists, create if not (empty array)
2. Auto-detect company name from domain (e.g., `electron-srl.com` -> `Electron Srl`)
3. Assign next sequential ID: `PRO-001`, `PRO-002`, etc.
4. Ask user for:
   - Contact name (optional)
   - Contact email
   - Monthly contract value estimate (optional)
5. Set status to `lead`
6. Save to JSON file
7. Suggest next step: "Run `/42:geo-sales --prospect audit <domain>` to score this prospect"

### `--prospect list [status]`

Read `~/.geo-prospects/prospects.json` and render a summary table:

```
GEO Prospect Pipeline — April 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID       Domain                  Company           Status      Score  Value
───────  ──────────────────────  ────────────────  ──────────  ─────  ──────
PRO-001  electron-srl.com        Electron Srl      Qualified   32/100  €4.5K
PRO-002  acme.com                ACME Corp         Lead        —       —
PRO-003  bigshop.it              BigShop           Won         41/100  €6.0K

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pipeline: 1 lead | 1 qualified | 0 proposals | 1 won | 0 lost
Committed MRR: €6,000 | Pipeline Value: €4,500
```

If a status filter is provided, show only prospects with that status.

### `--prospect show <id-or-domain>`

Display full prospect detail including all notes, audit history, and proposal files.

### `--prospect update <domain>`

1. Find prospect by domain or ID
2. Present current status and ask for new status
3. Valid statuses: `lead`, `qualified`, `proposal`, `won`, `lost`
4. Update status field
5. Add auto-note: "Status changed to <status>"
6. Save and confirm

### `--prospect audit <id-or-domain>`

1. Run `/42:seo-geo quick <domain>` to get GEO snapshot score
2. Save score to prospect record: `geo_score`, `audit_date`
3. Save audit output to `~/.geo-prospects/audits/<domain>-<date>.md`
4. Update `audit_file` path in prospect record
5. Add auto-note: "Quick audit run. GEO Score: XX/100."
6. If score < 55: suggest "Score indicates strong sales opportunity. Run `/42:geo-sales --proposal <domain>` to generate proposal."

### `--prospect note <id-or-domain> "<text>"`

1. Find prospect by ID or domain
2. Append note with current ISO date
3. Save back to JSON
4. Confirm: "Note added to Electron Srl (PRO-001)"

### `--prospect won <id-or-domain> <monthly-value>`

1. Update status to `won`
2. Set `monthly_value` to provided amount
3. Set `contract_start` to today
4. Add auto-note: "Deal won at EUR <value>/month"
5. Save and confirm

### `--prospect lost <id-or-domain> "<reason>"`

1. Update status to `lost`
2. Add auto-note: "Deal lost. Reason: <reason>"
3. Save and confirm

---

## Orchestration: Pipeline Overview

### `--pipeline`

Visual revenue-focused pipeline summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEO AGENCY PIPELINE SUMMARY — April 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STAGE          COUNT   POTENTIAL VALUE   NOTES
─────────────  ─────   ───────────────   ─────────────────────
Lead             2      €8,000/mo        New discoveries
Qualified        1      €4,500/mo        Ready for proposal
Proposal Sent    1      €6,000/mo        Awaiting signature
Won              3      €18,500/mo       Active clients (MRR)
Lost             1      —                Budget freeze

COMMITTED MRR:        €18,500
PIPELINE (qualified+): €10,500
TOTAL POTENTIAL:      €29,000/mo -> €348,000/yr

Next actions:
-> PRO-003 (acme.com): Send proposal — score 38/100 (strong case)
-> PRO-007 (shop.it): Follow up — proposal sent 8 days ago
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

For dashboard functionality, the Python CRM dashboard can be used:
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/crm_dashboard.py`

---

## Orchestration: Proposal Generation

### `--proposal <domain>`

**Additional flags:** `[--tier basic|standard|premium] [--client-name "Name"] [--monthly EUR]`

**Examples:**
```
/42:geo-sales --proposal electron-srl.com
/42:geo-sales --proposal electron-srl.com --tier standard --client-name "Electron Srl"
```

### Step 1: Load Audit Data

1. Check if `~/.geo-prospects/audits/<domain>*.md` exists
2. If not, suggest running `/42:geo-sales --prospect audit <domain>` first
3. Extract from audit:
   - GEO Score (overall and per-category)
   - Top 3 critical findings
   - Quick wins list
   - Business type
   - Estimated organic traffic impact

### Step 2: Customize the Proposal

Auto-fill proposal template with:
- Company name (from domain or prospect record)
- GEO score and tier label
- 3 most critical pain points (translated to business language)
- Estimated revenue at risk from AI search shift
- Recommended service tier based on score:
  - Score 0-40 -> Recommend Premium (critical issues need full attention)
  - Score 41-60 -> Recommend Standard (significant gaps, needs monthly work)
  - Score 61-75 -> Recommend Basic (solid base, needs monitoring)
  - Score 76+ -> Offer Basic or quarterly retainer check-in

### Step 3: Generate Proposal File

Output to `~/.geo-prospects/proposals/<domain>-proposal-<date>.md`
Also update prospect record if it exists in `~/.geo-prospects/prospects.json`

---

## Proposal Template

Generate the following document, filling all `[PLACEHOLDERS]` with real audit data:

---

```markdown
# GEO Optimization Proposal
## [COMPANY NAME] — AI Search Visibility

**Prepared by:** [YOUR AGENCY NAME]
**Prepared for:** [CONTACT NAME], [COMPANY NAME]
**Date:** [DATE]
**Valid until:** [DATE + 30 DAYS]
**Reference:** GEO-PROP-[YYMMDD]-[DOMAIN]

---

## Executive Summary

[COMPANY NAME] operates in [INDUSTRY] and serves customers across [GEOGRAPHY].
Our GEO audit of [DOMAIN], conducted on [DATE], reveals a GEO Readiness Score
of **[SCORE]/100 ([TIER LABEL])**.

This means your website currently has [TIER DESCRIPTION — use score interpretation table].
As AI-powered search (ChatGPT, Google AI Overviews, Perplexity) now influences
**[X]% of online discovery** and is growing at 527% year-over-year, this gap
represents a measurable risk to your pipeline.

The three most urgent issues are:
1. **[CRITICAL FINDING 1]** — [Business impact in one sentence]
2. **[CRITICAL FINDING 2]** — [Business impact in one sentence]
3. **[CRITICAL FINDING 3]** — [Business impact in one sentence]

We recommend the **[TIER NAME] package** at **EUR [PRICE]/month**, which addresses
all critical issues within 90 days and positions [COMPANY] as an AI-visible
authority in [INDUSTRY].

---

## The Opportunity: Why GEO Matters for [COMPANY NAME]

### The AI Search Shift Is Already Happening

| Metric | Value |
|--------|-------|
| AI-referred traffic growth (2025) | +527% YoY |
| AI traffic conversion vs. organic | 4.4x higher |
| ChatGPT weekly active users | 900M+ |
| Google AI Overviews monthly reach | 1.5B users, 200+ countries |
| Gartner: traditional search traffic drop by 2028 | -50% |
| Marketers investing in GEO today | Only 23% |

**First-mover advantage is real.** Companies that invest in GEO now will
capture the AI search channel before competitors do.

### Your Current Position

| Metric | [COMPANY] | Industry Average | Top Performers |
|--------|-----------|------------------|----------------|
| GEO Score | [SCORE]/100 | 45/100 | 75+/100 |
| AI Crawlers Allowed | [X]/14 | 8/14 | 14/14 |
| Brand Mentions (AI platforms) | [STATUS] | Moderate | High |
| Schema Coverage | [STATUS] | Partial | Complete |
| llms.txt | [Yes/No] | 12% have it | 78% have it |

---

## Audit Findings Summary

### GEO Score Breakdown

| Category | Your Score | Weight | Weighted | Priority |
|----------|-----------|--------|---------|----------|
| AI Citability & Visibility | [SCORE]/100 | 25% | [WEIGHTED] | [HIGH/MED/LOW] |
| Brand Authority Signals | [SCORE]/100 | 20% | [WEIGHTED] | [HIGH/MED/LOW] |
| Content Quality & E-E-A-T | [SCORE]/100 | 20% | [WEIGHTED] | [HIGH/MED/LOW] |
| Technical Foundations | [SCORE]/100 | 15% | [WEIGHTED] | [HIGH/MED/LOW] |
| Structured Data | [SCORE]/100 | 10% | [WEIGHTED] | [HIGH/MED/LOW] |
| Platform Optimization | [SCORE]/100 | 10% | [WEIGHTED] | [HIGH/MED/LOW] |
| **TOTAL GEO SCORE** | | | **[SCORE]/100** | **[TIER]** |

### Critical Issues Found

[For each critical issue from audit:]

#### [ISSUE TITLE]
**What we found:** [Technical finding in plain language]
**Business impact:** [What this means for their revenue/visibility]
**Our fix:** [What we will do to resolve it]
**Timeline:** [When they will see improvement]

---

## Our Solution: Service Packages

We offer three engagement models based on the scope of optimization needed.

---

### BASIC — EUR 2,500/month
*Best for: Sites with score 61-75 needing targeted improvements*

**What's included:**
- Quarterly full GEO audit (4x/year)
- Quarterly client report with score tracking
- Schema.org implementation (Organization + key page schemas)
- AI crawler access optimization (robots.txt)
- llms.txt creation and maintenance
- Email support (48-hour response)

**Estimated GEO score improvement:** +10-20 points in 6 months
**Contract:** Minimum 6 months

---

### STANDARD — EUR 5,000/month (Recommended for [COMPANY])
*Best for: Sites with score 40-60 needing structured monthly work*

**Everything in Basic, plus:**
- Monthly full GEO audit + delta report
- Monthly strategy call (60 minutes)
- Content citability optimization (up to 10 pages/month)
- Brand authority building (Wikipedia, Wikidata, LinkedIn optimization)
- Platform-specific optimization (Google AIO, ChatGPT, Perplexity)
- E-E-A-T improvements (author pages, credentials, freshness signals)
- Slack channel for fast communication (24-hour response)

**Estimated GEO score improvement:** +25-40 points in 6 months
**Contract:** Minimum 6 months

---

### PREMIUM — EUR 9,500/month
*Best for: Sites with score 0-40 with critical issues, or competitive industries*

**Everything in Standard, plus:**
- Bi-weekly strategy calls
- Technical SEO implementation support (Core Web Vitals, SSR, speed)
- Full content strategy + production (4 optimized articles/month)
- Active brand building (Reddit, YouTube, industry citations)
- Competitor monitoring and response
- Dedicated account manager
- Priority support (4-hour response)

**Estimated GEO score improvement:** +40-60 points in 6 months
**Contract:** Minimum 12 months

---

## ROI Projection for [COMPANY NAME]

Based on your current GEO score of [SCORE]/100 and industry benchmarks:

| Scenario | 6-Month Score | AI Traffic Increase | Est. Additional Value/Month |
|----------|--------------|--------------------|-----------------------------|
| No action | [SCORE + 2]/100 | +5% (organic growth) | EUR [LOW] |
| Basic package | [SCORE + 15]/100 | +30-40% | EUR [MED] |
| Standard package | [SCORE + 32]/100 | +60-90% | EUR [HIGH] |
| Premium package | [SCORE + 50]/100 | +100-150% | EUR [VERY HIGH] |

**Assumptions:**
- Based on estimated [X] monthly organic visitors to [DOMAIN]
- AI search is projected to drive 25-40% of organic discovery by end of 2026
- AI-referred traffic converts at 4.4x the rate of regular organic traffic
- Calculations use conservative estimates — actual results may vary

**Payback period (Standard package):** [X] months based on current traffic

---

## Engagement Timeline

### Month 1 — Foundation
- Kick-off call and onboarding (Week 1)
- Full technical audit + baseline metrics capture
- Quick wins implementation: robots.txt, schema, llms.txt, meta descriptions
- Expected score improvement: +5-10 points

### Month 2-3 — Optimization
- Content citability rewrites (top 10 pages)
- E-E-A-T improvements: author pages, credentials, dates
- Platform-specific optimization (Google AIO, ChatGPT, Perplexity)
- Brand presence: LinkedIn, Wikipedia/Wikidata groundwork
- Expected score improvement: +15-25 points cumulative

### Month 4-6 — Authority Building
- Brand mention campaigns (Reddit, industry sites, YouTube)
- Topical authority content strategy
- Monthly reports showing score improvements
- Expected score improvement: +30-45 points cumulative

### Month 6 — Review
- Full re-audit with before/after comparison
- ROI report
- Renewal discussion

---

## Why Us

- **GEO specialists**: We focus exclusively on AI search optimization, not traditional SEO agencies adapting to GEO
- **Transparent reporting**: Monthly reports show exactly what changed and why
- **No lock-in beyond minimum**: Month-to-month after initial commitment
- **Proven methodology**: 11-dimension GEO audit covering all major AI platforms
- **Fast results**: Quick wins visible within 30 days

---

## Investment Summary

| Package | Monthly | 6-Month | 12-Month |
|---------|---------|---------|----------|
| Basic | EUR 2,500 | EUR 15,000 | EUR 30,000 |
| Standard | EUR 5,000 | EUR 30,000 | EUR 60,000 |
| Premium | EUR 9,500 | EUR 57,000 | EUR 114,000 |

*All prices exclude VAT. Payment terms: monthly, due within 15 days of invoice.*

---

## Next Steps

To move forward:

1. **Review this proposal** and share any questions
2. **Schedule a 30-minute call** to walk through findings together: [CALENDAR LINK]
3. **Sign the service agreement** (sent separately upon acceptance)
4. **Kick-off call** scheduled for your chosen start date

This proposal is valid for **30 days** from the date above.

---

## Terms & Conditions

- **Minimum commitment:** As stated per package above
- **Cancellation:** 30-day written notice after minimum term
- **Confidentiality:** All audit findings and client data are strictly confidential
- **Results:** We guarantee effort and methodology, not specific ranking outcomes
- **Reporting:** Monthly reports delivered by the 5th of each month
- **Access needed:** Read access to Google Analytics / Search Console (if available)

---

*This proposal was prepared using GEO-SEO analysis tools and reflects findings
from the audit of [DOMAIN] conducted on [DATE]. All scores and recommendations
are based on current industry best practices for Generative Engine Optimization.*
```

---

## Pricing Recommendation Logic

Base recommendation on GEO score:
- Score 0-40 -> Recommend **Premium** (critical issues require intensive work)
- Score 41-60 -> Recommend **Standard** (structured monthly optimization)
- Score 61-75 -> Recommend **Basic** (maintenance + targeted improvements)
- Score 76+ -> Offer **Basic** or quarterly retainer check-in

---

## Proposal Output

1. Save proposal to `~/.geo-prospects/proposals/<domain>-proposal-<date>.md`
2. Update prospect record: set `status` to `proposal`, save `proposal_file` path
3. Print confirmation:
   ```
   Proposal generated: ~/.geo-prospects/proposals/electron-srl.com-proposal-2026-03-12.md
   Prospect status updated: Qualified -> Proposal
   Recommended package: STANDARD (EUR 5,000/month) — Score 32/100

   Next: Share the proposal file or convert to PDF for client delivery.
   ```

---

## General Output Rules

- All commands print confirmation + current prospect status to terminal
- No external files unless explicitly saving audits/proposals
- JSON database is the single source of truth
- Pipeline and list commands always read fresh from `prospects.json`
