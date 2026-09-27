# Two-team operating model — The Paramaribo Letter

The desk runs as **two teams**. Do not mash their jobs. Conductor (or you) can oversee both; Codex handles X / LinkedIn / Gmail with `APPROVE_SEND`.

---

## Team A — Growth & Promotion

**Owns:** marketing, social media, partnerships, subscriber growth, funnel measurement, free-tool stack.

| Role | Agent id | Default |
|---|---|---|
| Growth Marketing Lead | `growth_marketing_lead` | Core |
| Editorial & Content Lead *(distribution copy / Content Writer)* | `editorial_content_lead` | Core |
| Social & Community Manager *(cadence)* | `social_community_manager` | Core |
| **Mary — X Community Manager** *(replies / relationships)* | `mary_community_manager` | Daily X community |
| Partnerships & Referral Manager | `partnerships_referral_manager` | After CVR known |
| Lifecycle & Conversion Specialist | `lifecycle_conversion` | After CVR known / funnel work |
| Letter marketing (solo) | `letter_marketing` | Quick path only |

**Mary** grows @paramaribolette toward **1,000** real followers: **5–10** replies/day, daily sourced chart (~**8:30 AM Central**), scenario analysis 2–3×/week. Letter issues stay with Team B / Content Writer; Mary owns X community + chart distribution. Prompt: `prompts/run-mary-community.md`.

**X security block:** If the browser check fails — no workarounds. Copy + click paths; human posts; Mary verifies from screenshots/permalinks.

**After Team B publishes:** run `prompts/run-team-a-growth-loop.md` (existing Team A agents only; no new agent; no ASTER).  
**Prompt:** `prompts/run-letter-growth-desk.md`  
**Current facts (read first):** `prompts/letter-facts.md`  
**Canon:** `public/marketing/project-plan.md` · `free-services.md` · `launch-status.md` · `content-performance.csv`  
**Primary KPI:** legitimate new newsletter subscribers per 1,000 impressions. Never invent counts.  
**Channels:** site subscribe (Resend) · X @paramaribolette · LinkedIn Newsletter · Gmail inbox  
**Guardrails:** freeze paid ads & heavy partnerships until visit→subscribe CVR is measured; never invent list sizes; dry-run unless `APPROVE_SEND`.

```text
Run Team A — Growth & Promotion.

SITE: https://www.paramariboletter.com
X: @paramaribolette
LINKEDIN: https://www.linkedin.com/newsletters/the-paramaribo-letter-7498641775679426560/
INBOX: paramariboletter@gmail.com
ISSUE: [default: latest in public/catalog.json]
GOAL: [e.g. promote the latest issue / hit 60 visitors a week by 11 Oct / raise /subscribed rate]
STAGE: [core three | full Team A]
MODE: [dry-run | APPROVE_SEND <named items only>]
AS-OF: current time + timezone
SUBSCRIBER_COUNTS: [paste LinkedIn / Resend separately, or say unknown]

Spawn: growth_marketing_lead, editorial_content_lead, social_community_manager
(+ partnerships_referral_manager, lifecycle_conversion if STAGE is full Team A)

Moderator synthesizes one publisher brief. Do not rewrite research conclusions.
Do not post/send unless MODE names APPROVE_SEND items.
```

---

## Team B — Editorial & Publishing

**Owns:** research, writing, editing, newsletter production, release to the archive (site).

| Layer | Agents |
|---|---|
| Managing Editor | `research_director` |
| Crypto core | `killa_quant`, `macro_liquidity`, `bang_technician`, `glassnode_onchain`, `bitwise_fundamentals`, `leopold_ai_scaling`, `cowen_cycle_risk` |
| Crypto bench | `eth_platform`, `hayes_crypto_credit`, `policy_regulation`, `carter_monetary`, `murad_meme`, `hasu_incentives`, `cryptoquant_flows`, `options_vol`, `capriole_systematic` |
| Round two | `risk_red_team` |
| Equity desk (separate session) | `filings`, `earnings`, `sector`, `insider`, `chatter`, `chief_of_staff` |

**Prompts:** `run-paramaribo-letter.md` · `run-crypto-council.md` · `run-equity-desk.md` · `daily-btc-pulse.md`  
**Release:** in the website checkout (start from `website/main`), add `public/issues/{id}.json` + `.body.html` + cover → `python3 scripts/publish_letter.py --rebuild` (also rebuilds issue pages, topic hubs, sitemap, feed) → push `website` `main` (Vercel). Never copy `public/` wholesale from investment-research. Steps: `run-paramaribo-letter.md` → After the draft.  
**Guardrails:** educational / not advice; one `<p>` per agent stand; cash & insufficient evidence valid; lenses ≠ authors; never delete archive issues.

```text
Run Team B — Editorial & Publishing.

PACKET: [paste timestamped evidence]
AS-OF: [time + timezone]
SCOPE: [pulse | core seven | full crypto bench | full bench + equity | letter only]
MODE: [memo only | publish Issue N]
ISSUE_META: [Vol/Issue, slug, cover path if publishing]

Round 1: spawn research lenses in parallel (no cross-talk).
Round 2: risk_red_team on the leading thesis.
Round 3: research_director → letter-ready synthesis (headline, scenarios, one paragraph per stand).
If MODE is publish: follow run-paramaribo-letter.md "After the draft" (website checkout, new issue files only, publish_letter.py --rebuild, push website/main).
Do not post to X/LinkedIn (that is Team A).
```

---

## Handoff between teams

```
Team B publishes issue on site
        ↓
Team A receives: issue id, URL, title, dek, cover, 2–3 pull quotes, compliance notes
        ↓
Run prompts/run-team-a-growth-loop.md (existing Team A only)
        ↓
Team A dry-run pack → human APPROVE_SEND → X / LinkedIn / email notify (Resend path)
        ↓
Team A logs content-performance.csv + weekly visitors, /subscribed visitors, /topics visitors, LinkedIn, Resend
        ↓
Before next Team B cycle: 5-question report to Research Director (unavailable until data)
```

| Say this | Who runs |
|---|---|
| **Team A** / **Growth** | Growth & Promotion |
| **Team B** / **Editorial** / **publish Issue N** | Editorial & Publishing |
| **Both teams** | B first (or already published), then A on that issue |
| **Day N** | Usually Team A sprint clock; B only if a new packet exists |

## Split of names that collide

- **Team B “editorial”** = research letter (Managing Editor + council).  
- **Team A `editorial_content_lead`** = *distribution* copy (hooks, threads, LinkedIn editions) — does not change the research conclusion.
