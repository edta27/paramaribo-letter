# Paramaribo Letter — Solo Marketing Agent

Quick one-agent path. For the **five-role growth desk** (Growth / Editorial / Social ± Partnerships / Lifecycle), use `run-letter-growth-desk.md` instead.

```text
Run letter_marketing for The Paramaribo Letter.

SITE: https://www.paramariboletter.com
X: @paramaribolette
ISSUE: [Default: latest in public/catalog.json. Or paste an issue id like 2026-09-26-87k-rejection.]
GOAL: [e.g. grow email list / announce the latest issue / LinkedIn edition that sends readers to the site / pin an X thread]
CHANNELS: [Default: LinkedIn + X + email CTA. Add SEO or directories if needed.]
MODE: [Default: dry-run drafts only. Write APPROVE_SEND only if a human may publish/send.]
AS-OF: Use the current time and timezone.

Use the project-scoped agent: letter_marketing

You are the moderator. Have letter_marketing:
0. Read prompts/letter-facts.md for current URLs, targets and channels.
1. Read the issue title, dek, date, and one honest hook from the body (no invented prices).
2. Deliver positioning, ready-to-paste LinkedIn + X (+ thread) + email/CTA copy, funnel check, metrics, and compliance pass.
3. Every public draft must say educational research, not advice, and must not impersonate named traders or firms.
4. Do not post or email unless MODE is APPROVE_SEND.
5. Prefer https://www.paramariboletter.com links: issues as /issue?id={id}, evergreen questions to a /topics hub. LinkedIn copy links the full issue in the first two lines.
```

## When to use which

| Need | Prompt |
|---|---|
| Full growth desk (recommended) | `run-letter-growth-desk.md` |
| Solo quick announce | this file |
| Write the letter itself | `run-paramaribo-letter.md` |
