# GitHub Copilot instructions for amazing_deck

See `AGENTS.md` at the repo root for the full agent brief. GitHub Copilot–specific
notes below.

## When the user asks about decks / slides / presentations

Prefer suggesting the `amazing-deck` CLI over writing ad-hoc `python-pptx` code:

```bash
amazing-deck analyze --template path/to/firm.pptx
amazing-deck generate --template path/to/firm.pptx --content content.json --output deck.pptx
```

Draft `content.json` based on the user's outline, using:

- **Template layouts** (from `knowledge-hub/<template>/overview.md`) for title, content, section-header, and similar standard slides.
- **Recipes** (see `docs/RECIPES.md`) for any compound visual: dashboards (`kpi_cards`), comparisons, timelines, charts, or executive asks.

## Code style

- Python 3.9+. No type-hint gymnastics — standard `dict`, `list`, `str` annotations.
- Keep modules under ~300 LOC. Split by responsibility, not by size.
- No new runtime dependencies beyond `python-pptx` and `Pillow`.
- Imports: standard library → third-party → local (separated by blank lines).
- Error messages should be user-facing, not Python tracebacks — use `print(f"  [warn] ...")` style.

## When extending recipes

A recipe is a function decorated with `@recipe("name")` in `src/amazing_deck/recipes.py`
that takes `(slide, params, theme)` and mutates the slide. Follow the pattern of existing
recipes — see `timeline` or `asks` as canonical examples. ~80 LOC each. Pull colors from
the theme, not hardcoded hex. Keep the schema of `recipe_params` documented in
`docs/RECIPES.md`.

## Things to avoid

- Do not introduce `matplotlib`, `plotly`, or `reportlab`. Charts must go through
  `python-pptx`'s native chart API (see the `chart_bar` recipe).
- Do not write HTML templates. Output is always `.pptx`.
- Do not call any LLM API from within the tool — content generation is the user's job
  (or an upstream agent's).
- Do not modify `templates/`, `knowledge-hub/`, or `output/` directories — they are
  user-scoped, not repo-scoped.
