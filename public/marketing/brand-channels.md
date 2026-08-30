# Paramaribo Letter — brand channels

| Channel | Value | Status |
|---|---|---|
| Site | https://www.paramariboletter.com | Live |
| Fallback site | https://paramaribo-letter.vercel.app | Live |
| X | [@paramaribolette](https://x.com/paramaribolette) | Live (pin + Issue 12 + agents post); Issue 13 announce pending; Issue 12 link correction posted |
| LinkedIn Newsletter | [The Paramaribo Letter](https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/) (by Shan Ho) | **Live** — approximately 68 subs; edition count confirm in UI; Issue 13 posted, frequency pending |
| Inbox / replies | paramariboletter@gmail.com | Live |
| Subscribe | https://www.paramariboletter.com/#new-subscribers | Live |
| Unsubscribe | https://www.paramariboletter.com/unsubscribe.html | Live |
| Agents | https://www.paramariboletter.com/agents.html | Live |

## Next

- [x] LinkedIn Issue 13 posted (human-confirmed; do not re-post)
- [ ] LinkedIn frequency → **Occasionally** (`APPROVE_SEND` required)
- [ ] X Issue 13 announce (`APPROVE_SEND` required)
- [x] X Issue 12 correction reply posted to the existing post; do not duplicate

## Email: two different jobs

1. **Inbox (done)** — `paramariboletter@gmail.com`  
   Use for: reader replies, partner outreach “From”, LinkedIn/X “Email”, press.  
   Put in bios: `paramariboletter@gmail.com` or “DM / email paramariboletter@gmail.com”.

2. **Newsletter send (Resend)** — transactional “new issue” mail via `/api/notify`  
   Vercel env `RESEND_FROM_EMAIL` should be a **verified Resend domain**, ideally:  
   `The Paramaribo Letter <letter@paramariboletter.com>`  
   Optional: set Resend **Reply-To** to `paramariboletter@gmail.com` so readers hit the Gmail inbox.  
   Do **not** use `@gmail.com` as the Resend From address (deliverability / Resend rules).

## Checklist when “email is set up”

- [x] Gmail inbox exists: paramariboletter@gmail.com  
- [ ] Site/X/LinkedIn point readers to that inbox if you want replies  
- [ ] Resend domain verified for paramariboletter.com (or send domain you own)  
- [ ] Vercel: `RESEND_API_KEY`, `RESEND_FROM_EMAIL`, `NOTIFY_SECRET`, `SITE_URL=https://www.paramariboletter.com`  
- [ ] GitHub Action secret `NOTIFY_SECRET` on the letter deploy repo  
- [ ] Test: subscribe with your own address → thank-you modal → get a notify after next catalog push (or run `scripts/notify_subscribers.py`)

## Resend/Vercel confirmation — 2026-08-29 23:02 CDT

- Resend Audience: **4 subscribers**, **0 unsubscribers**.
- Resend Metrics, last 15 days: **16 emails**, **100% deliverability**, **0 bounces**, **0 complaints**.
- Resend: `updates.paramariboletter.com` is verified. The root `paramariboletter.com` was not shown as verified.
- Vercel Production variable names observed: `SITE_URL`, `RESEND_API_KEY`, `RESEND_FROM_EMAIL`, `NOTIFY_SECRET`.
- `RESEND_REPLY_TO` was not present. Values were masked/hidden and were not changed.
- GitHub Action `NOTIFY_SECRET` was not checked in this pass.
