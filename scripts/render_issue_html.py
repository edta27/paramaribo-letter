#!/usr/bin/env python3
"""Write one HTML file per issue so the first response already has the title and social tags.

Vercel middleware rewrites /issue?id=<id> to /issue-pages/<id>. Crawlers that do not run
app.js still see the catalog title, dek, cover, canonical, and Twitter tags.
"""

from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ISSUES = PUBLIC / "issues"
OUT = PUBLIC / "issue-pages"
SITE = "https://www.paramariboletter.com"
BRAND = "The Paramaribo Letter"
ID_OK = __import__("re").compile(r"^[a-z0-9][a-z0-9-]{0,120}$")


def esc(value: str) -> str:
    return html.escape(value or "", quote=True)


def fmt_date(iso: str) -> str:
    try:
        day = date.fromisoformat(iso)
    except ValueError:
        return iso
    return f"{day.strftime('%B')} {day.day}, {day.year}"


def absolute_cover(cover: str) -> str:
    path = (cover or "").strip() or "images/masthead.png"
    if path.startswith("https://") or path.startswith("http://"):
        return path
    return f"{SITE}/{path.lstrip('/')}"


def load_issues() -> list[dict]:
    rows = []
    for path in ISSUES.glob("*.json"):
        meta = json.loads(path.read_text())
        issue_id = meta.get("id") or ""
        if not ID_OK.match(issue_id):
            raise SystemExit(f"refusing issue id that is not a safe slug: {issue_id!r}")
        body_path = path.with_suffix(".body.html")
        meta["body"] = body_path.read_text() if body_path.exists() else ""
        rows.append(meta)
    rows.sort(key=lambda row: (row.get("date") or "", row.get("id") or ""), reverse=True)
    return rows


def render_issue(row: dict) -> str:
    issue_id = row["id"]
    title = row.get("title") or issue_id
    dek = row.get("dek") or title
    document_title = f"{title} · {BRAND}"
    canonical = f"{SITE}/issue?id={quote(issue_id, safe='')}"
    image = absolute_cover(row.get("cover") or "")
    cover_src = (row.get("cover") or "images/masthead.png").strip()
    kicker = row.get("kicker") or ""
    byline = row.get("byline") or BRAND
    meta_line = f"{fmt_date(row.get('date') or '')} · {byline}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(document_title)}</title>
  <meta name="description" content="{esc(dek)}" />
  <link rel="canonical" href="{esc(canonical)}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="{esc(BRAND)}" />
  <meta id="og-title" property="og:title" content="{esc(document_title)}" />
  <meta id="og-desc" property="og:description" content="{esc(dek)}" />
  <meta id="og-image" property="og:image" content="{esc(image)}" />
  <meta id="og-url" property="og:url" content="{esc(canonical)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(document_title)}" />
  <meta name="twitter:description" content="{esc(dek)}" />
  <meta name="twitter:image" content="{esc(image)}" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="stylesheet" href="/styles.css" />
  <script>
    try {{
      var t = localStorage.getItem("paramaribo-theme");
      document.documentElement.dataset.theme = t === "light" ? "light" : "dark";
    }} catch (e) {{
      document.documentElement.dataset.theme = "dark";
    }}
  </script>
  <script>
    window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
  </script>
  <script defer src="/_vercel/insights/script.js"></script>
</head>
<body data-nav="feed">
  <div class="portal-stage wrap">
    <article class="issue-page">
      <div class="kicker" id="kicker">{esc(kicker)}</div>
      <h1 id="title">{esc(title)}</h1>
      <p class="lede" id="dek">{esc(dek)}</p>
      <div class="meta" id="meta">{esc(meta_line)}</div>
      <img class="cover" id="cover" src="{esc(cover_src)}" alt="{esc(title)}" />
      <div class="body" id="body">
{row.get("body") or ""}
      </div>
      <p class="disclaimer">Educational scenario research. Not personalized financial advice. No execution, no position sizing, no leverage recommendation. Older issues remain in the archive and are not removed when a new letter is posted. <a href="/agents">Read who the agents are</a>.</p>
    </article>
    <section class="subscribe-box" id="new-subscribers" aria-labelledby="sub-title">
      <h2 id="sub-title">Subscribe</h2>
      <p class="subscribe-lede">Email when the next letter posts. Educational research only.</p>
      <form class="subscribe-form" data-subscribe-form>
        <label class="sr-only" for="sub-email">Email</label>
        <input id="sub-email" name="email" type="email" required placeholder="you@example.com" autocomplete="email" />
        <input class="hp" name="company" type="text" tabindex="-1" autocomplete="off" aria-hidden="true" />
        <button class="btn btn-primary" type="submit">Subscribe</button>
      </form>
      <p class="subscribe-status" data-sub-status aria-live="polite"></p>
      <p class="subscribe-unsub">Already on the list? <a href="/unsubscribe">Unsubscribe</a>.</p>
    </section>
    <footer class="site">
      <div>© The Paramaribo Letter</div>
      <div><a href="/#new-subscribers">Subscribe</a> · <a href="/unsubscribe">Unsubscribe</a> · <a href="/agents">Agents</a></div>
    </footer>
  </div>
  <script src="/catalog.js"></script>
  <script src="/app.js"></script>
  <script src="/subscribe.js"></script>
  <script src="/shell.js"></script>
  <script>Letter.renderIssue();</script>
</body>
</html>
"""


def write_middleware(ids: list[str]) -> None:
    listed = ",\n".join(f"  {json.dumps(issue_id)}" for issue_id in ids)
    text = f"""import {{ next, rewrite }} from "@vercel/functions";

// Generated by scripts/render_issue_html.py. Ids stay in sync with public/issue-pages/.
const ISSUE_IDS = new Set([
{listed}
]);

export const config = {{
  matcher: "/issue",
}};

export default function middleware(request) {{
  const id = new URL(request.url).searchParams.get("id") || "";
  if (!ISSUE_IDS.has(id)) return next();
  const dest = new URL("/issue-pages/" + id, request.url);
  dest.search = "";
  return rewrite(dest);
}}
"""
    (ROOT / "middleware.js").write_text(text)


def render_issue_pages() -> list[dict]:
    rows = load_issues()
    OUT.mkdir(parents=True, exist_ok=True)
    keep = set()
    for row in rows:
        issue_id = row["id"]
        dest = OUT / f"{issue_id}.html"
        dest.write_text(render_issue(row))
        keep.add(dest.name)
        print(f"wrote {dest.relative_to(ROOT)}")
    for stale in OUT.glob("*.html"):
        if stale.name not in keep:
            stale.unlink()
            print(f"removed {stale.relative_to(ROOT)}")
    ids = [row["id"] for row in rows]
    write_middleware(ids)
    print(f"wrote middleware.js ({len(ids)} issue ids)")
    return rows


def main() -> int:
    render_issue_pages()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
