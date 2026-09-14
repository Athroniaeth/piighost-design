#!/usr/bin/env python3
"""Check a front-end tree against the piighost charter.

Usage:
    python scripts/check_charter.py <dir> [--strict]

Reports, file and line by line:
  - inline `style=` attributes in .svelte/.tsx/.jsx/.html files: the production
    Content-Security-Policy is `style-src 'self'` with no `unsafe-inline`, so an
    inline style works in development and is blocked in production;
  - arbitrary pixel font sizes such as `text-[13px]`: the root font size scales
    on large displays, a px size ignores that and looks abruptly small;
  - em-dashes in user-facing text (.svelte, .tsx, dictionaries): the charter's
    copy rule, in both languages;
  - `asChild` in .tsx: the base-ui variant of shadcn uses the `render` prop;
  - raw hex colours outside token files: colours come from the CSS variables so
    light and dark stay in step.

Exit code is 1 when a finding exists (0 with --report-only). Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

UI_FILES = {".svelte", ".tsx", ".jsx", ".html"}
COPY_FILES = {".svelte", ".tsx", ".jsx", ".ts", ".js", ".json", ".md"}
TOKEN_FILES = {"app.css", "globals.css", "tokens.css"}
SKIP_DIRS = {"node_modules", "dist", "build", ".svelte-kit", ".next", "out", "generated", ".git", "coverage"}

CHECKS = [
    ("inline-style", re.compile(r"\sstyle\s*=\s*[\"'{]"), UI_FILES,
     "inline style attribute; the CSP allows no unsafe-inline, move it to a class"),
    ("px-font-size", re.compile(r"text-\[\d+(?:\.\d+)?px\]"), UI_FILES | {".ts", ".js"},
     "pixel font size; use the rem scale (text-sm, text-[0.8125rem]) so the root zoom applies"),
    ("as-child", re.compile(r"\basChild\b"), {".tsx", ".jsx"},
     "asChild; the base-ui variant composes with the `render` prop"),
]
EM_DASH = re.compile("[—–]")
HEX_COLOUR = re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{3}){1,2}\b")


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def scan(root: Path) -> list[tuple[Path, int, str, str]]:
    findings: list[tuple[Path, int, str, str]] = []
    for path in iter_files(root):
        suffix = path.suffix
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(lines, 1):
            for code, pattern, suffixes, message in CHECKS:
                if suffix in suffixes and pattern.search(line):
                    findings.append((path, number, code, message))
            if suffix in COPY_FILES and EM_DASH.search(line) and not line.lstrip().startswith(("//", "#", "*", "/*")):
                findings.append((path, number, "em-dash", "em-dash in copy; write a sentence, a comma or a colon instead"))
            if suffix in {".svelte", ".tsx", ".jsx", ".css"} and path.name not in TOKEN_FILES and HEX_COLOUR.search(line):
                if "url(" in line or "svg" in line.lower():
                    continue
                findings.append((path, number, "hex-colour", "raw hex colour; use a token (bg-primary, text-muted-foreground, var(--border))"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", type=Path, help="front-end directory to scan, e.g. frontend/src")
    parser.add_argument("--report-only", action="store_true", help="always exit 0")
    args = parser.parse_args()
    if not args.root.is_dir():
        print(f"error: {args.root} is not a directory", file=sys.stderr)
        return 2
    findings = scan(args.root)
    for path, number, code, message in findings:
        print(f"{path}:{number}: [{code}] {message}")
    by_code: dict[str, int] = {}
    for _, _, code, _ in findings:
        by_code[code] = by_code.get(code, 0) + 1
    if findings:
        summary = ", ".join(f"{count} {code}" for code, count in sorted(by_code.items()))
        print(f"\n{len(findings)} finding(s): {summary}")
        return 0 if args.report_only else 1
    print("charter: no finding")
    return 0


if __name__ == "__main__":
    sys.exit(main())
