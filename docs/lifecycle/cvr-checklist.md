# Visit-to-subscribe CVR checklist

Purpose: establish a trustworthy baseline before paid promotion or heavy partnerships.

## Funnel definitions

| Event | Meaning | Source |
|---|---|---|
| `pageview` | A page was viewed | Vercel Web Analytics |
| `subscribe_form_start` | A visitor focused or entered the subscribe form | Vercel custom event |
| `subscribe_complete` | The API returned a successful subscribe response | Vercel custom event |

Primary rate:

`completed subscribers ÷ unique website visitors × 100`

Supporting rates:

- Form-start rate = form starts ÷ unique visitors × 100
- Form completion rate = successful completes ÷ form starts × 100
- New-subscriber rate = `outcome=new_subscriber` completes ÷ unique visitors × 100

Do not use raw pageviews as a substitute for unique visitors, and do not combine Resend results with LinkedIn Newsletter subscribers.

## Weekly review

- [ ] Record the date range and timezone.
- [ ] Record unique visitors and top referrers.
- [ ] Record subscribe-form starts.
- [ ] Record `subscribe_complete` events by outcome.
- [ ] Check that event counts are plausible against the site’s traffic.
- [ ] Note missing configuration or ad-blocker uncertainty.
- [ ] Compare the result with the prior period only when the measurement window is comparable.
- [ ] Record one change for the next test; do not change several variables at once.

## First baseline

The current planning baseline is approximately **4 visitors over one week**. Treat it as directional and too small for a reliable conversion conclusion. Keep the funnel instrumented, collect a larger comparable window, and do not buy ads or scale partnerships from this sample alone.

## Test log

| Window | Visitors | Form starts | New completes | CVR | Change | Decision |
|---|---:|---:|---:|---:|---|---|
| YYYY-MM-DD → YYYY-MM-DD |  |  |  |  |  |  |
