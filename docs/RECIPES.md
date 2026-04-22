# Recipe Reference

Recipes are compound slide components that templates typically don't provide.

List available recipes:

```bash
amazing-deck recipes
```

## `kpi_cards`

Big-number dashboard with 2-4 metric cards.

```json
{
  "recipe": "kpi_cards",
  "recipe_params": {
    "title": "Q3 Commitments",
    "cards": [
      {"label": "BASELINE",    "value": "18%",     "subtext": "<metrics platform>, April"},
      {"label": "TARGET",      "value": "45%",     "subtext": "by Q3 end"},
      {"label": "AMBASSADORS", "value": "10 -> 20","subtext": "globally"}
    ]
  }
}
```

**Params:** `title?`, `cards[] = {label, value, subtext?, color?}`

## `comparison`

Two-column side-by-side comparison.

```json
{
  "recipe": "comparison",
  "recipe_params": {
    "title": "Cohort 2 - What we are and are not doing",
    "left":  {"header": "WHAT WE ARE DOING",     "items": ["Focus on Education", "Scale to 20"]},
    "right": {"header": "WHAT WE ARE NOT DOING", "items": ["Technical Depth", "Firmwide competitions"]}
  }
}
```

**Params:** `title?`, `left/right = {header, items[]}`, `left_color?`, `right_color?`

## `timeline`

Horizontal milestone timeline with dates and status.

```json
{
  "recipe": "timeline",
  "recipe_params": {
    "title": "Cohort 2 Milestones",
    "milestones": [
      {"date": "May 5",  "label": "Orientation", "status": "done"},
      {"date": "May 8",  "label": "Roundtable",  "status": "current"},
      {"date": "Jun 1",  "label": "Mid-cohort",  "status": "upcoming"},
      {"date": "Jul 15", "label": "Q3 Review",   "status": "upcoming"}
    ]
  }
}
```

**Params:** `title?`, `milestones[] = {date, label, status: done|current|upcoming}`

## `chart_bar`

Native PowerPoint bar or column chart.

```json
{
  "recipe": "chart_bar",
  "recipe_params": {
    "title": "BU Weekly Active Copilot Users",
    "categories": ["Jan", "Feb", "Mar", "Apr"],
    "series": [
      {"name": "Weekly Active", "values": [8, 12, 15, 18]}
    ],
    "orientation": "vertical"
  }
}
```

**Params:** `title?`, `categories[]`, `series[] = {name, values[]}`, `orientation: vertical|horizontal`

## `asks`

Large numbered ask cards for executive decks.

```json
{
  "recipe": "asks",
  "recipe_params": {
    "title": "Asks from Leadership",
    "asks": [
      {"number": 1, "title": "Formal time allocation",
       "body": "Sanction ~10% of role time, protected from BAU.",
       "why": "Without sanctioned time, the program depends on goodwill."}
    ]
  }
}
```

**Params:** `title?`, `asks[] = {number?, title, body, why?, color?}`
