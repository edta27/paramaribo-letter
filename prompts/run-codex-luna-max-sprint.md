# Codex sprint — Luna Max (Paramaribo Letter)

> **Historical, dated late August 2026 (Issue 12 sprint).** Issue numbers, URLs, the deploy path and "thank-you modal" references here are out of date. Use `prompts/letter-facts.md`, `run-letter-growth-desk.md`, and `run-paramaribo-letter.md` instead. Never copy `public/` wholesale onto the website branch.

Paste the block below into a **new Codex session**. Parent: **Sol High** if available. Workers: project agents on **`gpt-5.6-luna`** with **`model_reasoning_effort = "max"`** (Luna Max) for `lifecycle_conversion` and `growth_marketing_lead`; High is enough for editorial/social copy edits.

**Mode:** implement code + docs. **Do not** post to X/LinkedIn or send Resend mail unless the user wrote `APPROVE_SEND` and named the action.

**Baseline from Vercel (2026-08-29 screenshot):**

- Production **Ready** on `main` (`ccb1639` marketing HTML fix)
- Domain: `www.paramariboletter.com`
- Web Analytics: **on** · ~**4 visitors / 1w** · checklist 4/5 (Speed Insights Plus optional — skip unless asked)
- Funnel events: **not instrumented** · Resend list size: **unknown** · visit→subscribe CVR: **unknown**

**Canonical context:** `public/marketing/project-plan.md` · growth-desk amendment in this prompt · paste pack `public/marketing/linkedin-launch.md`

---

```text
Run the Paramaribo Letter Codex sprint under Luna Max.

SITE: https://www.paramariboletter.com
X: @paramaribolette
LINKEDIN: https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/ (56 subs, 3 editions — do not invent Resend count)
INBOX: paramariboletter@gmail.com
DEPLOY_REPO: edta27/paramaribo-letter (website remote → main)
RESEARCH_REPO: edta27/investment-research (this worktree may differ; ship site files to website/main for Vercel)
MODE: implement + dry-run social. No APPROVE_SEND unless I say so.
AS-OF: current time + timezone.
VERCEL_BASELINE: ~4 visitors / last week; Web Analytics enabled; production Ready.

You are the moderator. Use Luna Max (reasoning effort max) for lifecycle_conversion and growth_marketing_lead. Use High for editorial_content_lead and social_community_manager when you need paste polish only.

════════════════════════════════════════
PHASE 0 — packet (moderator, no spawn yet)
════════════════════════════════════════
1. Read public/marketing/project-plan.md, launch-status.md, brand-channels.md, linkedin-launch.md.
2. Read public/subscribe.js, public/api/subscribe.js, public/lib/resend.js, .env.example, vercel.json / public/vercel.json.
3. Confirm: educational / not advice; lenses ≠ authors; never invent subscriber counts; prefer https://www.paramariboletter.com clean URLs (/issue?id=, /agents, /#new-subscribers).
4. Growth-desk amendment (binding for this sprint):
   - Bottleneck = measurement, not more promo posts.
   - Day-1 order: instrument + env checklist docs → LinkedIn Issue 12 is HUMAN publish (prepare only).
   - Cap experiments; freeze paid ads + heavy partnerships until visit→subscribe CVR is a number.
   - Do not re-queue X “what is an agent?”; X is reply-first while unlock prompt may show.

════════════════════════════════════════
PHASE 1 — Lifecycle (Luna Max) — CODE
════════════════════════════════════════
Spawn lifecycle_conversion (Luna Max). Implement:

A) Funnel events in public/subscribe.js (and any shared binder):
   - On email field focus (once per page load): window.va?.('event', { name: 'subscribe_form_start' }) or the current Vercel Web Analytics custom-event API used on the site.
   - On successful subscribe (res.ok && data.ok): window.va?.('event', { name: 'subscribe_complete' })
   - On form section visible optional: subscribe_form_view via IntersectionObserver once — only if cheap and reliable; skip if fragile.
   - Guard: no-op if window.va missing; never block subscribe on analytics failure.
   - Do not send PII (no email) in event props.

B) Copy friction (small):
   - issue.html subscribe lede: change “Email me when…” → “Email when the next letter posts.” (drop “me”)
   - Prefer unsubscribe links as /unsubscribe (clean URL) in new/edited strings.

C) Docs for humans (do not claim env is set):
   - Update public/marketing/launch-status.md and brand-channels.md with a “Measure CVR” checklist:
     - Confirm Vercel env: SITE_URL, RESEND_API_KEY, RESEND_FROM_EMAIL, RESEND_REPLY_TO, NOTIFY_SECRET
     - Confirm GitHub Action secret NOTIFY_SECRET on paramaribo-letter
     - Export Resend Contacts count (paste into launch-status when known — leave blank/unknown until human pastes)
     - Events to watch in Vercel Analytics: subscribe_form_start, subscribe_complete
   - Draft welcome sequence (3 emails) into public/marketing/welcome-sequence.md — DRY RUN TEXT ONLY, marked do-not-send until From domain verified. Include unsubscribe + educational disclaimer.

D) Acceptance:
   - grep/read shows va events wired
   - python3 -m http.server smoke not required if static; note how to verify in Vercel Analytics after deploy
   - Regenerate public/marketing/*.html from md if your tree uses the HTML mirrors (keep index listing welcome-sequence + project-plan)

════════════════════════════════════════
PHASE 2 — Growth (Luna Max) — DOCS ONLY
════════════════════════════════════════
Spawn growth_marketing_lead (Luna Max). No code required unless Phase 1 left gaps.

1. Rewrite the “First 14-day growth plan” section in public/marketing/project-plan.md to the amended board:
   - Days 1–2: env confirm (human) + LinkedIn Issue 12 publish (human) + start/complete events live
   - Days 2–7: X reply-first; optional Issue 10 pull-quote; optional process poll; NO subscribe nag
   - Days 8–14: one homepage hook OR one CTA test only after events exist; welcome mail only after domain verified; partnerships stay frozen
2. Add Vercel baseline note: ~4 visitors/1w as of 2026-08-29 — not a KPI claim, just starting denominator.
3. Update launch-status “Next” checkboxes to match (instrumentation done vs human remaining).
4. Keep LinkedIn 56 and Resend unknown separate.

════════════════════════════════════════
PHASE 3 — Editorial + Social (High) — PASTE ONLY
════════════════════════════════════════
Spawn editorial_content_lead and social_community_manager only if paste packs need refresh.

1. Ensure linkedin-launch.md Issue 12 paste uses clean URLs and lens language (“desk read of…”, not “Bang writes”).
2. Add Issue 10 pull-quote draft to linkedin-launch.md or x-account-launch.md (dry-run).
3. Add 7-day reply-first calendar table to x-account-launch.md (from social memo).
4. Explicit line: DO NOT POST without APPROVE_SEND.

════════════════════════════════════════
PHASE 4 — ship site files
════════════════════════════════════════
1. Commit on the current branch with a clear message (instrument subscribe funnel + amend growth plan).
2. Deploy path used by this project: checkout website-deploy (tracks website/main), bring over public/ + vercel.json changes, commit, git push website HEAD:main.
3. Also push the research branch to origin if that is the workflow for this worktree.
4. After deploy: curl -sI https://www.paramariboletter.com/marketing/project-plan | head; confirm subscribe.js on production contains subscribe_complete (curl the JS).
5. Do NOT enable Speed Insights Plus unless the user asks (checklist 5/5 is optional paid).

════════════════════════════════════════
PHASE 5 — human handoff (moderator output)
════════════════════════════════════════
End with a short checklist the human must do (Codex cannot):
[ ] Vercel env values confirmed
[ ] Resend domain verified + contact count pasted into launch-status
[ ] LinkedIn frequency → Occasionally or Weekly
[ ] APPROVE_SEND LinkedIn Issue 12 (paste in linkedin-launch)
[ ] Watch Vercel Analytics for subscribe_form_start / subscribe_complete after self-test subscribe
[ ] X: replies only until unlock prompt eases

Report: files changed, deploy SHA/URL, what remains human-only. Never invent Resend or X follower counts.
```

## Success criteria (Definition of Done)

| Done when | Owner |
|---|---|
| `subscribe_form_start` + `subscribe_complete` fire via `window.va` | Codex |
| Welcome sequence markdown exists, marked do-not-send | Codex |
| Project plan 14-day board matches growth-desk amendment | Codex |
| Live on `www.paramariboletter.com` after `website`/`main` push | Codex |
| Resend count + env confirmed | **Human** |
| LinkedIn Issue 12 published | **Human** + `APPROVE_SEND` |
| Visit→subscribe CVR computable (visitors + completes in same window) | Human + Analytics |

## Out of scope this sprint

- Paid ads, partnerships outreach, referral product
- New research letter / council run
- Buying X engagement / pods
- Speed Insights Plus upgrade
- Impersonating named traders
- Claiming 500k or inventing list sizes
