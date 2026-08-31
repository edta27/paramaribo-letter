# Engagement matrix

Updated: 2026-08-31 ~3:47 a.m. CT (Clarity CSV + X snapshot). Vercel / LinkedIn still 2026-08-30. Do not mash channels. Never invent missing cells.

## Cross-platform snapshot

| Channel | Reach / activity | Engagement | Growth |
|---|---|---|---|
| **X** (@paramaribolette) | [Issue 14](https://x.com/paramaribolette/status/2094338477378654619) · 17 posts · prior day 8 replies + [Recovery Check](https://x.com/paramaribolette/status/2094149496921870372) | profile visits / link clicks unavailable (needs Premium) | **6** followers · 12 following |
| **LinkedIn** (Issue 13 post) | **120** impressions · **51** members reached | **0** social engagements | **0** followers gained |
| **LinkedIn Newsletter email** | **63** sends | **8%** open rate | (subs counted separately ~68) |
| **Site (Vercel Analytics)** | **28** visitors · **110** page views | bounce **68%** | see pages/referrers below |
| **Site (Clarity, 29–31 Aug)** | **43** sessions (**28** bot) · **34** unique users | 1.33 pages/session · 1.5 min active | 40/43 new-user sessions |
| **Resend** | — | — | **4** contacts |

## Site analytics (Vercel · screenshot 2026-08-30 ~1:06 AM)

| Measure | Result |
|---|---:|
| Visitors | 28 |
| Page views | 110 |
| Bounce rate | 68% (+68% vs prior window in UI) |

**Top pages (visitors):** `/` 17 · `/issue` 15 · `/agents` 2 · `/marketing/brand-channels` 2 · `/unsubscribe` 2  

**Referrers (visitors):** `t.co` 2 · `vercel.com` 2 · Google Android 1 · `linkedin.com` 1  

**Reading:** Traffic ramped Aug 27–29 (Issue 12/13 + social). Home and issue pages dominate. X (`t.co`) and LinkedIn both show as referrers, but counts are still tiny — discovery is starting, not a funnel yet. Subscribe custom events remain unavailable on the current Analytics plan.

## Clarity (29–31 Aug · export 2026-08-31 ~3:47 AM)

Source: Clarity dashboard CSV, project `paramariboletter`, range 29 Aug 12:00 AM – 31 Aug 11:59 PM.

| Measure | Result |
|---|---:|
| Total sessions | **43** |
| Bot sessions | **28** (suspicious-interaction 28; suspicious-device 25 — categories overlap) |
| Non-bot remainder | **~15** if bots ⊆ total |
| Unique users | **34** (export; may include bots — do not treat as 34 humans) |
| Pages per session | 1.33 |
| Scroll depth (avg) | 41.67% |
| Active time | 92s / **1.5 min** (of 145s / 2.4 min total) |
| New-user sessions | 40 / 43 (93%) |
| Returning-user sessions | 3 / 43 (7%) |
| Rage clicks | 0 |
| Dead clicks | 2 (4.65%) |
| Excessive scrolling / quick backs | 0 |
| JS errors | 0 |
| Smart events | none recorded |

**Unique users by day:** 29 Aug **13** · 30 Aug **22** · 31 Aug **1** (pre-open; Issue 14 X went up ~3:25 AM — too early for click-through).

**Top pages (sessions):** `/` 29 · `/issue` 14 · `/marketing/today-closeout-manual` 3 · vercel.app alias 1 · `/marketing/brand-channels` 1 · `/unsubscribe` 1.

**Referrers (sessions):** internal 7 · LinkedIn Android **2** · `t.co` **2** · Gmail Android **1** · vercel.com 1 · google.com 1.

**Channels:** Other 31 · Direct 7 · Referral 5 · Organic Search 2.

**Reading:** Headline uniques (**34**) and sessions (**43**) are up vs the 30 Aug screenshot (14 users / 17 sess), but **28/43 sessions are bots**. Do not report 34 readers. Peak day in this window is **30 Aug (22 uniques)** — Issue 13 weekend — not 31 Aug. Home and issue still dominate. `/marketing/today-closeout-manual` (3) is publisher traffic, not audience. Social referrers remain tiny (`t.co` 2, LinkedIn app 2). One Gmail Android session is consistent with a Resend click, not proof of list growth. No Clarity smart events → subscribe funnel still unmeasured here. Dead clicks 2, still low. France/Netherlands one-session PCs sit next to 25 suspicious-device bots — do not call that EU demand.

Prior Clarity (screenshot 2026-08-30 ~1:08 AM): 17 sessions (15 bot excluded) · 14 unique · 1.59 pages · 34.70% scroll · 1.3 min active. Keep that row as the previous snapshot; do not splice the two series.

## Observability (Production · last 6h · screenshot ~1:07 AM)

Healthy: function errors **0%**, timeouts **0%**, edge traffic normal. No site-down signal. Skip Observability Plus paid upgrade.

## LinkedIn post detail (Issue 13)

| LinkedIn measure | Result |
|---|---:|
| Impressions | 120 |
| In-network impressions | 46% |
| Out-of-network impressions | 54% |
| Members reached | 51 |
| Article views | 7 |
| Email sends | 63 |
| Email open rate | 8% |
| Profile viewers from post | 0 |
| Followers gained | 0 |
| Social engagements | 0 |
| Reactions | 0 |
| Comments | 0 |
| Reposts | 0 |
| Saves | 0 |
| Sends | 0 |

### Reading

LinkedIn is getting some **discovery beyond the existing network** (54% out-of-network), but that reach has **not** yet converted into profile visits, followers, or visible engagement (reactions/comments/reposts).

Email layer (63 sends / 8% open) is a separate surface from on-platform social engagements — do not treat opens as “likes.”

## Next LinkedIn creative note (Content Writer)

Close the next edition/post with a discussion question, e.g.:

> What signal would you require before treating this range as a real floor?

Keep educational / conditional tone; link the full letter; no advice framing.

## Sources

- LinkedIn analytics (user paste 2026-08-30)
- Mary X community log 2026-08-30
- Prior Resend / Vercel snapshots in `launch-status.md`
