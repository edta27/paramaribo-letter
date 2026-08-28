#!/usr/bin/env python3
"""Append-only publisher for The Paramaribo Letter. Rebuilds the catalog. Never deletes an issue file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LETTER = ROOT / "public"
ISSUES = LETTER / "issues"
IMAGES = LETTER / "images"
CATALOG_JSON = LETTER / "catalog.json"
CATALOG_JS = LETTER / "catalog.js"

SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    s = SLUG_RE.sub("-", text.lower()).strip("-")
    return s[:80] or "issue"


def load_issue(meta_path: Path) -> dict:
    meta = json.loads(meta_path.read_text())
    body_path = meta_path.with_suffix(".body.html")
    if not body_path.exists():
        raise SystemExit(f"missing body file: {body_path.name}")
    meta["body"] = body_path.read_text()
    meta["file"] = meta_path.name
    return meta


def list_issues() -> list[dict]:
    rows = []
    for path in ISSUES.glob("*.json"):
        rows.append(load_issue(path))
    rows.sort(key=lambda r: (r.get("date") or "", r.get("id") or ""), reverse=True)
    return rows


def write_catalog(rows: list[dict]) -> None:
    public = [{k: r[k] for k in ("id", "date", "kicker", "title", "dek", "cover", "byline") if k in r} for r in rows]
    CATALOG_JSON.write_text(json.dumps(public, indent=2) + "\n")
    CATALOG_JS.write_text(
        "window.LETTER_ISSUES = "
        + json.dumps(rows, indent=2)
        + ";\n"
    )
    print(f"catalog {len(rows)} issues (append-only source: public/issues/)")


def paragraphs(text: str) -> str:
    chunks = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    html = []
    for chunk in chunks:
        if chunk.startswith("## "):
            html.append(f"<h2>{chunk[3:].strip()}</h2>")
        elif chunk.startswith("> "):
            html.append(f"<blockquote>{chunk[2:].strip()}</blockquote>")
        else:
            html.append("<p>" + chunk.replace("\n", " ") + "</p>")
    html.append(
        "<p>This letter is educational scenario research. It is not personalized advice and it does not recommend leverage.</p>"
    )
    return "\n".join(html) + "\n"


def add_issue(args: argparse.Namespace) -> None:
    day = args.date or date.today().isoformat()
    slug = args.slug or slugify(args.title)
    issue_id = f"{day}-{slug}"
    meta_path = ISSUES / f"{issue_id}.json"
    body_path = ISSUES / f"{issue_id}.body.html"
    if meta_path.exists() or body_path.exists():
        raise SystemExit(
            f"refusing to overwrite {issue_id}. Pick a new --slug. This publisher never deletes or replaces issues."
        )
    cover = args.cover or "images/cover-squeeze.png"
    if args.body_file:
        raw = Path(args.body_file).read_text()
        body = raw if "<p" in raw else paragraphs(raw)
    else:
        body = paragraphs(args.body or args.title)
    meta = {
        "id": issue_id,
        "date": day,
        "kicker": args.kicker or f"Vol. 1 · {day}",
        "title": args.title,
        "dek": args.dek or "",
        "cover": cover,
        "byline": args.byline or "The Paramaribo Letter",
    }
    ISSUES.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    body_path.write_text(body)
    print(f"wrote {meta_path.relative_to(ROOT)}")
    print(f"wrote {body_path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish a letter issue without deleting older ones")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild catalog.js from public/issues/")
    parser.add_argument("--title")
    parser.add_argument("--dek", default="")
    parser.add_argument("--kicker", default="")
    parser.add_argument("--byline", default="")
    parser.add_argument("--cover", default="")
    parser.add_argument("--date", default="")
    parser.add_argument("--slug", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--body-file", default="")
    parser.add_argument(
        "--notify",
        action="store_true",
        help="After rebuild, email subscribers via scripts/notify_subscribers.py (needs NOTIFY_SECRET)",
    )
    args = parser.parse_args()
    if args.title:
        add_issue(args)
    write_catalog(list_issues())
    if args.notify:
        import subprocess

        print("notifying subscribers…")
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "notify_subscribers.py")])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
