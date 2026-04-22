"""Batch-analyze templates into knowledge hubs."""
from pathlib import Path
from .extract import analyze_template


def analyze_all(templates_dir, hub_dir):
    templates_dir = Path(templates_dir)
    hub_dir = Path(hub_dir)
    hub_dir.mkdir(parents=True, exist_ok=True)

    templates = sorted(templates_dir.glob("*.pptx")) + sorted(templates_dir.glob("*.potx"))
    if not templates:
        print(f"No .pptx/.potx templates found in {templates_dir}")
        return []

    results = []
    for tpl in templates:
        print(f"Analyzing {tpl.name}...")
        out = hub_dir / tpl.stem
        analyze_template(tpl, out)
        print(f"  -> {out}")
        results.append(out)
    print(f"\nDone. Analyzed {len(results)} template(s).")
    return results
