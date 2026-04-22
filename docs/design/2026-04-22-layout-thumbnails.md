# Design: Layout Thumbnails + Background Extraction

**Date:** 2026-04-22
**Status:** Approved — ready for implementation

## Problem

`amazing-deck analyze` currently captures theme colors, fonts, layouts, placeholders, and embedded images. It misses two things that together account for most of a template's "personality":

1. **Backgrounds are invisible.** Per-layout background fills are stored in `<p:bg>` elements on the master and each layout — not as shapes we parse. For example, the `firm_template.pptx` we tested has:
   - Title layout → solid `accent5` blue (`#2C46FB`)
   - Title + Subtitle → solid `accent3` yellow (`#F6BF0E`)
   - Section / Agenda / Content → solid `tx1` dark
   - Image + Title + Content → `accent3` with luminance 20% (pale yellow)
2. **No way to *see* a layout before picking it.** Knowledge-hub consumers (humans and LLMs) get text-only descriptions. Choosing between `"Title"`, `"Title + Subtitle"`, `"Title Only"` becomes guesswork — which fuzzy-matching can't fix.

## Goals

1. Extract and resolve per-layout background colors, writing them to the manifest and style guide.
2. Generate a PNG thumbnail per layout, embedded in the knowledge-hub markdown for visual comparison at a glance.
3. Degrade gracefully when LibreOffice is not installed.

## Non-goals (explicitly deferred)

- Per-slide thumbnails of the template's existing sample slides.
- Pixel-accurate gradient / pattern / picture fill rendering in the fallback path.
- Thumbnail caching (re-render only on change).
- Slide-level background overrides (only master + layout level in v1).

## Architecture

New module **`src/amazing_deck/thumbnails.py`** (~200 LOC) with one public entry point:

```python
render_layout_thumbnails(prs, output_dir, bg_map) -> dict[int, Path]
    # returns {layout_idx: png_path_relative_to_output_dir}
```

Internally, at first call it checks `shutil.which("soffice")` once and caches the result. Dispatches each layout to either:

- `_render_with_soffice(prs, layout_idx, output_path)` — preferred, high fidelity
- `_render_schematic(layout, bg_color, output_path)` — PIL fallback

Background extraction is a separate, always-run function in `extract.py`:

```python
extract_backgrounds(prs, theme) -> dict
    # returns {"master": {"fill_type": "solid", "hex": "#000000"},
    #          "layouts": [{"index": 0, "fill_type": "solid", "hex": "#2C46FB"}, ...]}
```

## Data flow

```
analyze_template(template_path, hub_dir):
  prs = Presentation(template_path)
  theme       = extract_theme(prs)
  backgrounds = extract_backgrounds(prs, theme)         # NEW
  layouts     = [describe_layout(i, L) for ...]
  thumbnails  = render_layout_thumbnails(prs, hub_dir / "layouts" / "thumbnails", backgrounds)   # NEW

  write manifest.json          # now includes "backgrounds", "thumbnails" keys
  write overview.md             # now includes thumbnail grid at top
  write style-guide.md          # now includes background-color table
  write layouts/XX-name.md      # now includes thumbnail at top
  write assets/backgrounds.json # NEW
```

## Background extraction (solid-fill resolution)

For each `<p:bg>` element:

1. Detect fill type from child element: `<a:solidFill>`, `<a:gradFill>`, `<a:blipFill>`, `<a:pattFill>`, or missing (→ inherit).
2. For `solidFill`:
   - Extract color: `<a:srgbClr val="XXXXXX"/>` → direct hex, or `<a:schemeClr val="accent5"/>` → look up in `theme["colors"]["accent5"]`.
   - Apply `<a:lumMod val="X"/>` (keep X% of luminance) and `<a:lumOff val="Y"/>` (add Y% toward white). Formula implemented in HSL space.
3. For non-solid fills (gradient, picture, pattern): record the type as metadata; output hex `"#CCCCCC"` as the fallback color for schematic rendering. LibreOffice will render these correctly regardless.

Output: `backgrounds.json` with resolved hex per layout + the master.

## Schematic renderer (PIL fallback)

Canvas: 1333 × 750 pixels (16:9, 100 dpi).

Per layout:
1. Fill canvas with the resolved background hex.
2. Pick a contrasting outline color based on background luminance (light bg → dark stroke, dark bg → light stroke).
3. For each placeholder:
   - Draw outlined rectangle at scaled `(left, top, width, height)`.
   - Label with placeholder role (e.g., `title`, `content`) in the bottom-left corner at ~14px.
4. Save as PNG at 800 × 450 (downscaled for markdown embedding).

No attempt to render real fonts, custom shapes, or decorative brand elements.

## soffice renderer (high-fidelity path)

Per layout:
1. Build a minimal single-slide `.pptx` containing one empty slide using this layout, saved to a temp path.
2. Run `subprocess.run(["soffice", "--headless", "--convert-to", "png", "--outdir", tmpdir, pptx_path], timeout=30)`.
3. Move the resulting PNG to `output_dir/<NN>-<slug>.png`. If the PNG is larger than 1920 px wide, resize down.

Error handling: if the subprocess returns non-zero or times out, log a warning and fall back to the schematic renderer **for that layout only** — don't abort the whole run.

## Markdown embedding

**`overview.md`** gains a "Layouts at a glance" section near the top:

```markdown
## Layouts at a glance

| | | | |
|---|---|---|---|
| ![0](layouts/thumbnails/00-title.png) | ![1](layouts/thumbnails/01-agenda.png) | ![2](layouts/thumbnails/02-title-subtitle.png) | ![3](layouts/thumbnails/03-title-and-content-1.png) |
| **[0] Title** | **[1] Agenda** | **[2] Title + Subtitle** | **[3] Title and Content 1** |
| ... | ... | ... | ... |
```

**`layouts/XX-name.md`** gets a thumbnail at the very top, before the placeholder table:

```markdown
# Layout N: Name

![Thumbnail](thumbnails/NN-name.png)

- **Index:** N
- **Background:** solid `#2C46FB`
- ...
```

**`style-guide.md`** gains a Backgrounds section:

```markdown
## Backgrounds by layout

| Layout | Fill type | Color |
|---|---|---|
| [0] Title | solid | `#2C46FB` |
| [1] Agenda | solid | `#000000` |
| [2] Title + Subtitle | solid | `#F6BF0E` |
| ... | ... | ... |
```

## Output structure

```
knowledge-hub/<template_name>/
├── overview.md                    # + thumbnail grid
├── style-guide.md                 # + backgrounds table
├── manifest.json                  # + "backgrounds" + "thumbnails" keys
├── generation-prompt.md
├── assets/
│   ├── colors.json
│   ├── fonts.json
│   ├── backgrounds.json           # NEW
│   └── images/
└── layouts/
    ├── 00-title.md                # + thumbnail embed
    ├── 01-agenda.md
    ├── ...
    └── thumbnails/                # NEW directory
        ├── 00-title.png
        ├── 01-agenda.png
        └── ...
```

## Testing

Manual verification:
1. `amazing-deck analyze --template templates/firm_template.pptx` completes without error.
2. Open `knowledge-hub/firm_template/overview.md` in a Markdown viewer. All 15 thumbnails render. Title layout shows blue, Title + Subtitle yellow, Section dark — consistent with the backgrounds we traced.
3. `manifest.json` has a `backgrounds` field with 15 entries + master, each with `hex` and `fill_type`.
4. To verify the fallback: temporarily rename `/Applications/LibreOffice.app`, rerun `analyze`, confirm schematic PNGs appear with the correct background colors and placeholder outlines.

## Dependencies

- New optional external: **LibreOffice** for high-fidelity thumbnails.
  - macOS: `brew install --cask libreoffice`
  - Linux: `apt install libreoffice` / `dnf install libreoffice`
  - Windows: download from libreoffice.org
  - README to document this as optional.
- No new Python packages (Pillow already a dep).

## Backward compatibility

- `manifest.json` gains new keys; no removed/renamed keys. Existing consumers unaffected.
- `overview.md`, layout `.md`, `style-guide.md` gain new sections at known positions; existing sections untouched.
- `generate` command unaffected.

## Risks / follow-ups

- **Long analyze time with soffice.** 15 layouts × 1–2 s each ≈ 20–30 s. Acceptable for one-time template analysis. Future optimization: parallelize with `concurrent.futures`.
- **Windows soffice path detection.** `shutil.which("soffice")` should work but Windows installs often use `soffice.com` — add both to the PATH check.
- **macOS LibreOffice.app bundle path.** `brew install --cask libreoffice` symlinks `soffice` into `/usr/local/bin`, so `which` works. Users installing the .dmg manually may need to add to PATH — documented in README.
- **Eventual caching.** Re-running analyze currently re-renders all thumbnails. Acceptable today; add hash-based caching in a later spec.

## Out of scope for follow-up specs

- Slide-level background overrides (v1 covers master + layout only).
- Rendering decorative shapes (custom geometries, lines, curves) in the schematic path.
- Using extracted background colors inside recipes (auto-contrasting text color, etc.) — separate design.
