# Paramaribo Letter — Marketing Agent

Paste into a new Codex/Conductor chat when you want growth copy and a channel plan for the site — not a market forecast.

```text
Run letter_marketing for The Paramaribo Letter.

SITE: https://paramaribo-letter.vercel.app
ISSUE: [Default: latest featured in public/catalog.json. Or paste an issue id like 2026-08-28-zz-bang-clear-map.]
GOAL: [e.g. grow email list / announce Issue 12 / LinkedIn newsletter setup / pin an X thread]
CHANNELS: [Default: LinkedIn + X + email CTA. Add SEO or directories if needed.]
MODE: [Default: dry-run drafts only. Write APPROVE_SEND only if a human may publish/send.]
AS-OF: Use the current time and timezone.

Use the project-scoped agent: letter_marketing

You are the moderator. Have letter_marketing:
1. Read the issue title, dek, date, and one honest hook from the body (no invented prices).
2. Deliver positioning, 7-day channel plan, ready-to-paste LinkedIn + X (+ thread) + email/CTA copy, funnel check, metrics, and compliance pass.
3. Every public draft must say educational research, not advice, and must not impersonate named traders or firms.
4. Do not post or email unless MODE is APPROVE_SEND.

Optional follow-ups the agent may suggest (human does them):
- Turn on Vercel Web Analytics and check subscribe conversion after a post.
- Confirm Resend NOTIFY_SECRET so catalog pushes email subscribers.
- Link Agents page and Unsubscribe in every bio/footer mention.
```

## When to use which agent

| Need | Agent / prompt |
|---|---|
| Write or edit the letter itself | `research_director` · `run-paramaribo-letter.md` |
| Full market council | `run-crypto-council.md` |
| Promote the site / an issue | `letter_marketing` · this file |
| Equity overnight board | `run-equity-desk.md` |

## Brand guardrails (short)

- Promote the *desk process* (agents argue, cash is valid, archive kept) — not guaranteed returns.
- Always link subscribe + the specific issue.
- Hashtag search fame ≠ endorsement; do not claim Bang, Cowen, or others write for you.
