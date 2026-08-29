# 14-day growth board — measurement first

Mode: dry-run planning. No public post, message, email, or paid promotion is authorized by this document.

Baseline: approximately **4 website visitors over one week**. This is a directional starting point, not enough evidence to claim a stable conversion rate or justify paid acquisition.

North star: grow the email list over a long horizon. Milestones remain 100 → 250 → 1,000 → 10,000 → 50,000 → 100,000 → 500,000. Never invent a current count.

## Measurement contract

- Website visitors, form views/starts, completed site subscribers, LinkedIn subscribers, and X followers remain separate counts.
- Use `subscribe_form_start` and `subscribe_complete` custom events.
- The primary decision metric is visit-to-subscribe CVR after a comparable observation window.
- Record source/referrer when available, but do not place email addresses or other personal data in analytics events.
- Freeze paid ads and heavy partnerships until the funnel has enough traffic for a useful comparison.

## Board

| Days | Experiment | Measurement | Success signal | Stop / handoff |
|---|---|---|---|---|
| 1–2 | Verify event wiring on home and issue pages | One start event on first form interaction; one complete event after a successful API response | Events visible without email data | Fix instrumentation before promotion |
| 3 | Establish the baseline | Visitors, form starts, completes, referrers | A dated baseline with caveats | Do not call 4 visitors conclusive |
| 4–5 | Publish one dry-run content pack for review | Draft approval status; no live send | Copy passes educational/compliance review | Human decides whether to publish |
| 6–7 | Observe organic traffic | Visitors, starts, completes by page | Enough observations to identify a bottleneck | Continue collecting if sample is thin |
| 8–9 | Test one homepage hook | Comparable visitors and CVR by period | Directional lift or clear loser | Keep the stronger hook; document uncertainty |
| 10–11 | Test one CTA variation | Form-start and completion rates | Fewer drop-offs without weaker quality | Revert unclear or harmful copy |
| 12 | Review archive and cross-links | Clicks/pageviews to issue, archive, subscribe | Readers can move from issue to signup | Fix broken or unclear paths |
| 13 | Consolidate the measurement log | One-page readout of counts and caveats | Decision-ready evidence packet | No referral or paid expansion yet |
| 14 | Choose the next bounded test | Baseline vs. current period | One next experiment with owner/date | Partnerships remain frozen until conversion is measurable |

## Weekly readout

- Traffic: ___ visitors; top source: ___
- Subscribe-form starts: ___
- New site subscribers: ___
- Visit-to-subscribe CVR: ___% (window: ___)
- LinkedIn Newsletter subscribers: ___ (separate)
- X impressions/profile visits: ___ (awareness only)
- Best-performing hook: ___
- Biggest uncertainty: ___
- Next test: ___
