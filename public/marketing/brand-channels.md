# Paramaribo Letter — brand channels

| Channel | Value | Status |
|---|---|---|
| Site | https://www.paramariboletter.com | Live |
| Fallback site | https://paramaribo-letter.vercel.app | Live |
| X | [@paramaribolette](https://x.com/paramaribolette) | Live (pin + Issue 12 + agents post); Issue 12 link correction pending |
| LinkedIn Newsletter | [The Paramaribo Letter](https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/) (by Shan Ho) | **Live** — 67 subs, 3 editions; Issue 12 pending |
| Inbox / replies | paramariboletter@gmail.com | Live |
| Subscribe | https://www.paramariboletter.com/#new-subscribers | Live |
| Unsubscribe | https://www.paramariboletter.com/unsubscribe.html | Live |
| Agents | https://www.paramariboletter.com/agents.html | Live |

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
