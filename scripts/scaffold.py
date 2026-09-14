#!/usr/bin/env python3
"""Copy the charter's tokens and components into a project.

Usage:
    python scripts/scaffold.py svelte <project-src-dir>   # e.g. frontend/src
    python scripts/scaffold.py react  <project-src-dir>   # e.g. src

Svelte: writes app.css (tokens), src/lib/{cn,ui,labels,theme.svelte,highlight,time}.ts,
        src/components/ui/*.svelte and the entity components. Existing files are
        left alone unless --force is given, so a project keeps its own edits.
React:  writes globals.css and lib/labels.ts, and prints the shadcn commands for
        the base-nova primitives, which the CLI generates better than a copy.

Standard library only.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ASSETS = HERE / "assets"

SVELTE_FILES: list[tuple[str, str]] = [
    ("tokens/app.css", "app.css"),
    ("svelte/lib/cn.ts", "lib/cn.ts"),
    ("svelte/lib/ui.ts", "lib/ui.ts"),
    ("svelte/lib/labels.ts", "lib/labels.ts"),
    ("svelte/lib/theme.svelte.ts", "lib/theme.svelte.ts"),
    ("svelte/lib/highlight.ts", "lib/highlight.ts"),
    ("svelte/lib/time.ts", "lib/time.ts"),
]
SVELTE_UI = ["Button", "Badge", "Card", "Segmented", "Tabs", "Region", "StepChip", "CodeBlock", "CopyButton"]
SVELTE_COMPONENTS = ["EntityLabel", "EntityRow", "EntityHighlight", "FacetSection", "ThemeToggle", "GithubIcon"]

REACT_FILES: list[tuple[str, str]] = [
    ("tokens/globals.css", "app/globals.css"),
    ("react/lib/labels.ts", "lib/labels.ts"),
]
REACT_COMPONENTS = ["region", "step-chip", "entity-row", "entity-highlight", "field-label", "section", "copy-button"]


def copy(src: Path, dst: Path, force: bool) -> str:
    if dst.exists() and not force:
        return f"kept    {dst}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return f"wrote   {dst}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stack", choices=["svelte", "react"])
    parser.add_argument("target", type=Path, help="the project's source directory")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args()
    target: Path = args.target
    if not target.is_dir():
        print(f"error: {target} is not a directory", file=sys.stderr)
        return 2

    if args.stack == "svelte":
        pairs = list(SVELTE_FILES)
        pairs += [(f"svelte/ui/{n}.svelte", f"components/ui/{n}.svelte") for n in SVELTE_UI]
        pairs += [(f"svelte/components/{n}.svelte", f"components/{n}.svelte") for n in SVELTE_COMPONENTS]
        for src, dst in pairs:
            print(copy(ASSETS / src, target / dst, args.force))
        print(
            "\nnext: pnpm add @fontsource-variable/geist @fontsource-variable/geist-mono @lucide/svelte\n"
            "      import './app.css' from main.ts; components import from ../lib and ./ui"
        )
        return 0

    for src, dst in REACT_FILES:
        print(copy(ASSETS / src, target / dst, args.force))
    for name in REACT_COMPONENTS:
        print(copy(ASSETS / f"react/components/{name}.tsx", target / f"components/playground/{name}.tsx", args.force))
    print(
        "\nnext: pnpm dlx shadcn@latest init  (style base-nova, base colour neutral, css variables)\n"
        "      pnpm dlx shadcn@latest add button badge card tabs separator\n"
        "      pnpm add lucide-react next-themes; load Geist and Geist_Mono with next/font/google"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
