# Engagement matrix

Updated: 2026-08-30. Do not mash channels. Never invent missing cells.

## Cross-platform snapshot

| Channel | Reach / activity | Engagement | Growth |
|---|---|---|---|
| **X** (@paramaribolette) | 8 relevant replies · [BTC Recovery Check](https://x.com/paramaribolette/status/2094149496921870372) | early chart post (views may lag) | **4** followers · 6 following |
| **LinkedIn** (Issue 13 post) | **120** impressions · **51** members reached | **0** social engagements | **0** followers gained |
| **LinkedIn Newsletter email** | **63** sends | **8%** open rate | (subs counted separately ~68) |
| **Site (Vercel Analytics)** | **28** visitors · **110** page views | bounce **68%** | see pages/referrers below |
| **Site (Clarity, 3d)** | **17** sessions · **14** unique users | 1.59 pages/session · 1.3 min active | 94% new-user sessions |
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

## Clarity (last 3 days · screenshot 2026-08-30 ~1:08 AM)

| Measure | Result |
|---|---:|
| Sessions | 17 (15 bot sessions excluded) |
| Unique users | 14 |
| Pages per session | 1.59 |
| Scroll depth (avg) | 34.70% |
| Active time | 1.3 min (of 3.0 min total) |
| New-user sessions | 94.12% |
| Returning-user sessions | 5.88% |
| Rage clicks | 0% |
| Dead clicks | 5.88% (1 session) |
| Excessive scrolling / quick backs | 0% |

**Reading:** Mostly first-time visitors, short sessions, shallow scroll — consistent with high bounce. No rage-click problem. Dead clicks are low but worth a later UX pass on subscribe/nav if they persist.

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
