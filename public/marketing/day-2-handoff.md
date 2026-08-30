# Overnight handoff — Day 2

**As-of:** 2026-08-29 ~01:36 CT · Day 1 closed · human asleep  
**Split:** Conductor = marketing oversee (no X / LinkedIn / Gmail). Codex + human = those channels.  
**Posts need** `APPROVE_SEND` named per item.

## Roles

| Who | Does |
|---|---|
| **Conductor marketing team** | Oversees plan, measurement, paste packs, deploy verify, Day N briefs |
| **Codex** | X, LinkedIn (Shan Ho / Newsletter), Gmail inbox drafts — only with approval |
| **Human** | Approves sends, confirms env/Resend count, sleeps / wakes the sprint |

## Day 1 closed

- [x] Site live; subscribe / unsubscribe / agents / archive / marketing notes
- [x] X profile, pin, Issue 12, “What is an agent?”
- [x] LinkedIn Newsletter live (56 · 3 editions) — Issue 12 edition **not** published
- [x] Local funnel events: `subscribe_form_start`, `subscribe_complete` (no email in payloads)
- [ ] Production deploy of those events — **verify on Day 2 open**
- [x] Paid ads + partnerships frozen; ~4 visitors / 1w baseline noted

## Day 2 objective

Confirm subscribe events on production, publish LinkedIn Issue 12 with an honest frequency label, keep X reply-first, and log the first real numbers (small n is fine).

## Day 2 — Codex + human (channels)

Volume cap: **one** distribution action (LinkedIn Issue 12). X = replies only.

1. Gmail — read; draft only until `APPROVE_SEND` per thread  
2. LinkedIn frequency → Weekly or Occasionally — `APPROVE_SEND`  
3. LinkedIn Issue 12 from `linkedin-launch.md` — `APPROVE_SEND`  
4. LinkedIn comment replies (short, educational) — `APPROVE_SEND`  
5. X — replies only; no fourth promo — `APPROVE_SEND` per reply  
6. Skip: Issue 10 quote, polls, partner DMs, welcome mail, subscribe nag  

### Paste into Codex (morning)

```text
Run Paramaribo Letter Day 2 channel work. DRY-RUN until I type APPROVE_SEND and name the item.

SITE: https://www.paramariboletter.com
X: @paramaribolette
LINKEDIN: https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/
  (56 subs, 3 editions as of 2026-08-29 — do not invent Resend or X follower counts)
INBOX: paramariboletter@gmail.com
ISSUE 12: https://www.paramariboletter.com/issue?id=2026-08-28-zz-bang-clear-map
SUBSCRIBE: https://www.paramariboletter.com/#new-subscribers
AGENTS: https://www.paramariboletter.com/agents
PASTE PACK: public/marketing/linkedin-launch.md
AS-OF: [paste time + timezone]
MODE: dry-run. APPROVE_SEND only for items I name.

Facts you must not fight:
- Day 1 X work is done (pin + Issue 12 + agents post). Unlock-more prompt → reply-first. Do not re-queue those posts.
- Instrumentation may be local-only until Conductor confirms production. Do not claim events are live.
- Paid ads + partnerships frozen. Educational / not advice. Lenses ≠ authors. Prefer clean paramariboletter.com URLs.

Do, in order, as drafts only:
1) Gmail: summarize unread that looks like a reader. Draft replies. Do not send.
2) LinkedIn Newsletter: draft click-path to change frequency from “Published daily” → Weekly or Occasionally. Wait for APPROVE_SEND frequency.
3) LinkedIn Issue 12: use linkedin-launch.md paste. Wait for APPROVE_SEND Issue 12.
4) LinkedIn reply block: 3 short comment-reply drafts. APPROVE_SEND per reply or named batch.
5) X: draft replies only. Zero new promo posts. APPROVE_SEND per reply.
6) End with one-screen recap: waiting on APPROVE_SEND, untouched items, counts still unknown.

If I later say e.g. APPROVE_SEND LinkedIn Issue 12 — execute only that item, then stop and wait.
```

## Day 2 — Conductor oversee (no posting)

1. Verify production `subscribe.js` contains both event names; deploy from Codex letter repo if still missing  
2. Self-test brief for human (focus → start; subscribe → complete; no PII in events)  
3. Measurement log line: visitors / starts / completes / LinkedIn / Resend (unknown OK)  
4. Keep paste packs clean-URL; partnerships freeze holds  
5. Env reminder: `SITE_URL`, Resend From domain, Reply-To, `NOTIFY_SECRET`  

## Success criteria

- Events on prod **or** written “not on prod” + next deploy step  
- Self-test attempted; “0 completes” is a valid log  
- LinkedIn frequency not “daily”; Issue 12 edition public if approved  
- X: zero new promo posts  
- No ads, welcome blast, or invented counts  

## Free tools — use all free tiers

Full list + signup order: **`free-services.md`**.

**Day 2 priority signups (human / Codex):**
1. Microsoft Clarity → paste Project ID into `public/site-config.js`  
2. Google Search Console → submit `/sitemap.xml`  
3. UptimeRobot → watch `/`  
4. Google Sheets → import `measurement-log.csv`  
5. (Optional) GA4, Bing Webmaster, Canva, mail-tester after Resend domain  

Site already ships: Vercel Analytics · `/feed.xml` · `/sitemap.xml` · Clarity/GA4 loader (off until IDs filled).

## What not to do

Paid boosts · partnerships · invent CVR · mash LinkedIn into email north star · second agents explainer · welcome sequence send · impersonate named traders  

## When you wake up

Say **“Day 2”** here — Conductor runs oversee (deploy verify + log). Paste the Codex block above for X / LinkedIn / Gmail.  
If events still are not live, say **`push to main and deploy`** in the Codex letter tree (or here) first.
