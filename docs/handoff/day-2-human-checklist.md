# Day 2 human handoff

Status: preparation complete. Public actions remain blocked until a human gives the exact `APPROVE_SEND` approval.

## LinkedIn

- [ ] Open the public newsletter: https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/
- [ ] Change frequency from **Published daily** to **Occasionally** or **Weekly** so the label matches the event-driven cadence.
- [ ] Create and review the Issue 12 edition using `docs/editorial-social-dry-run.md` or `public/marketing/linkedin-launch.md`.
- [ ] Confirm the title, issue URL, disclaimer, and site subscribe link.
- [ ] Say `APPROVE_SEND` immediately before publishing the Issue 12 edition.

## X

- [ ] Do not edit or delete the existing Issue 12 post without a separate decision.
- [ ] Review the correction draft in `public/marketing/x-account-launch.md`.
- [ ] Publish a short corrective reply or follow-up with the complete Issue 12 URL only after `APPROVE_SEND`.
- [ ] Reply first to genuine questions; no pods, mass replies, or engagement bait.

## Funnel and account checks

- [x] Subscribe and unsubscribe forms explicitly carry `data-clarity-mask="true"`; confirm the setting in Microsoft Clarity project `ya3iur94oo` when dashboard access is available.
- [ ] In Vercel Analytics, record visitors, `subscribe_form_start`, and `subscribe_complete` separately.
- [ ] Do not calculate a stable CVR from the current ~4-visitors/week baseline.
- [ ] Confirm Resend sender-domain authentication and `RESEND_REPLY_TO` in Vercel.
- [ ] Keep LinkedIn subscribers, Resend subscribers, X followers, and site visitors as separate counts.
