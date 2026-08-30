# The Paramaribo Letter — Project Plan

Canonical publisher plan for Codex and the growth desk. Keep channel counts honest; never invent subscriber totals.

## Mission

Build The Paramaribo Letter into a trusted, evidence-driven research publication covering Bitcoin, macro liquidity, equities, and event risk.

Long-term goal: grow toward 500,000 email subscribers through consistent publishing, useful analysis, organic distribution, referrals, and measurable conversion improvements.

500,000 is a long-term horizon—not a guaranteed outcome. Use milestones: 100 → 250 → 1,000 → 10,000 → 50,000 → 100,000 → 500,000.

## Live assets

- Website: https://www.paramariboletter.com/
- X account: https://x.com/paramaribolette
- LinkedIn Newsletter: https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/
- GitHub repository: https://github.com/edta27/paramaribo-letter
- Vercel project: `paramaribo-letter`
- Agents page: https://www.paramariboletter.com/agents
- Archive: https://www.paramariboletter.com/#archive-wrap
- Desk: https://www.paramariboletter.com/desk
- Subscribe form: https://www.paramariboletter.com/#new-subscribers
- Publisher notes: https://www.paramariboletter.com/marketing
- Free services playbook: `public/marketing/free-services.md`
- RSS: https://www.paramariboletter.com/feed.xml
- Sitemap: https://www.paramariboletter.com/sitemap.xml

## Work completed

### Website and deployment

- Custom domain is live.
- Vercel project logo/avatar was uploaded.
- Favicon/logo was added and deployed.
- Vercel project was renamed to `paramaribo-letter`.
- Subscribe form, Resend path, thank-you modal, and unsubscribe flow are present.
- Vercel Web Analytics was added to the site pages.
- Marketing documents were repaired after returning 404 errors.
- Old `.md` links now redirect to working browser pages:
  - https://www.paramariboletter.com/marketing/launch-status
  - https://www.paramariboletter.com/marketing/linkedin-launch

### X

Profile updates completed:

- Display name: The Paramaribo Letter
- Handle: `@paramaribolette`
- Website: https://www.paramariboletter.com/
- Location: Independent research desk
- Bio: Desk notes from a multi-agent research council on Bitcoin, macro & equities. Educational — not advice. Cash is valid. Archive kept.
- Header image uploaded.
- Purple P avatar retained.

Published:

- Pinned launch post: https://x.com/paramaribolette/status/2093566708900335894
- Issue 12 post: https://x.com/paramaribolette/status/2093566847735996596
- Day 2 “What is an agent?” post: https://x.com/paramaribolette/status/2093570419361997076

X has shown an “Unlock more on X” human-engagement prompt. Build genuine engagement through replies and conversations before increasing promotional volume.

### LinkedIn

The LinkedIn Newsletter is already live:

- Name: The Paramaribo Letter
- Subscribers: 56
- Editions: 3
- Frequency currently shown as: Published daily
- Description: An evidence-driven research desk on Bitcoin, macro liquidity, and event risk. Multiple lenses, one evidence packet.
- Newsletter is featured on Shan Ho’s personal profile.
- Public URL: https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/

The LinkedIn Issue 12 edition still needs to be published.

## Two-team model

See `prompts/run-two-teams.md`.

### Team A — Growth & Promotion

Marketing, social, partnerships, subscriber growth. Agents: `growth_marketing_lead`, `editorial_content_lead` (distribution copy), `social_community_manager`, `partnerships_referral_manager`, `lifecycle_conversion` (+ solo `letter_marketing`).

1. Growth Marketing Lead — strategy, funnel, experiments, milestones  
2. Editorial and Content Lead — hooks, pull quotes, threads, LinkedIn editions (does not change research)  
3. Social and Community Manager — X/LinkedIn cadence and replies  
4. Partnerships and Referral Manager — after conversion is proven  
5. Lifecycle and Conversion Specialist — signup, welcome, analytics  

### Team B — Editorial & Publishing

Research, writing, editing, newsletter production, site release. Led by `research_director` + crypto council / equity desk. Publishes to `public/issues/` then hands the live URL to Team A.

## Immediate priorities

1. Publish Issue 12 as a LinkedIn Newsletter edition.
2. Decide whether “Published daily” accurately reflects the real publishing schedule. Use Weekly or Occasionally if publishing is event-driven.
3. Keep the public LinkedIn Newsletter URL in brand-channel notes (done when this plan was ingested).
4. Confirm Resend sender-domain authentication.
5. Confirm these Vercel environment settings:
   - `SITE_URL=https://www.paramariboletter.com`
   - Resend sender address
   - `RESEND_REPLY_TO=paramariboletter@gmail.com`
   - GitHub notification secret
6. Verify visit-to-subscribe conversion.
7. Create a welcome sequence for new site subscribers.
8. Keep LinkedIn and Resend email subscribers as separate counts.
9. Consider creating a dedicated LinkedIn Page later; it is optional and not required for current publishing.

## First 14-day growth plan

### Days 1–3

- Publish LinkedIn Issue 12.
- Post one clear “What is an agent?” explanation.
- Share one strong pull quote from Issue 10 or Issue 11.
- Reply to every genuine question about the desk.

### Days 4–7

- Publish a subscription reminder linking to `#new-subscribers`.
- Publish one Bitcoin-levels explainer with conditional language.
- Run one reader question or poll.
- Review clicks, signup starts, completed signups, and source traffic.

### Days 8–10

- Test two homepage hooks.
- Test two subscription calls to action.
- Publish one archive post showing that old issues remain available.
- Cross-link the website, X account, LinkedIn Newsletter, and Agents page.

### Days 11–14

- Publish another issue or desk note.
- Create a short “how the bench works” thread.
- Begin a referral experiment only if signup conversion is measurable.
- Review the best-performing topics, hooks, and channels.

## Required measurement

Track separately:

- Website visitors
- Subscribe-form views
- Subscribe starts
- Completed subscribers
- Visit-to-subscribe conversion rate
- Email delivery rate
- Open rate
- Click rate
- Unsubscribe rate
- X impressions and profile visits
- LinkedIn impressions and newsletter subscribers
- Referral source

Do not combine:

- LinkedIn subscribers with Resend subscribers
- X followers with email subscribers
- Website visits with completed subscriptions

## Editorial rules

- Educational research only.
- Not personalized financial advice.
- No execution instructions.
- No leverage or position-sizing recommendations.
- No guaranteed targets.
- Use conditional language: “if,” “could,” “watch,” and “scenario.”
- Named traders and firms are analytical lenses; they do not write for The Paramaribo Letter.
- Cash and “insufficient evidence” remain valid conclusions.
- Preserve the archive; never delete older issues to make room for new ones.
- Use the custom domain in all public links.

## Growth guardrails

- Do not buy paid ads until visit-to-subscribe conversion is known.
- Do not pursue heavy partnerships until the signup funnel is working.
- Prioritize useful analysis and organic distribution.
- Keep the five-role desk focused on measurable experiments.
- Every public social post, reply, newsletter edition, or profile change requires explicit approval before publishing when an assistant is performing the action.

## Next action

**Day 1 closed.** Overnight handoff: `public/marketing/day-2-handoff.md`.

1. Wake → say **Day 2** to Conductor (oversee: verify events live, measurement log).
2. Paste Day 2 Codex prompt from that handoff for X / LinkedIn / Gmail (`APPROVE_SEND` per item).
3. If events not on prod yet: authorize **push to main and deploy** in the letter repo first.
4. Measure visit→subscribe before scaling promo. Partnerships/ads stay frozen.

Paste-ready edition: `public/marketing/linkedin-launch.md`  
Growth desk: `prompts/run-letter-growth-desk.md` · Luna Max sprint: `prompts/run-codex-luna-max-sprint.md`  
Vercel baseline (2026-08-29): ~4 visitors / 1w · Web Analytics on · production Ready.
