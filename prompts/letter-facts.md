# Paramaribo Letter — current facts (read first)

Every letter and growth agent reads this file before producing anything. When it disagrees with an older doc, prompt, or agent file, **this file wins**. Last updated: **2026-10-05**. Numbers below are dated; if the user pastes newer ones, use theirs.

## Site

- Canonical domain: **https://www.paramariboletter.com** (paramaribo-letter.vercel.app is only the deploy host). Hosted on **Vercel, Hobby plan**, deploying from `main` of **github.com/edta27/paramaribo-letter** (git remote `website`).
- Clean URLs. Use these forms in every public link:
  - Issue: `https://www.paramariboletter.com/issue?id={id}` (`/issue.html?id=` only redirects; do not use it)
  - Subscribe: `/#new-subscribers` · Unsubscribe: `/unsubscribe` · Agents: `/agents` · Cases: `/cases` · Charts: `/charts`
  - Topic guides: `/topics` plus five evergreen hubs: `/topics/bitcoin-four-year-cycle`, `/topics/bitcoin-crash-scenarios`, `/topics/bitcoin-etf-flows-leverage`, `/topics/bitcoin-macro-fed-yen`, `/topics/bitcoin-support-resistance`
  - Feed: `/feed.xml` · Sitemap: `/sitemap.xml`
- Topic hubs are the best landing links for broad questions ("is the four-year cycle over?") in replies, LinkedIn posts, and partner pitches. Link an issue for a specific call; link a topic hub for an evergreen question.
- Every issue page is prerendered for search engines: the issue **title** becomes the page `<title>` and the **dek** becomes the meta description and social-card text. Issues are filed into topic hubs automatically by keyword (`scripts/topics.json`).
- Google Search Console: verified. Sitemap resubmission is on Michael's list.

## Where the site code lives (important before publishing)

- **edta27/paramaribo-letter is the source of truth for site code** since 2026-09-26. It has code this repo (investment-research) does not: `scripts/render_issue_html.py`, `scripts/render_case_html.py`, `scripts/build_topics.py`, `scripts/topics.json`, `middleware.js`, `public/topics/`, `public/subscribed.html`, `public/clarity.js`, and newer `public/index.html`, `styles.css`, `shell.js`, `subscribe.js`, `vercel.json`.
- **Never copy `public/` or `vercel.json` wholesale from investment-research onto the website branch.** It would silently revert SEO, topic pages, signup tracking, and design fixes. Bring over only the new issue files (see `prompts/run-paramaribo-letter.md`, "After the draft").
- In the website checkout, `python3 scripts/publish_letter.py` rebuilds everything in one go: catalog, prerendered issue pages, case pages, homepage feed, topic hubs, `sitemap.xml`, `feed.xml`. Don't hand-edit generated issue pages, `middleware.js`, the homepage feed, or the topics row.
- Safety net: a "Rebuild generated site pages" GitHub Action on paramaribo-letter reruns `publish_letter.py --rebuild` after any push touching issues or catalog. It catches mistakes; it is not a reason to skip the rebuild. Full hands-off steps: `prompts/issue-newsletter-hands-off.md`, step 5.
- Site changes (SEO, topic pages, signup prompts, design) also land as pull requests on paramaribo-letter from Claude threads in Michael's project. Always `git fetch website` and start from `website/main` before publishing, or the push is rejected.

## Signups and measurement

- Signup flow: form → `/api/subscribe` (Resend) → redirect to **`/subscribed`** (noindex thank-you page). There is no thank-you modal any more.
- Signup forms: homepage, right after each issue article, a link under the issue byline, a dismissible reading bar on issue pages, topic pages, cases, charts.
- **Vercel Hobby does not record custom events.** Signups are counted as **page views of `/subscribed`** in Vercel Web Analytics. Subscribe rate = `/subscribed` visitors ÷ site visitors. Measurable since 2026-09-27; before that date there is no signup data.
- Microsoft Clarity (project `ya3iur94oo`) runs on pages with signup forms: session recordings plus tagged events (`subscribe_view`, `subscribe_form_start`, `subscribe_complete`, `subscribe_error`, `subscribe_bar_view`, `subscribe_bar_click`; `sub_location` = home, issue-end, topic, charts, cases, case).
- New-issue email: `/api/notify` via Resend from `updates.paramariboletter.com`. Reply-To inbox: paramariboletter@gmail.com.

## Traffic baseline and targets (Vercel Web Analytics)

| Week starting | Visitors | Page views |
|---|---|---|
| 24 Aug | 45 | 144 |
| 31 Aug | 78 | 329 |
| 7 Sep | 25 | 50 |
| 14 Sep | 15 | 31 |
| 21 Sep | 23 | 44 |

- Steady state after the launch spike: **about 20 visitors a week**.
- Referrers, 30 days to 27 Sep: direct/unknown 162, google.com 22, X (t.co) 20, LinkedIn 15, vercel.com 11, Gmail 5.
- **Targets:** 60 visitors/week by **11 Oct 2026**; 100 visitors/week by **25 Oct 2026** with at least 25 from Google; stretch 150/week. **10 new email signups** by 25 Oct. LinkedIn newsletter to **100** subscribers.
- Weekly metrics: visitors, search visitors (google + bing), social visitors (t.co + LinkedIn), `/issue` visitors, `/topics` visitors, `/subscribed` visitors and subscribe rate, LinkedIn newsletter subscribers (Michael reports it).

## Channels

- **LinkedIn Newsletter** "The Paramaribo Letter" (https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/): about **68 subscribers**, the largest audience, but it sends the fewest site visitors (~15/month). **Priority #1:** every LinkedIn edition and post links to the full issue on paramariboletter.com near the top, not only at the bottom.
- X: @paramaribolette. Inbox: paramariboletter@gmail.com.
- Google already sends more visitors than LinkedIn; search is priority #2 (topic hubs, clear titles and deks).
- Newsletter swaps, Medium import, Reddit: deferred until a few weeks of `/subscribed` data exist.

## Posting rule

Nothing goes out to X, LinkedIn, email, Reddit, or partners unless Michael writes `APPROVE_SEND` and names the item. Claude threads in the project never post outside the site; drafts go to Michael. Never claim a post went out without a permalink or Michael's confirmation.

## Latest issue

Read `public/catalog.json` (first entry is the newest). As of 2026-10-05: **Issue 28**, `2026-09-30-the-crash-that-doesnt-wait`. The `/topics/bitcoin-support-resistance` intro names levels "as of Issue 28"; when a new issue moves the level map, flag that it needs a refresh.
