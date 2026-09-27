# Paramaribo Letter — Team A · Growth Desk (marketing)

**Team A — Growth & Promotion.** Five publisher roles aimed at a long-horizon **500,000-subscriber** goal. Not market research. Not advice. Team B owns the letter itself — see `prompts/run-two-teams.md`.

**After Team B publishes:** prefer the full existing-agent loop in `prompts/run-team-a-growth-loop.md` (no new agent; no ASTER). Primary KPI: legitimate new newsletter subscribers per 1,000 impressions. Log `public/marketing/content-performance.csv`. Never invent counts.

**Default run = core three.** Add Partnerships and Lifecycle only when the signup funnel is converting (or the user asks). The growth loop also includes Mary and letter_marketing; partnerships stay organic-only until CVR is known.

```text
Run the Paramaribo Letter growth desk.

SITE: https://www.paramariboletter.com
X: @paramaribolette
INBOX: paramariboletter@gmail.com
ISSUE: [Default: latest in public/catalog.json]
GOAL: [e.g. launch week on X / improve subscribe CVR / 14-day experiment board]
STAGE: [Default: core three. Write "full growth desk" to also spawn partnerships_referral_manager and lifecycle_conversion.]
MODE: [Default: dry-run. APPROVE_SEND only if a human may post or email.]
AS-OF: current time + timezone.
WEEKLY_VISITORS: [Paste the latest Vercel week if known.]
SUBSCRIBER_COUNT: [Paste if known. Otherwise agents must say insufficient evidence — never invent.]

Use these project-scoped agents:
Core (always): growth_marketing_lead, editorial_content_lead, social_community_manager
X community (daily): mary_community_manager — spawn when GOAL includes community replies / Day-N engagement
Bench: partnerships_referral_manager, lifecycle_conversion

You are the moderator.

Round 0 — packet
1. Read prompts/letter-facts.md (baseline ~20 visitors/week, targets 60/week by 11 Oct and 100/week by 25 Oct, topic hubs, /subscribed signup counting, LinkedIn priority). Then load ISSUE title/dek/id, its URL as /issue?id={id}, and any SUBSCRIBER_COUNT or analytics the user pasted.
2. Remind everyone: educational / not advice; lenses ≠ authors; prefer paramariboletter.com links.
3. Paid ads and heavy partnerships stay frozen until visit→subscribe CVR is known. Signups count as /subscribed page views since 2026-09-27; say how many weeks of data exist.

Round 1 — parallel (no cross-talk)
Spawn growth_marketing_lead, editorial_content_lead, and social_community_manager together.
If STAGE is full growth desk, also spawn partnerships_referral_manager and lifecycle_conversion.

Round 2 — synthesis (moderator)
Merge into one publisher brief:
1. Stage target and bottleneck, scored against the visitor and signup targets in letter-facts.md
2. 14-day experiment board (from Growth)
3. Paste-ready content pack (from Editorial)
4. 7-day social calendar + reply rules (from Social)
5. Optional: partner warm-up / lifecycle backlog if those agents ran
6. Compliance pass
7. Explicit “do not post/send” unless MODE is APPROVE_SEND

Solo quick path (one agent only): use letter_marketing via prompts/run-letter-marketing.md.
```

## Role map

| Role | Agent id | When |
|---|---|---|
| Growth Marketing Lead | `growth_marketing_lead` | Always (core) |
| Editorial & Content Lead | `editorial_content_lead` | Always (core) |
| Social & Community Manager | `social_community_manager` | Always (core) |
| Partnerships & Referral Manager | `partnerships_referral_manager` | After funnel converts / full desk |
| Lifecycle & Conversion Specialist | `lifecycle_conversion` | After funnel converts / full desk |

## Guardrails

- North star 500k is a horizon, not a claim about today.
- No bots, pods, fake testimonials, or signal-service positioning.
- Resend notify already covers “new issue” email when secrets are set — don’t duplicate poorly.
