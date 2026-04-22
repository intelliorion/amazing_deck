# Content Format

The content JSON passed to `amazing-deck generate` describes every slide in the deck.

## Top level

```json
{
  "slides": [ ]
}
```

Each slide is one of three kinds:

| Kind | Required keys | Notes |
|---|---|---|
| **Layout** | `layout`, `placeholders` | Use a template layout |
| **Recipe** | `recipe`, `recipe_params` | Use a compound component |
| **Extras-only** | `layout` (use "Blank"), `extras` | Fully custom shapes |

All three kinds accept an optional `extras` array for additional custom shapes.

## Layout slide

```json
{
  "layout": "Title and Content",
  "placeholders": {
    "title": "Key Points",
    "content": ["First bullet", "Second bullet", "Third bullet"]
  }
}
```

### Placeholder keys (matching order)

1. **Role:** `title`, `subtitle`, `content`, `body`, `date`, `footer`, `slide_number`
2. **Exact name:** e.g. `"Title 1"`, `"Content Placeholder 2"`
3. **Index:** e.g. `"0"`, `"1"`

Find names/indexes in `knowledge-hub/<template>/layouts/NN-name.md`.

### Placeholder values

| Value | Effect |
|---|---|
| String | Plain text |
| List of strings | Bulleted list |
| `{"type": "table", "rows": []}` | Table replaces placeholder region |
| `{"type": "image", "path": "..."}` | Image replaces placeholder region |

## Recipe slide

```json
{
  "recipe": "kpi_cards",
  "recipe_params": {
    "title": "Q3 Commitments",
    "cards": [
      {"label": "BASELINE", "value": "18%", "subtext": "AIIP, April"},
      {"label": "TARGET",   "value": "45%", "subtext": "by Q3 end"}
    ]
  }
}
```

See [`RECIPES.md`](RECIPES.md) for each recipe's params.

## Extras

Use for custom shapes the layout doesn't provide:

```json
{
  "layout": "Blank",
  "extras": [
    {"type": "textbox", "x_in": 1, "y_in": 1, "w_in": 6, "h_in": 1,
     "text": "Callout", "font_size": 20, "bold": true, "color": "#1B3E6F"},
    {"type": "rectangle", "x_in": 0, "y_in": 7, "w_in": 13.33, "h_in": 0.1,
     "fill": "#1B3E6F"}
  ]
}
```
