# Paramaribo Letter — brand channels

| Channel | Value | Status |
|---|---|---|
| Site | https://www.paramariboletter.com | Live |
| Fallback site | https://paramaribo-letter.vercel.app | Live |
| X | [@paramaribolette](https://x.com/paramaribolette) | Live · Issue 12 correction [posted](https://x.com/paramaribolette/status/2093911560607383999) |
| LinkedIn Newsletter | [The Paramaribo Letter](https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/) | Live · Issue 13 posted · ~68 subs |
| Inbox / replies | paramariboletter@gmail.com | Live |
| Subscribe | https://www.paramariboletter.com/#new-subscribers | Live |
| Unsubscribe | https://www.paramariboletter.com/unsubscribe | Live |
| Agents | https://www.paramariboletter.com/agents | Live |
| Resend send domain | `updates.paramariboletter.com` | **Verified** |
| Google Search Console | www.paramariboletter.com | Verified |
| UptimeRobot | www.paramariboletter.com | Up |
| Clarity | `ya3iur94oo` | Live |

## Email: two different jobs

1. **Inbox (done)** — `paramariboletter@gmail.com`  
   Reader replies, partner outreach, LinkedIn/X email field.

2. **Newsletter send (Resend)** — `/api/notify`  
   Verified domain: **`updates.paramariboletter.com`**.  
   Vercel has `RESEND_FROM_EMAIL` + `RESEND_API_KEY` + `NOTIFY_SECRET` + `SITE_URL`.  
   **Still add:** `RESEND_REPLY_TO=paramariboletter@gmail.com` so replies hit Gmail.  
   Do **not** use `@gmail.com` as the Resend From address.

## Checklist when “email is set up”

- [x] Gmail inbox: paramariboletter@gmail.com  
- [x] Resend domain verified (`updates.paramariboletter.com`)  
- [x] Vercel: `RESEND_API_KEY`, `RESEND_FROM_EMAIL`, `NOTIFY_SECRET`, `SITE_URL`  
- [ ] Vercel: `RESEND_REPLY_TO=paramariboletter@gmail.com`  
- [ ] Confirm GitHub Action secret `NOTIFY_SECRET` on paramaribo-letter  
- [x] Resend Contacts: **4** · unsubs **0** · deliverability OK on recent sends  
