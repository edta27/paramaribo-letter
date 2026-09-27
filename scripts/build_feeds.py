#!/usr/bin/env python3
"""Build sitemap.xml and feed.xml from public/catalog.json. Free SEO / distribution surfaces."""

from __future__ import annotations

import html
import json
import xml.etree.ElementTree as ET
from datetime import date as Date
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
SITE = "https://www.paramariboletter.com"
CATALOG = PUBLIC / "catalog.json"


def load_issues() -> list[dict]:
    rows = json.loads(CATALOG.read_text())
    if not isinstance(rows, list):
        raise SystemExit("catalog.json must be a list of issues")
    return rows


def write_sitemap(issues: list[dict]) -> None:
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    def add(loc: str, lastmod: str | None = None, priority: str = "0.5") -> None:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = loc
        if lastmod:
            ET.SubElement(url, "lastmod").text = lastmod
        ET.SubElement(url, "priority").text = priority

    add(f"{SITE}/", issues[0]["date"] if issues else None, "1.0")
    add(f"{SITE}/agents", None, "0.8")
    add(f"{SITE}/charts", None, "0.75")
    add(f"{SITE}/cases", None, "0.8")
    add(f"{SITE}/desk", None, "0.6")
    cases_path = PUBLIC / "cases" / "catalog.json"
    cases = []
    if cases_path.exists():
        raw = json.loads(cases_path.read_text())
        if isinstance(raw, list):
            cases = raw
    for case in cases:
        add(f"{SITE}/case?id={case['id']}", case.get("date"), "0.75")
    for issue in issues:
        add(f"{SITE}/issue?id={issue['id']}", issue.get("date"), "0.7")

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    out = PUBLIC / "sitemap.xml"
    tree.write(out, encoding="utf-8", xml_declaration=True)
    print(f"wrote {out.relative_to(ROOT)} ({len(list(urlset))} urls)")


def rfc822(iso: str) -> str:
    """RSS 2.0 wants RFC 822 dates; readers and validators reject bare YYYY-MM-DD."""
    try:
        day = Date.fromisoformat(iso)
    except ValueError:
        return ""
    return format_datetime(datetime(day.year, day.month, day.day, 12, tzinfo=timezone.utc))


def write_rss(issues: list[dict]) -> None:
    items = []
    for issue in issues[:50]:
        link = f"{SITE}/issue?id={html.escape(issue['id'], quote=True)}"
        title = html.escape(issue.get("title") or issue["id"])
        dek = html.escape(issue.get("dek") or "")
        date = rfc822(issue.get("date") or "")
        items.append(
            f"""    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{html.escape(date)}</pubDate>
      <description>{dek}</description>
    </item>"""
        )
    body = "\n".join(items)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>The Paramaribo Letter</title>
    <link>{SITE}/</link>
    <description>Desk notes from a multi-agent research council on Bitcoin, macro liquidity, equities, and event risk. Educational scenario research, not advice.</description>
    <language>en-us</language>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml" />
    <docs>{SITE}/feed.xml</docs>
{body}
  </channel>
</rss>
"""
    out = PUBLIC / "feed.xml"
    out.write_text(xml)
    print(f"wrote {out.relative_to(ROOT)} ({min(len(issues), 50)} items)")


def main() -> int:
    issues = load_issues()
    write_sitemap(issues)
    write_rss(issues)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
