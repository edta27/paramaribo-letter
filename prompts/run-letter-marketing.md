# Paramaribo Letter — Solo Marketing Agent

Quick one-agent path. For the **five-role growth desk** (Growth / Editorial / Social ± Partnerships / Lifecycle), use `run-letter-growth-desk.md` instead.

```text
Run letter_marketing for The Paramaribo Letter.

SITE: https://www.paramariboletter.com
X: @paramaribolette
ISSUE: [Default: latest featured in public/catalog.json. Or paste an issue id like 2026-08-28-zz-bang-clear-map.]
GOAL: [e.g. grow email list / announce Issue 12 / LinkedIn newsletter setup / pin an X thread]
CHANNELS: [Default: LinkedIn + X + email CTA. Add SEO or directories if needed.]
MODE: [Default: dry-run drafts only. Write APPROVE_SEND only if a human may publish/send.]
AS-OF: Use the current time and timezone.

Use the project-scoped agent: letter_marketing

You are the moderator. Have letter_marketing:
1. Read the issue title, dek, date, and one honest hook from the body (no invented prices).
2. Deliver positioning, ready-to-paste LinkedIn + X (+ thread) + email/CTA copy, funnel check, metrics, and compliance pass.
3. Every public draft must say educational research, not advice, and must not impersonate named traders or firms.
4. Do not post or email unless MODE is APPROVE_SEND.
5. Prefer https://www.paramariboletter.com links.
```

## When to use which

| Need | Prompt |
|---|---|
| Full growth desk (recommended) | `run-letter-growth-desk.md` |
| Solo quick announce | this file |
| Write the letter itself | `run-paramaribo-letter.md` |
