# 42-SEO-Skills — Project Context voor Claude

## Wat is dit project?

De bronrepo voor de **`42-seo-skills` Claude Code plugin** — 59 skills voor SEO, GEO, content-analyse, crawling en reporting. Wordt gedistribueerd via Claude Code plugin marketplace (`/plugin install 42-seo-skills`), niet meer via symlinks.

## Mapstructuur (plugin-root)

```
42-SEO-Skills/
├── .claude-plugin/
│   └── plugin.json             ← plugin manifest (naam, versie, keywords)
├── skills/                     ← 59 skills, elk met SKILL.md
│   ├── 42-init/                ← bootstrap-skill voor klantprojecten
│   ├── 42-audit/ ...
│   └── references/             ← gedeelde kennisbank (eeat, cwv, quality-gates)
├── scripts/                    ← gedeelde Python (preflight.py, fetch_page.py, …)
├── hooks/                      ← gedeelde hooks
├── profiles/                   ← /42-init profielen (content/ecom/technical/full)
├── requirements.txt            ← Python deps (gedeelde venv)
├── .env.example                ← API-key template
├── README.md                   ← installatie + skill-overzicht
├── LICENSE                     ← MIT
└── CLAUDE.md                   ← dit bestand
```

**In `.gitignore` (niet in de plugin):**
`_archive/`, `input/`, `docs/`, `skillsCreator-definitions/`, `42-reports/`, `.env`, `NOSHARE/`, `.claude/` (oude pre-plugin symlinks).

## Naamgevingsregels

- Skills heten altijd `42-[naam]` (bijv. `42-audit`, `42-keyword-discovery`)
- Elke skill is een map met een `SKILL.md` bestand
- In SKILL.md verwijs je naar gedeelde resources met:
  - `${CLAUDE_PLUGIN_ROOT}/scripts/...` voor gedeelde Python scripts
  - `${CLAUDE_PLUGIN_ROOT}/skills/references/...` voor gedeelde kennisbank
- Skill-lokale scripts staan in `skills/<naam>/scripts/` en mogen relatief worden aangeroepen

## Distributie-architectuur

De plugin wordt gehost op GitHub (`chapter42/42-SEO-Skills`, public) en gedistribueerd via de Claude Code plugin marketplace:

```bash
/plugin marketplace add chapter42/42-SEO-Skills
/plugin install 42-seo-skills@42-SEO-Skills
/plugin update 42-seo-skills          # pakt nieuwe versies automatisch
```

**Lokaal testen** (voordat je pusht):
```bash
/plugin marketplace add file:///Users/royhuiskes/Claude\ Code/42-SEO-Skills
/plugin install 42-seo-skills
```

## Klantproject-flow

Per klantproject draait de gebruiker éénmalig `/42-init`. Die skill:

1. Vraagt naar project-profiel (content / ecom / technical / full)
2. Schrijft een skill-allowlist in `.claude/settings.local.json` (via `disabledSkills` met glob-patterns)
3. Kopieert `.env.example` naar `.env` en vraagt welke API-keys in te vullen
4. Installeert de gedeelde Python venv op `~/.claude/venvs/42-seo/` (of update 'm met `pip install -U`)
5. Maakt `42-reports/<klant-slug>/` aan

De venv is **gedeeld** over klantprojecten — één install, alle projecten gebruiken dezelfde dependencies. Voor uitzonderingen kan er project-lokaal een `./.venv` bijgemaakt worden.

## Wensen / Beslissingen

- **`skills/` is de bron van waarheid** — geen dubbele `dist/` meer
- **Python deps: gedeelde venv** op `~/.claude/venvs/42-seo/`, bootstrap via `/42-init`
- **Toggle-stijl**: `disabledSkills` met globs (`42-ecom-*`) — minder onderhoud bij nieuwe skills
- **`_archive/` altijd boven weggooien** — archiveer, gooi niet weg
- **Valuta is EUR (€)** — DataForSEO-account wordt in euro's afgerekend
- **Klantdata** (`42-reports/`, `.env`, `NOSHARE/`) nooit committen

## Versioning

Elke plugin-release bumpt `.claude-plugin/plugin.json`'s `version`. Volg [semver](https://semver.org/):
- Patch (1.0.0 → 1.0.1): bugfix in een skill
- Minor (1.0.1 → 1.1.0): nieuwe skill of nieuwe feature in bestaande skill
- Major (1.x → 2.0): breaking change (skill-rename, verwijderd profiel, etc.)
