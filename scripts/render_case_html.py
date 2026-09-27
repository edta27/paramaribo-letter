#!/usr/bin/env python3
"""Write one HTML file per case study, and the case list, so crawlers see them without JS.

Vercel middleware rewrites /case?id=<id> to /case-pages/<id>. cases.js still runs on top
and renders the same markup, so readers see no change.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from urllib.parse import quote

from render_issue_html import BRAND, ID_OK, SITE, esc, fmt_date, json_ld

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CASES = PUBLIC / "cases"
OUT = PUBLIC / "case-pages"
TEMPLATE = PUBLIC / "case.html"
INDEX = PUBLIC / "cases.html"
IMAGE = f"{SITE}/images/masthead.png"
DEFAULT_DISCLAIMER = (
    "This case study is provided for educational and historical purposes only. "
    "It is not investment advice, and historical results do not guarantee future outcomes."
)


def load_catalog() -> list[dict]:
    rows = json.loads((CASES / "catalog.json").read_text())
    for row in rows:
        if not ID_OK.match(row.get("id") or ""):
            raise SystemExit(f"refusing case id that is not a safe slug: {row.get('id')!r}")
    return rows


def case_url(case_id: str) -> str:
    return f"/case?id={quote(case_id, safe='')}"


# The helpers below mirror cases.js so the page does not change when JS re-renders it.


def tags(pack: dict) -> str:
    bits = list(pack.get("investors") or []) + list(pack.get("companies") or [])
    if not bits:
        return ""
    return '<ul class="case-tags">' + "".join(f"<li>{esc(t)}</li>" for t in bits) + "</ul>"


def themes(pack: dict) -> str:
    if not pack.get("themes"):
        return ""
    return '<p class="case-themes">' + " · ".join(esc(t) for t in pack["themes"]) + "</p>"


def toc_html(toc: list) -> str:
    if not toc:
        return ""
    items = "".join(f'<li><a href="#{esc(r.get("id"))}">{esc(r.get("title"))}</a></li>' for r in toc)
    return f'<nav class="case-toc" aria-label="On this page"><h2>On this page</h2><ol>{items}</ol></nav>'


def timeline_html(items: list) -> str:
    if not items:
        return ""
    rows = []
    for r in items:
        src = f'<span class="tl-src">{esc(r.get("source"))}</span>' if r.get("source") else ""
        rows.append(
            f'<li><span class="tl-when">{esc(r.get("when"))}</span>'
            f'<span class="tl-what">{esc(r.get("what"))}</span>{src}</li>'
        )
    return '<ol class="case-timeline" aria-label="Decision timeline">' + "".join(rows) + "</ol>"


def figures_html(table: dict | None) -> str:
    if not table or not table.get("rows"):
        return ""
    head = "".join(f"<th>{esc(c)}</th>" for c in table.get("columns") or [])
    body = "".join("<tr>" + "".join(f"<td>{esc(str(c))}</td>" for c in row) + "</tr>" for row in table["rows"])
    return (
        f'<figure class="case-figure"><figcaption>{esc(table.get("caption") or "Key figures")}</figcaption>'
        f'<div class="case-table-wrap" tabindex="0"><table><thead><tr>{head}</tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
        f'<p class="case-figure-note">{esc(table.get("note") or "")}</p></figure>'
    )


def sources_html(sources: list) -> str:
    if not sources:
        return ""
    rows = []
    for s in sources:
        label = esc(s.get("title"))
        meta = " · ".join(esc(v) for v in (s.get("kind"), s.get("date")) if v)
        link = f'<a href="{esc(s["url"])}" rel="noopener noreferrer">{label}</a>' if s.get("url") else label
        rows.append(
            f"<li>{link}"
            + (f' <span class="src-meta">{meta}</span>' if meta else "")
            + (f" — {esc(s['note'])}" if s.get("note") else "")
            + "</li>"
        )
    return '<ol class="case-sources">' + "".join(rows) + "</ol>"


def article_html(pack: dict, row: dict) -> str:
    title = pack.get("title") or row.get("title") or row["id"]
    minutes = pack.get("readingMinutes") or row.get("readingMinutes") or "—"
    summary = (
        f'<section class="case-summary" id="summary">{pack["summaryHtml"]}</section>'
        if pack.get("summaryHtml")
        else ""
    )
    return f"""
        <div class="kicker">{esc(pack.get("kicker") or "Investor Case Studies")}</div>
        <h1 id="title">{esc(title)}</h1>
        <p class="lede">{esc(pack.get("subtitle") or pack.get("dek") or "")}</p>
        <div class="meta">{esc(fmt_date(pack.get("date") or row.get("date") or ""))} · {minutes} min read · {esc(BRAND)}</div>
        {tags(pack)}
        {themes(pack)}
        {toc_html(pack.get("toc") or [])}
        {summary}
        {timeline_html(pack.get("timeline") or [])}
        {figures_html(pack.get("figures"))}
        <div class="body">{pack.get("bodyHtml") or ""}</div>
        <section id="sources">
          <h2>Sources and further reading</h2>
          {sources_html(pack.get("sources") or [])}
        </section>
        <p class="disclaimer">{esc(pack.get("disclaimer") or DEFAULT_DISCLAIMER)}</p>
    """


def head_tags(pack: dict, row: dict) -> str:
    title = pack.get("title") or row.get("title") or row["id"]
    dek = pack.get("dek") or row.get("dek") or title
    doc_title = f"{title} · {BRAND}"
    canonical = f"{SITE}{case_url(row['id'])}"
    day = pack.get("date") or row.get("date") or ""
    ld = json_ld(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": dek,
            "image": [IMAGE],
            "datePublished": day,
            "dateModified": day,
            "author": {"@type": "Organization", "name": BRAND, "url": f"{SITE}/"},
            "publisher": {
                "@type": "Organization",
                "name": BRAND,
                "url": f"{SITE}/",
                "logo": {"@type": "ImageObject", "url": f"{SITE}/paramaribo-letter-logo-300.png"},
            },
            "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
            "keywords": ", ".join(pack.get("themes") or []),
            "isAccessibleForFree": True,
        }
    )
    return f"""<title>{esc(doc_title)}</title>
  <meta name="description" content="{esc(dek)}" />
  <link rel="canonical" href="{esc(canonical)}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="{esc(BRAND)}" />
  <meta id="og-title" property="og:title" content="{esc(doc_title)}" />
  <meta id="og-desc" property="og:description" content="{esc(dek)}" />
  <meta id="og-image" property="og:image" content="{IMAGE}" />
  <meta id="og-url" property="og:url" content="{esc(canonical)}" />
  <meta property="article:published_time" content="{esc(day)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(doc_title)}" />
  <meta name="twitter:description" content="{esc(dek)}" />
  <meta name="twitter:image" content="{IMAGE}" />
  <link rel="alternate" type="application/rss+xml" title="{esc(BRAND)}" href="{SITE}/feed.xml" />
  {ld}"""


def render_case(row: dict, template: str) -> str:
    pack = json.loads((CASES / f"{row['id']}.json").read_text())
    head_start = template.index("<title>")
    head_end = template.index('<link rel="icon"')
    page = template[:head_start] + head_tags(pack, row) + "\n  " + template[head_end:]
    return page.replace('<p class="chart-loading">Loading case study…</p>', article_html(pack, row))


def card_html(row: dict, featured: bool) -> str:
    return f"""
      <a class="case-card{" case-card--feature" if featured else ""}" href="{esc(case_url(row["id"]))}">
        <div class="feed-kicker">{esc(row.get("kicker") or "Case study")}</div>
        <h2>{esc(row.get("title"))}</h2>
        <p>{esc(row.get("dek") or "")}</p>
        {themes(row)}
        <div class="feed-meta">{esc(fmt_date(row.get("date") or ""))} · {row.get("readingMinutes") or "—"} min read</div>
      </a>"""


def fill_between(text: str, name: str, html: str) -> str:
    start = f"<!-- {name}:start (generated by scripts/render_case_html.py) -->"
    end = f"<!-- {name}:end -->"
    if start not in text or end not in text:
        print(f"cases.html has no {name} markers; skipped")
        return text
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    return f"{head}{start}{html}\n    {end}{tail}"


def write_case_index(rows: list[dict]) -> None:
    """Fill the case-feature / case-list divs in cases.html."""
    text = INDEX.read_text()
    text = fill_between(text, "case-feature", card_html(rows[0], True) if rows else "")
    text = fill_between(text, "case-list", "".join(card_html(r, False) for r in rows[1:]))
    INDEX.write_text(text)
    print(f"wrote case list ({len(rows)} cases)")


def render_case_pages() -> list[str]:
    rows = load_catalog()
    template = TEMPLATE.read_text()
    OUT.mkdir(parents=True, exist_ok=True)
    keep = set()
    for row in rows:
        dest = OUT / f"{row['id']}.html"
        dest.write_text(render_case(row, template))
        keep.add(dest.name)
        print(f"wrote {dest.relative_to(ROOT)}")
    for stale in OUT.glob("*.html"):
        if stale.name not in keep:
            stale.unlink()
            print(f"removed {stale.relative_to(ROOT)}")
    write_case_index(rows)
    return [row["id"] for row in rows]


if __name__ == "__main__":
    render_case_pages()
