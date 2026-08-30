# Free services stack — use every free tier that helps

Rule: **if it is free forever (or a free tier with no card required for our scale), use it.** Skip anything that needs paid ads, boosts, or paid seats. Do not invent metrics from empty dashboards.

Primary site: https://www.paramariboletter.com  
Overseer: Conductor marketing desk · Channels (X / LinkedIn / Gmail): Codex + human `APPROVE_SEND`

---

## Already in use (keep)

| Service | Free what | Job |
|---|---|---|
| [Vercel](https://vercel.com) Hobby | Hosting + Web Analytics + custom events | Site + `subscribe_form_start` / `subscribe_complete` |
| [Resend](https://resend.com) free | Contacts + transactional mail (quota) | Subscribe / notify |
| [GitHub](https://github.com/edta27/paramaribo-letter) | Repo + Actions | Source + notify workflow |
| Custom domain | DNS you already own | Canonical links |
| X / LinkedIn native analytics | Built into apps | Impressions (separate from email) |

---

## Sign up today (human + Codex) — all free

Do these once. Paste IDs into `public/site-config.js` (Clarity / GA4) or the measurement sheet. Conductor can wire code; you create accounts.

### A. Measurement & UX (highest value)

| # | Service | Sign up | Then |
|---|---|---|---|
| 1 | **[Microsoft Clarity](https://clarity.microsoft.com)** | Free Microsoft account → project for paramariboletter.com | Paste **Project ID** into `site-config.js` → `clarityProjectId`. Heatmaps + session replay. Mask email fields in Clarity settings. |
| 2 | **[Google Analytics 4](https://analytics.google.com)** (optional) | Free Google account → GA4 property | Paste `G-…` into `ga4MeasurementId`. Primary funnel stays Vercel events; GA4 is backup + referrers. |
| 3 | **[Google Search Console](https://search.google.com/search-console)** | Add `https://www.paramariboletter.com` → DNS or HTML verify | Submit `https://www.paramariboletter.com/sitemap.xml` |
| 4 | **[Bing Webmaster Tools](https://www.bing.com/webmasters)** | Import from Search Console or verify domain | Free discovery; no cost |
| 5 | **Measurement log** | [Google Sheets](https://sheets.google.com) (free) | Import `public/marketing/measurement-log.csv` as the Day 2+ log |

### B. Uptime & quality

| # | Service | Sign up | Then |
|---|---|---|---|
| 6 | **[UptimeRobot](https://uptimerobot.com)** | Free 50 monitors | HTTP(s) monitor every 5 min on `/` and `/api/subscribe` (keyword or status). Alert → Gmail. |
| 7 | **[PageSpeed Insights](https://pagespeed.web.dev)** | No account | Run monthly on home + one issue URL; fix only free wins |
| 8 | **[securityheaders.com](https://securityheaders.com)** | No account | Spot-check after deploys |
| 9 | **[mail-tester.com](https://www.mail-tester.com)** | Free tests (limited/day) | After Resend domain works, send one test issue notify → score SPF/DKIM/DMARC |
| 10 | **[MXToolbox](https://mxtoolbox.com)** | Free lookups | SPF / DKIM / DMARC for paramariboletter.com |

### C. Content & social (no paid boost)

| # | Service | Sign up | Then |
|---|---|---|---|
| 11 | **[Canva](https://www.canva.com)** Free | Account | Quote cards from Issue 10/12 pull quotes; export PNG for X/LinkedIn |
| 12 | **[Google Campaign URL Builder](https://ga-dev-tools.google/campaign-url-builder/)** | No account | Only when adding UTMs (`utm_source=x` / `linkedin` → `/#new-subscribers`) |
| 13 | **[opengraph.xyz](https://www.opengraph.xyz)** or LinkedIn Post Inspector | Free | Preview OG before sharing Issue 12 |
| 14 | **RSS readers** (Feedly free / NetNewsWire) | Optional | Subscribe to `https://www.paramariboletter.com/feed.xml` to verify the feed |
| 15 | **[httpstatus.io](https://httpstatus.io)** | Free | Batch-check `/`, `/agents`, issue URL, `/marketing` |

### D. Email hygiene (still free)

| # | Service | Notes |
|---|---|---|
| 16 | **Gmail** `paramariboletter@gmail.com` | Human inbox / Reply-To — Codex drafts |
| 17 | **Resend dashboard** | Contacts count only until welcome is approved |
| 18 | **Google Domains / registrar DNS** | Free checks for Resend TXT records (wherever DNS lives) |

---

## Built into the site (no signup)

| Asset | URL | Purpose |
|---|---|---|
| Sitemap | `/sitemap.xml` | Search Console |
| RSS | `/feed.xml` | Archive syndication |
| Robots | `/robots.txt` | Points at custom-domain sitemap |
| Site config | `/site-config.js` | Paste Clarity / GA4 IDs |
| Extra analytics loader | `/analytics-extra.js` | Loads Clarity/GA4 only if IDs set |
| CVR / welcome docs | `docs/` in letter repo + `marketing/` here | Dry-run |

Regenerate feeds after catalog changes:

```bash
python3 scripts/build_feeds.py
```

`publish_letter.py --rebuild` also refreshes feeds.

---

## Do not use (not free, or wrong stage)

- Paid X / LinkedIn boosts or ads managers  
- Plausible / Fathom paid plans (Clarity + Vercel cover this stage)  
- Beehiiv / Substack as a second list (splits Resend)  
- Engagement pods, bought followers, shoutout farms  
- Speed Insights **Plus** (paid) — skip unless later  
- Anything that asks for a credit card “for the free trial” when a forever-free tool exists  

---

## Owner checklist (paste when done)

```
Clarity project ID: ya3iur94oo   → LIVE on production via /clarity.js (2026-08-29)
GA4 ID (optional): _______________   → site-config.js
Search Console: [x] verified  [x] sitemap submitted (15 URLs · commits f62445a / 3ad25ba)
Bing Webmaster: [ ] verified
UptimeRobot: [x] www.paramariboletter.com HTTP Up · 100% / 24h · 0 incidents
              [ ] email alerts (optional)  [ ] optional /api/subscribe
Sheets log: [ ] imported measurement-log.csv (CSV updated locally)
Resend Contacts count: 4 (0 unsubs) · domain updates.paramariboletter.com verified
mail-tester score (after domain): ___/10
Vercel 7d: 25 visitors · 102 PV · 64% bounce · subscribe events N/A on plan
RESEND_REPLY_TO on Vercel: [ ] still missing
```


Deploy `site-config.js` after filling IDs (same path as other public files). Empty IDs = no Clarity/GA4 load (Vercel Analytics still runs).

---

## Paste into Codex (account setup + IDs)

```text
Help set up FREE-ONLY tools for The Paramaribo Letter. No paid plans, no ads, no boosts.

SITE: https://www.paramariboletter.com
INBOX: paramariboletter@gmail.com
CONFIG FILE: public/site-config.js
PLAYBOOK: public/marketing/free-services.md

In order:
1) Walk me through Microsoft Clarity project creation; I will paste the Project ID — you update site-config.js clarityProjectId only.
2) Walk me through Google Search Console property + submit https://www.paramariboletter.com/sitemap.xml
3) Walk me through UptimeRobot monitor on https://www.paramariboletter.com/ (alert to Gmail)
4) Optional: GA4 Measurement ID into site-config.js
5) Optional: Bing Webmaster import from Search Console
6) Create/open a Google Sheet from public/marketing/measurement-log.csv columns
7) After Resend domain is verified: remind me to run mail-tester once

Do not enable paid Vercel Speed Insights Plus. Do not buy ads. Do not post to X/LinkedIn unless I APPROVE_SEND.
When site-config.js changes, remind me to deploy (push to main) so Clarity loads in production.
```
