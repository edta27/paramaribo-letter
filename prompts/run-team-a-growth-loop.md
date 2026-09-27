# Autonomous Team A growth loop

**Do not create a new agent. Do not create ASTER.** Use existing Team A identities only.

Authoritative role files stay in `.codex/agents/`. This file only sequences them after Team B publishes.

## Handoff

Team B finishes: research → independent analysis → shared packet → debate → red team → verification → Research Director synthesis → site issue live.

Then Team A collaborates on **distribution** (not isolated content generators):

| Order | Agent | Job (existing) |
|---|---|---|
| 1 | `editorial_content_lead` | Publication assets from the live issue only |
| 2 | `growth_marketing_lead` | Distribution strategy + KPI frame |
| 3 | `social_community_manager` | Platform-native cadence (X/LinkedIn) |
| 4 | `mary_community_manager` | X replies, 8:30 CT chart, community |
| 5 | `lifecycle_conversion` | Reader behavior + conversion measurement |
| 6 | `letter_marketing` | Newsletter acquisition campaigns |
| 7 | `partnerships_referral_manager` | Organic distribution only; paid/heavy still frozen until CVR known |

Do not rewrite Team B conclusions. Growth data may change **which questions** we investigate next. It must never change **what conclusion** research reaches.

Every agent reads `prompts/letter-facts.md` first (URLs, topic hubs, signup counting, baseline and targets).

## Primary KPI

**Legitimate new newsletter subscribers per 1,000 impressions.**

Distinguish high impressions + low conversion from lower impressions + high conversion. The second can be more valuable.

Never invent impressions, clicks, or subscriber counts. If unknown, write `unavailable`.

Site-side numbers come from Vercel Web Analytics (Hobby plan, page views only): weekly visitors, /issue visitors, /topics visitors, and signups = /subscribed page views (measurable since 2026-09-27). Near-term targets: 60 visitors/week by 11 Oct 2026, 100 by 25 Oct, 10 email signups by 25 Oct.

## After every publication

Append a row to `public/marketing/content-performance.csv` (TOPIC, ARTICLE, HOOK, FORMAT, PLATFORM, POSTING TIME, IMPRESSIONS, ENGAGEMENT, CLICKS, SUBSCRIPTIONS, CONVERSION).

Before the next Team B cycle, Team A sends the Research Director five answers:

1. What topic attracted the most qualified readers?
2. What hook generated the most subscriptions?
3. What produced impressions but failed to convert?
4. What should we test next?
5. What should we stop repeating?

Claim no pattern until enough rows exist.

## Safety

No fake followers/subscribers, mass DMs, spam comments, manufactured engagement, impersonation, or platform workarounds. If publish access is blocked: finished copy + click path + APPROVE_SEND. Never claim a post went out without a permalink or human confirm.

X copy: `.cursor/skills/sound-human-on-x/SKILL.md` starting Issue 19.
