---
name: 42-status
description: >
  Generate a complete status overview of an active SEO project. Reads STATE.md,
  capabilities.json, all reports/, exports/, and recent activity to produce a
  consolidated dashboard. Shows phase progress, findings count, API costs,
  blockers, and next actions. Use when user says "status", "overzicht",
  "where are we", "wat heb je gedaan", "progress", "/42-status", or asks
  for a project summary.
allowed-tools: Read, Bash, Glob, Grep
version: 1.0.0
tags: [status, dashboard, overview, orchestrator]
---

# 42 Status — SEO Project Dashboard

Genereert een compleet overzicht van de huidige staat van een SEO project. Leest alle bestanden in `42-reports/<domain>/` en presenteert een gestructureerd dashboard.

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/42-status` | Smart: 0 projects → instructie / 1 project → toon status / 2+ → toon lijst |
| `/42-status --list` | Toon alleen project lijst (uit `42-reports/INDEX.md`) |
| `/42-status <domain>` | Toon volledig overzicht voor specifiek domein |
| `/42-status <domain> --short` | Compacte versie (scores + blockers only) |
| `/42-status <domain> --findings` | Alleen findings tabel |
| `/42-status <domain> --costs` | Alleen API cost tracking |
| `/42-status <domain> --next` | Alleen "wat is de volgende stap" |

---

## Procedure

### Stap 1: Smart Routing

```
ARGUMENT GIVEN?
├── Yes (`<domain>`)
│   └── Verify 42-reports/<domain>/STATE.md exists
│       ├── Yes → Step 2 (load project)
│       └── No → "Project not found. Run /42-status --list to see active projects."
│
└── No (geen argument)
    └── Count subdirectories in 42-reports/
        ├── 0 → "No projects. Run /42-seo-project intake to start."
        ├── 1 → Auto-load that project, go to Step 2
        └── 2+ → Show project list from INDEX.md, ask which to view
```

**Project list display** (when 2+ projects exist or `--list` flag given):

```bash
# Read 42-reports/INDEX.md and show its "Active Projects" table
cat 42-reports/INDEX.md
```

If INDEX.md doesn't exist, build it on the fly:
```bash
for dir in 42-reports/*/; do
  domain=$(basename "$dir")
  if [ -f "$dir/STATE.md" ]; then
    last_mod=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$dir/STATE.md")
    tier=$(grep "capability_tier:" "$dir/STATE.md" | head -1 | awk '{print $2}')
    echo "$domain | tier $tier | last: $last_mod"
  fi
done
```

Then prompt: "Which project? (type domain or number)"

### Stap 2: Lees Core State Files

Voor het actieve project:
1. **`STATE.md`** — fase status, top_25, top_5, decisions, capability tier
2. **`capabilities.json`** — API keys status, tools available, blocked features
3. **`INTAKE.md`** — business context (type, taal, doelen)

### Stap 3: Inventariseer Reports + Drift-check

```bash
find 42-reports/<domain>/reports/ -name "*.md" -type f
find 42-reports/<domain>/exports/ -type f
find 42-reports/<domain>/reports/pages/ -name "*.md" -type f 2>/dev/null
```

Voor elke report file:
- Filename + last modified
- Eerste H1 (titel)
- Korte samenvatting indien beschikbaar (eerste paragraaf na intro)

**Drift detection** (BELANGRIJK — STATE.md loopt vaak achter op wat er echt gebeurd is):

Map reports/exports naar fases en vergelijk met STATE.md:

| Artefact | Impliceert fase |
|----------|-----------------|
| `reports/QUICK-SCAN.md` | Phase 0 (intake) |
| `exports/<ts>/` directory met >100 SF files | Phase 1 (SF crawl gedaan) |
| `reports/PAGE-HEALTH.md`, `exports/page-health-scores.csv` | Phase 1 top-25 selectie klaar |
| `reports/PAGE-ANALYSIS.md` | Phase 2 (discovery) |
| `reports/KEYWORD-RESEARCH*.md`, `exports/*keyword*.json` | Phase 3 (keywords) |
| `reports/pages/*-cwv.md`, SF `pagespeed_*.csv` | Phase 4 (technical) |
| JSON-LD output files | Phase 6 (entity/schema) |
| `reports/LINK-GRAPH.md`, SF `all_outlinks.csv` | Phase 7 (links) |
| `reports/COMPETITORS.md` | Phase 8 (competitive) |

Voor elke fase: als er artefacten bestaan maar STATE.md zegt `pending`/`blocked` → **DRIFT**. Toon de fase in de output met `⚠️ drift` en vermeld "STATE zegt X, maar Y bestaat".

Optioneel: als drift gevonden → vraag gebruiker "STATE.md syncen?" voor auto-update.

### Stap 4: Aggregeer Findings

Scan alle `.md` bestanden in `reports/` op:
- 🔴 Critical findings (severity markers)
- 🟡 High/Medium findings
- 🟢 Low findings / wins
- Skill-output scores (regex: `\d+/100`)

Tel:
- Total critical / high / medium / low
- Skills uitgevoerd (uit STATE.md phase status of report file count)
- Quick wins identifiable (zoek "P1", "Quick Win", "Critical")

### Stap 5: API Cost Tracking

Als DataForSEO/Firecrawl gebruikt:
1. Zoek in reports/ naar bedragen (bv. "API cost: €0.13")
2. Sommeer alle gevonden costs
3. Optioneel: roep DataForSEO `appendix/user_data` aan voor live saldo

**Belangrijk**: `.env` staat op project root (`/42-SEO-Skills/.env`), **niet** in `42-reports/<domain>/`. Bash subshells erven env vars niet automatisch — source eerst expliciet:

```bash
cd /path/to/42-SEO-Skills
set -a && . ./.env && set +a
curl -s -u "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" \
  "https://api.dataforseo.com/v3/appendix/user_data" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('balance: €' + str(round(d['tasks'][0]['result'][0]['money']['balance'], 2)))"
```

Note: het `money` object bevat géén `currency` veld — alleen `total`, `balance`, `limits`. DataForSEO bills dit account in **EUR**, dus hard-code `€` als prefix (niet `$`).

### Stap 6: Bepaal Next Action

Op basis van STATE.md phase status:
- Welke fases zijn `completed` / `in_progress` / `pending` / `blocked`?
- Wat is de eerste `pending` fase?
- Zijn er blockers (wachten op gebruiker input, SF crawl, API keys)?
- Wat zou de orchestrator als volgende stap doen?

---

## Output Format

```markdown
# 📊 42 SEO Project Status — <Domain>

> Last updated: <STATE.md last modified>
> Capability tier: <1/2/3>

## 🎯 Project Context
- **Domein**: <url>
- **Type**: <business_type>
- **Talen**: <active languages>
- **Doelen**: <primary goals>

## 📈 Phase Progress

| Phase | Status | Reports |
|-------|--------|---------|
| 0. Intake | ✅ completed | INTAKE.md |
| 1. Crawl & Top-25 | ⏳ blocked | wachten op SF |
| 2. Discovery | ⏸ pending | — |
| 3. Keywords | ✅ completed | KEYWORD-RESEARCH.md |
| 4. Technical | 🔄 partial | QUICK-SCAN.md |
| 5. Content & GEO | 🔄 partial | pages/homepage-cwv.md |
| 6. Entity | ⏸ pending | — |
| 7. Links | ⏸ pending | — |
| 8. Competitive | ⏸ pending | — |
| 9. Report | ⏸ pending | — |

## 🔥 Top Findings

| # | Finding | Severity | Pagina | Effort |
|---|---------|----------|--------|--------|
| 1 | ... | 🔴 Critical | ... | ... |

## 📁 Generated Files
<tree of reports/ + exports/>

## 💰 API Costs
| Source | Used | Saldo |
|--------|------|-------|
| DataForSEO | €0.14 | €17.62 |
| Firecrawl | (MCP) | n/a |

## 🚨 Blockers
- ⏳ Wachten op SF crawl
- (other blockers)

## ⏭️ Next Action
<concrete next step based on phase routing>

## 📊 Metrics
- Skills uitgevoerd: X / 49
- Documenten: Y
- Critical findings: Z
- Quick wins identifiable: N
```

---

## Mode: --short

Alleen:
- Phase progress tabel (compact)
- Top 3 findings
- Next action

## Mode: --findings

Alleen de findings tabel met severity sorting.

## Mode: --costs

Alleen API cost tracking + saldo check.

## Mode: --next

Alleen "wat is de volgende stap" met concrete commando suggestie.

---

## Edge Cases

- **Geen project gevonden**: "No active project. Run `/42-seo-project intake` to start."
- **Meerdere projecten**: Toon lijst + vraag welke
- **STATE.md missend**: "Project directory exists but STATE.md missing. Run `/42-seo-project init`."
- **Capabilities.json missend**: Toon waarschuwing maar continue zonder tier info

---

## Reference

- Phase definitions: zie `42-seo-project/SKILL.md`
- Findings format: zie `${CLAUDE_PLUGIN_ROOT}/skills/references/quality-gates.md`
- Severity definitions: 🔴 Critical (blocks ranking) / 🟡 High (significant impact) / 🟢 Medium-Low
