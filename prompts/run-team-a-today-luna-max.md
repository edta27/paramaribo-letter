# Team A — Today closeout (Luna Max / Codex)

> **Historical, dated 2026-08-30 (Issue 13).** Issue numbers, URLs, the deploy path and "thank-you modal" references here are out of date. Use `prompts/letter-facts.md`, `run-letter-growth-desk.md`, and `run-paramaribo-letter.md` instead. Never copy `public/` wholesale onto the website branch.

**As-of context for this paste:** Issue 13 is live on the site **and** posted on LinkedIn. Team B is done for the issue. Team A finishes today’s distribution + measurement hygiene.

Paste the fenced block into a **new Codex** session.  
Parent: **Sol High** if available. Workers: **`gpt-5.6-luna`** with **`max`** for `growth_marketing_lead` + `lifecycle_conversion`; **High** for `editorial_content_lead` + `social_community_manager`.

---

```text
Run Team A — Growth & Promotion — TODAY CLOSEOUT under Luna Max.

SITE: https://www.paramariboletter.com
X: @paramaribolette
LINKEDIN: https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/
INBOX: paramariboletter@gmail.com
ISSUE 13: https://www.paramariboletter.com/issue?id=2026-08-30-stall-not-a-floor
  Title: The $77–80k stall is not a floor
  Id: 2026-08-30-stall-not-a-floor
ALREADY DONE TODAY:
  - Team B published Issue 13 on the site (live).
  - Issue 13 was posted on LinkedIn (human confirmed).
STILL OPEN (do not re-do LinkedIn Issue 13 edition):
  - LinkedIn frequency may still say “Published daily” → change to Occasionally (needs APPROVE_SEND).
  - X: promote Issue 13 + optional Issue 12 URL correction if the old post still lacks ?id=.
  - Measurement log + Resend/Vercel env checklist.
  - Docs sync: launch-status, linkedin-launch, x-account-launch, brand-channels.
MODE: dry-run for all public actions until I type APPROVE_SEND and name the item.
AS-OF: [paste local time + timezone]
COUNTS: LinkedIn ~68 (paste latest if different). Resend = unknown unless I paste. Never invent.

You are the Team A moderator.
Spawn Luna Max: growth_marketing_lead, lifecycle_conversion
Spawn High: editorial_content_lead, social_community_manager
Do NOT spawn partnerships_referral_manager (still frozen). Do NOT run Team B / research council.

════════════════════════════════════════
PHASE 0 — packet
════════════════════════════════════════
1. Load Issue 13 json/body (or live URL facts): title, dek, id, cover path, key levels only from the letter.
2. Read public/marketing/launch-status.md, linkedin-launch.md, x-account-launch.md, free-services.md, brand-channels.md.
3. Remind: educational / not advice; lenses ≠ authors; clean paramariboletter.com URLs; cash valid; do not mash LinkedIn with Resend.

════════════════════════════════════════
PHASE 1 — Docs (implement, no approval needed)
════════════════════════════════════════
1. Mark in launch-status + linkedin-launch: Issue 13 LinkedIn post DONE (do not invent edition count — ask or leave “confirm in UI”).
2. Add Issue 13 paste block to linkedin-launch.md (archive for next time) if missing — title/body/site links/disclaimer.
3. Write X Issue 13 announce draft + optional Issue 12 correction draft into x-account-launch.md (clearly labeled DO NOT POST without APPROVE_SEND).
4. Update brand-channels / launch-status “Next” so LinkedIn Issue 13 is checked; leave frequency + X as open until approved.
5. Append one row guidance to measurement-log.csv or docs for today’s date (visitors / starts / completes / LinkedIn / Resend unknown).
6. Commit docs on the letter repo branch you are on. Push only if the workflow for this tree is push-to-main; otherwise prepare the commit and ask.

════════════════════════════════════════
PHASE 2 — Paste packs (dry-run)
════════════════════════════════════════
editorial_content_lead + social_community_manager produce:

A) X — Issue 13 announce (≤260 chars or short post + optional 4-beat thread). Must include:
   https://www.paramariboletter.com/issue?id=2026-08-30-stall-not-a-floor
   Educational / not advice. No “bottom is in.” Prefer “stall is not a floor” / cash until Daily close.

B) X — Issue 12 correction reply ONLY if still needed (complete URL with id). One short reply, not a new promo pile-on.

C) LinkedIn — frequency click-path: Edit newsletter → Occasionally. No second Issue 13 edition.

D) 3 reply templates for Issue 13 comments (advice? / who writes? / where subscribe?).

E) End with a one-screen APPROVE_SEND menu:
   [ ] APPROVE_SEND LinkedIn frequency Occasionally
   [ ] APPROVE_SEND X Issue 13 announce
   [ ] APPROVE_SEND X Issue 12 correction
   Nothing else.

════════════════════════════════════════
PHASE 3 — Lifecycle / Growth (Luna Max) — checklist only
════════════════════════════════════════
1. Confirm production still has subscribe_form_start / subscribe_complete (curl subscribe.js).
2. Confirm Clarity ya3iur94oo /clarity.js still referenced on home + issue.
3. Human checklist (do not claim env is set): SITE_URL, RESEND_FROM domain, RESEND_REPLY_TO, NOTIFY_SECRET, Resend Contacts count paste, Vercel Analytics custom events visible.
4. Explicitly: no welcome-sequence send tonight. No paid ads. No partnerships outreach.
5. If UptimeRobot email alerts still optional — one sentence how to enable to paramariboletter@gmail.com.

════════════════════════════════════════
PHASE 4 — Stop and hand back
════════════════════════════════════════
Output:
1. What you committed/pushed (files + SHA if any)
2. Paste-ready X Issue 13 post (and correction if any)
3. APPROVE_SEND menu (only the three items above)
4. What is DONE for today vs what waits on me
5. Counts still unknown

If I later say e.g. APPROVE_SEND X Issue 13 announce — execute ONLY that item on X, then stop.
Do not delete or edit prior X posts except posting a reply/correction.
Do not publish another LinkedIn edition for Issue 13.
```

## Success for “today done”

- Docs reflect Issue 13 LinkedIn done  
- X Issue 13 draft ready  
- Frequency + X items waiting on a single clear `APPROVE_SEND` line  
- No research rewrite, no welcome mail, no partnerships  
