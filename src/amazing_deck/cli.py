"""CLI entry point for amazing-deck."""
import argparse
import json
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="amazing-deck",
        description="Analyze .pptx templates and generate on-brand decks.")
    sub = parser.add_subparsers(dest="cmd")

    pa = sub.add_parser("analyze", help="Analyze templates -> knowledge hub")
    pa.add_argument("--templates-dir", type=Path, default=Path("./templates"))
    pa.add_argument("--hub-dir", type=Path, default=Path("./knowledge-hub"))
    pa.add_argument("--template", type=Path,
                    help="Single template file (overrides templates-dir)")

    pg = sub.add_parser("generate", help="Generate a deck from content JSON")
    pg.add_argument("--template", type=Path, help="Template .pptx (optional)")
    pg.add_argument("--content", type=Path, required=True)
    pg.add_argument("--output", type=Path, required=True)
    pg.add_argument("--quiet", action="store_true")
    pg.add_argument("--keep-template-slides", action="store_true",
                    help="Preserve the template's pre-existing slides "
                         "(default: clear them so output has only generated content)")

    sub.add_parser("init", help="Scaffold working directories")
    sub.add_parser("recipes", help="List available recipes")

    args = parser.parse_args(argv)

    if args.cmd == "analyze":
        from .analyze import analyze_all
        from .extract import analyze_template
        if args.template:
            out = args.hub_dir / args.template.stem
            analyze_template(args.template, out)
            print(f"Knowledge hub: {out}")
        else:
            analyze_all(args.templates_dir, args.hub_dir)

    elif args.cmd == "generate":
        from .generate import generate_deck
        content = json.loads(args.content.read_text())
        generate_deck(args.template, content, args.output,
                      verbose=not args.quiet,
                      keep_template_slides=args.keep_template_slides)

    elif args.cmd == "init":
        for d in ["templates", "knowledge-hub", "output"]:
            p = Path(d)
            p.mkdir(exist_ok=True)
            (p / ".gitkeep").touch()
        print("Scaffolded: templates/  knowledge-hub/  output/")

    elif args.cmd == "recipes":
        from .recipes import REGISTRY
        print("Available recipes:")
        for name in sorted(REGISTRY):
            doc = (REGISTRY[name].__doc__ or "").strip().split("\n")[0]
            print(f"  {name:<15}  {doc}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
