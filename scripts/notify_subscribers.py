#!/usr/bin/env python3
"""Call the live /api/notify endpoint after a new Paramaribo Letter issue is published."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "catalog.json"
DEFAULT_SITE = "https://paramaribo-letter.vercel.app"


def load_issue(issue_id: str | None) -> dict:
    rows = json.loads(CATALOG.read_text())
    if not rows:
        raise SystemExit("catalog is empty")
    if issue_id:
        for row in rows:
            if row.get("id") == issue_id:
                return row
        raise SystemExit(f"issue not in catalog: {issue_id}")
    return rows[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Notify Paramaribo Letter subscribers")
    parser.add_argument("--issue-id", default="")
    parser.add_argument("--site", default=os.environ.get("SITE_URL", DEFAULT_SITE))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    secret = os.environ.get("NOTIFY_SECRET", "")
    if not secret and not args.dry_run:
        raise SystemExit("NOTIFY_SECRET is required")

    issue = load_issue(args.issue_id or None)
    payload = {"issue": {k: issue.get(k) for k in ("id", "date", "kicker", "title", "dek", "cover")}}
    url = args.site.rstrip("/") + "/api/notify"

    if args.dry_run:
        print(json.dumps({"url": url, "payload": payload}, indent=2))
        return 0

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {secret}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            body = res.read().decode("utf-8")
            print(body)
            data = json.loads(body)
            if not data.get("ok"):
                return 1
            return 0
    except urllib.error.HTTPError as err:
        print(err.read().decode("utf-8", errors="replace"), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
