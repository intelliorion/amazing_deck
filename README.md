# amazing-deck

**Analyze any PowerPoint template, then generate on-brand decks from it — including charts, timelines, KPI cards, and milestone slides.**

`amazing-deck` turns a corporate `.pptx` template into a reusable "knowledge hub," then lets you produce branded decks from structured content. It ships with a library of recipes for the visual patterns templates usually don't provide out of the box.

---

## Why

Most corporate decks are painful because:

- Templates only give you placeholders — they don't give you charts, timelines, or milestone visuals.
- Every deck starts from scratch instead of composing reusable components.
- LLMs generating decks don't know your template's rules — colors, fonts, what "on-brand" means.

This tool solves all three:

1. **Analyze** your template once. Get a knowledge hub of layouts, colors, fonts, and a ready-to-use generation prompt.
2. **Generate** decks by composing layouts *and* recipes (chart, timeline, KPI cards, comparison, asks).
3. **Reuse** the hub across projects, teammates, or any LLM (Claude, GPT, Gemini).

---

## Quickstart

```bash
git clone https://github.com/YOUR_USERNAME/amazing-deck.git
cd amazing-deck
pip install -e .

# 1. Drop your .pptx template into templates/
cp ~/Desktop/firm_template.pptx templates/

# 2. Analyze it
amazing-deck analyze

# 3. Inspect the knowledge hub
ls knowledge-hub/firm_template/

# 4. Generate a deck from a content brief
amazing-deck generate \
  --template templates/firm_template.pptx \
  --content examples/simple_example.json \
  --output output/my_first_deck.pptx
```

Open `output/my_first_deck.pptx` in PowerPoint.

---

## The two features

### 1. Template analysis

```bash
amazing-deck analyze                          # analyze all templates in templates/
amazing-deck analyze --template T.pptx        # analyze a single template
```

Produces `knowledge-hub/<template>/`:

| File | What it contains |
|---|---|
| `overview.md` | Dimensions, layout count, use cases |
| `style-guide.md` | Theme colors (hex), fonts, sizing |
| `layouts/NN-name.md` | Per-layout description, placeholders, example JSON |
| `assets/images/` | Every image extracted from masters & layouts |
| `assets/colors.json` | Palette in machine-readable form |
| `assets/fonts.json` | Font specs |
| `generation-prompt.md` | **Ready-to-paste prompt for any LLM** to generate on-brand decks |
| `manifest.json` | Full structured manifest (for tooling) |

### 2. Deck generation

```bash
amazing-deck generate \
  --template path/to/template.pptx \
  --content  path/to/content.json \
  --output   path/to/deck.pptx
```

Content JSON supports:

- **Layouts** — fill template placeholders by role/name/index
- **Recipes** — compound visual components (see below)
- **Extras** — custom shapes when you need them

---

## Recipe library

Recipes are the visual patterns templates *don't* provide. v1 ships with:

| Recipe | Use for |
|---|---|
| `kpi_cards` | Big-number dashboards (3–4 metrics with labels + subtext) |
| `comparison` | Two-column "what we are / are not doing" |
| `timeline` | Horizontal milestones with dates and status |
| `chart_bar` | Native PowerPoint bar/column chart |
| `asks` | Numbered ask cards for executive decks |

See [`docs/RECIPES.md`](docs/RECIPES.md) for full schema + examples.

**Example:**

```json
{
  "recipe": "timeline",
  "recipe_params": {
    "title": "Cohort 2 Milestones",
    "milestones": [
      {"date": "May 5",  "label": "Orientation",  "status": "done"},
      {"date": "May 8",  "label": "Roundtable",   "status": "current"},
      {"date": "Jun 1",  "label": "Mid-cohort",   "status": "upcoming"},
      {"date": "Jul 15", "label": "Q3 review",    "status": "upcoming"}
    ]
  }
}
```

---

## Content format

See [`docs/CONTENT_FORMAT.md`](docs/CONTENT_FORMAT.md) for the full schema.

Summary:

```json
{
  "slides": [
    {"layout": "Title Slide",   "placeholders": {"title": "My Deck"}},
    {"recipe": "kpi_cards",     "recipe_params": {}},
    {"layout": 1, "placeholders": {"0": "Title", "1": ["Bullet", "Bullet"]}}
  ]
}
```

---

## Claude Code integration

A `SKILL.md` ships in this repo. To use with Claude Code:

```bash
mkdir -p ~/.claude/skills/amazing-deck
cp SKILL.md ~/.claude/skills/amazing-deck/
```

Then any `.pptx` deck request will route through the tool.

---

## Examples

- `examples/simple_example.json` — 3-slide smoke test
- `examples/cs_ambassador_example.json` — a 9-slide executive deck using layouts *and* recipes

Try it:

```bash
amazing-deck generate \
  --content examples/cs_ambassador_example.json \
  --output output/cs_example.pptx
```

---

## Project status

- **v0.1 (now)** — analyze + generate + 5 recipes. Working end-to-end.
- **v0.2 (roadmap)** — quadrant, process_flow, chart_line/pie, validation, quality audit.
- **v0.3 (roadmap)** — markdown-outline content format, multi-template merging.

---

## Contributing

PRs welcome. New recipes especially — see `src/amazing_deck/recipes.py` for the decorator pattern. A recipe is ~80 lines and must take `(slide, params, theme)`.

---

---

## Install as an agent skill

`amazing_deck` ships with skill-style instructions so any AI coding agent can recognize and invoke it. Drop the repo (or just the relevant file) into your agent's config and it will know what the tool does and how to use it.

| Agent | File to use | Where to put it |
|---|---|---|
| **Claude Code** | `SKILL.md` | Copy to `~/.claude/skills/amazing_deck/SKILL.md` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Already in the repo — Copilot picks it up when the repo is open |
| **Cursor, Codex, other agents** | `AGENTS.md` | At the repo root — most modern agents read it automatically |

All three files tell the agent: when the user asks to build a deck, run `amazing-deck analyze` on any template they provide, then draft a `content.json` using template layouts + recipes, then call `amazing-deck generate` — and enforce the quality rules (max 7 bullets per slide, theme colors only, etc.).


## License

MIT
