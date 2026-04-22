# AGENTS.md

Instructions for AI coding agents (Claude Code, GitHub Copilot, Cursor, Codex, etc.)
working with this repository.

## What this project is

`amazing_deck` is a CLI tool that (1) analyzes any PowerPoint `.pptx` template into a
structured knowledge hub, and (2) generates on-brand decks from content JSON + that
template, with a recipe library for charts, timelines, KPI cards, comparisons, and
executive asks.

Keywords that should trigger this tool: "build a deck", "generate slides",
"create a .pptx", "make a presentation", "turn my outline into slides",
"analyze our firm template".

## Setup

```bash
pip install -e .
# one-time, optional, for high-fidelity layout thumbnails:
# macOS:   brew install --cask libreoffice
# Linux:   sudo apt install libreoffice  (or equivalent)
# Windows: https://www.libreoffice.org/download/download/
```

## Two commands you will use

### 1. `amazing-deck analyze`

When the user has a `.pptx` template and wants branded output:

```bash
cp /path/to/their/template.pptx templates/
amazing-deck analyze
```

Read these files from the generated `knowledge-hub/<template_name>/` before drafting
content:

- `overview.md` — layout inventory with thumbnails at a glance
- `style-guide.md` — theme colors, fonts, per-layout background colors
- `layouts/NN-name.md` — each layout's placeholders + visual thumbnail
- `generation-prompt.md` — template-specific rules ready to paste into an LLM

### 2. `amazing-deck generate`

```bash
amazing-deck generate \
  --template templates/firm_template.pptx \
  --content  /tmp/content.json \
  --output   ~/Desktop/deck.pptx
```

Content JSON schema — see `docs/CONTENT_FORMAT.md`. Each slide is either:

- `{"layout": "<Layout Name>", "placeholders": {...}}` — uses a template layout
- `{"recipe": "<recipe_name>", "recipe_params": {...}}` — uses a compound component
- `{"layout": "Blank", "extras": [...]}` — fully custom shapes

## Recipe library

Run `amazing-deck recipes` for the current list. As of v0.1:

- `kpi_cards` — big-number dashboards
- `comparison` — 2-column doing/not-doing
- `timeline` — horizontal milestones with dates and status
- `chart_bar` — native PowerPoint bar/column chart
- `asks` — numbered executive ask cards

See `docs/RECIPES.md` for each recipe's parameters.

## Quality rules to enforce when generating content

1. **Max 7 bullets per slide.** If the user's outline has more, split into multiple slides.
2. **One message per slide.** If a slide would carry two messages, split.
3. **Use layout names exactly as listed** in the knowledge hub. Fuzzy matching exists but exact is safer.
4. **Use recipes for charts, timelines, KPIs** — never fake them with textboxes.
5. **Theme colors only.** Never invent hex values; use the palette from `assets/colors.json`.
6. **Body text >= 10pt; 14pt preferred** for projected decks. Titles inherit from template.
7. **Open with a commitment slide** (headline metric + target + date) and close with an `asks` recipe for any presentation to leadership.
8. **Always verify output** — after running `generate`, `ls -lh` the output file and (macOS) `open` it for user review.

## Fallbacks and failure modes

- **No template provided:** use the default blank template. Warn the user branding will be minimal.
- **Placeholder role mismatch:** log a warning, continue rendering the slide without that placeholder's content.
- **Unknown recipe name:** list available recipes and ask the user to pick.
- **LibreOffice not installed:** `analyze` still works; thumbnails fall back to PIL schematics (lower fidelity but show backgrounds + placeholder geometry correctly).

## Files NOT to touch

- `templates/*.pptx` — user's private templates (gitignored).
- `knowledge-hub/` — generated artifacts (gitignored, regenerable).
- `output/` — generated decks (gitignored).
- `examples/cs_ambassador_final.json` — locally-preserved sensitive content if it exists (gitignored).

## When asked to extend the tool

- **New recipe:** add a function decorated with `@recipe("name")` in `src/amazing_deck/recipes.py`. Take `(slide, params, theme)`. Keep each recipe ~80 LOC.
- **New layout matcher / analysis field:** edit `src/amazing_deck/extract.py`.
- **New CLI flag:** add to `src/amazing_deck/cli.py`, forward to the relevant function.
- **Run the test:** `amazing-deck generate --content examples/simple_example.json --output /tmp/test.pptx && open /tmp/test.pptx`.

## Project conventions

- Python 3.9+.
- Only two runtime dependencies: `python-pptx`, `Pillow`. Do not add more without strong reason.
- No async, no web framework, no LLM API calls — the tool is deterministic.
- PR-style commit messages; no force-push to main.
- Open source, MIT licensed.
