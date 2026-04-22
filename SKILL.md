---
name: amazing-deck
description: |
  Generate on-brand PowerPoint decks from ANY firm/corporate .pptx template.
  Analyzes the template into a knowledge hub (colors, fonts, layouts, images),
  then generates decks using template layouts plus recipes for charts,
  timelines, KPI cards, comparisons, and executive asks. Use when the user
  asks to build a deck, create slides, generate .ppt/.pptx, convert an
  outline into a presentation, or work with a firm template.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# amazing-deck

Build .pptx decks by (1) analyzing a template to learn its rules, then
(2) generating branded decks from content + recipes.

## When to use

- User asks to generate a PowerPoint/deck/slides
- User has a firm template (.pptx) and wants on-brand output
- User wants charts, timelines, milestones, or KPI dashboards in a deck
- User wants a reusable deck-generation workflow

## Setup (once per environment)

```bash
python3 -c "import pptx" 2>/dev/null || pip3 install --user --break-system-packages python-pptx Pillow
```

Clone or locate the forge repo (typically `~/github/amazing-deck`).
Install in editable mode so the CLI is available:

```bash
cd ~/github/amazing-deck && pip install --user --break-system-packages -e .
```

## Workflow

### Step 1 — Analyze the template

If the user has a template, analyze it first:

```bash
cd ~/github/amazing-deck
cp "/path/to/user/template.pptx" templates/
amazing-deck analyze
```

Read the generated `knowledge-hub/<name>/overview.md` and
`knowledge-hub/<name>/generation-prompt.md` to understand the template's
layouts, colors, and style rules. Summarize the available layouts to the user.

### Step 2 — Draft content

Write content to a JSON file based on the user's outline. Use **layouts**
for standard slides (title, content, section headers) and **recipes** for:

- Dashboards/metric slides → `kpi_cards`
- Two-column comparisons → `comparison`
- Milestones/roadmaps → `timeline`
- Data visualizations → `chart_bar`
- Executive asks → `asks`

See `docs/RECIPES.md` for parameters.

### Step 3 — Generate and open

```bash
amazing-deck generate \
  --template templates/firm_template.pptx \
  --content /tmp/deck_content.json \
  --output ~/Desktop/deck.pptx

open ~/Desktop/deck.pptx   # macOS
```

## Quality rules the skill enforces

- **Max 7 bullets per slide.** Split into two slides if more.
- **Min 10pt body, 14pt for projected text.** Never smaller.
- **Use theme colors from the knowledge hub.** Never invent hex values
  that don't come from the template's palette.
- **One message per slide.** If a slide has two messages, split it.
- **Charts beat tables beat bullets** for numeric data.
- **Always verify output** — `ls -lh` and `open` the file before declaring done.

## Fallbacks

- **No template provided:** Use the default blank template. Warn the user
  that branding will be minimal.
- **Missing placeholder:** Log warning, continue. Don't fail the build.
- **Recipe not in registry:** List available recipes and ask user to pick one.
