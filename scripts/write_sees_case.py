#!/usr/bin/env python3
"""Write the first Investor Case Studies pack (See's Candies, 1972)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "cases"
CATALOG = OUT / "catalog.json"

SUMMARY = """
<p>In early 1972, Blue Chip Stamps — a trading-stamp company that Warren Buffett, Charlie Munger, and Berkshire Hathaway already controlled — bought control of See’s Candy Shops for cash. Buffett later described the true asking price, after excess cash, as $30 million and the price they actually paid as $25 million. They almost walked. Munger thought the business was worth the ask. Buffett, still thinking in tangible assets, would not go higher. The sellers took $25 million.</p>
<p>What they bought was not a growth rocket. Boxed-chocolate poundage in the United States was already a slow category. See’s was regional. Christmas dominated the year. The durable fact, as they later reconstructed it, was pricing power built on a consumer franchise: people paid for the name, the product, and the occasion, not for the cocoa beans on the balance sheet. Cash came in at the register. Inventories turned quickly. Almost all of the subsequent profit could be sent upstream and redeployed.</p>
<p>This case is about that decision process — the near-miss on price, the economics that were knowable, the risks that were already on the table, and the later results that are easy to over-fit. It is not a recommendation to buy candy stocks, copy a 1972 multiple, or treat “brand” as a magic word.</p>
"""

BODY = r"""
<h2 id="why-it-matters">Why this case matters</h2>
<p>See’s is the hinge in the Buffett–Munger partnership where “cheap relative to assets” stopped being the whole method. Buffett has said so in later letters, with the benefit of decades. That hindsight is useful only if we keep it labeled. The educational core is narrower: a high return on a small pile of tangible capital, plus the right to raise price without losing the customer, can be worth more than a larger pile of assets that earn a commodity return. Inflation, which was already a 1970s fact rather than a surprise, punishes the second kind of business and is kinder to the first.</p>
<p>It also matters because the purchase nearly failed for a reason that still shows up in real work: the buyer’s framework was tighter than the opportunity. A $5 million gap on a $30 million ask is not a rounding error in 1972 dollars. Process can be both too cautious and still lucky.</p>

<h2 id="who">Investor and company profiles</h2>
<p>Warren Buffett, then in his early forties, had already converted Berkshire Hathaway from a struggling New England textile mill into a vehicle that owned insurance and other businesses. Charlie Munger was the other controlling mind at Blue Chip Stamps, the California trading-stamp company that became the purchase vehicle. Berkshire later merged Blue Chip in; See’s did not start as a Berkshire line item on day one. That legal path matters. The cash that bought See’s was Blue Chip’s, and the first years of See’s cash went back to Blue Chip.</p>
<p>See’s Candy Shops was a West Coast manufacturer and retailer of boxed chocolates, selling mostly through its own shops rather than through grocery aisles. Buffett later called it a “legendary” regional name. Contemporaneous Blue Chip filings describe a candy subsidiary acquired in January 1972, with company-operated shops in western states, two California kitchens, and a business that was highly seasonal around Christmas. Charles N. Huggins, already under contract at See’s, was put in charge the day of the purchase. Buffett and Munger later described a handshake compensation arrangement that they said was never reduced to a written contract and remained unchanged for years — an incentive story they tell as culture, not as a template anyone else should copy without evidence.</p>

<h2 id="context">Historical and market context</h2>
<p>The early 1970s were not a quiet backdrop. The United States was moving into a decade of inflation, oil shocks, and a brutal 1973–74 bear market in equities. Blue Chip’s own core product — trading stamps given by grocers — was already in secular decline. Berkshire’s 1991 letter later put Blue Chip stamp sales at $102.5 million in 1972 and $1.2 million in 1991. That collapse is not a See’s fact, but it is the parent’s fact. A parent losing its original business has a capital-allocation problem: what to do with the cash and float the stamp operation still threw off while it shrank.</p>
<p>Buying a candy company with that cash was a redeployment, not a “synergy” story. Buffett has long mocked synergy as an excuse. See’s did not need Blue Chip’s stamps. Blue Chip needed a business that could take capital and return more than the dying stamp operation.</p>
<p>Blue Chip was also living with antitrust residue. Its 1972 Form 10-K still listed a long-running Sherman Act case involving Blue Chip and major California grocers. That litigation is about stamps, not chocolate. It is still part of the buyer’s condition: the vehicle that wrote the check was not a clean, boring cash pile. It was a contested, shrinking promotional business.</p>

<h2 id="before">The company before the purchase</h2>
<p>Buffett’s later letters do not pretend See’s was distressed. The 2007 letter says the See family had built a competitive advantage over about fifty years. Poundage in 1972, in that same letter, was 16 million pounds. The more detailed 1983 operating table — published eleven years after the deal, still the best year-by-year series Buffett put in a shareholder letter — shows 16.95 million pounds, $31.3 million of sales, $2.08 million of after-tax operating profit, and 167 stores at year-end 1972.</p>
<p>Those 1972 figures in the 1983 table do not perfectly match later roundings. The 1991 letter says 1972 sales of $29 million and pre-tax profit of $4.2 million. The 2007 letter says sales of $30 million and pre-tax earnings of less than $5 million, with $8 million of capital required. The 1983 goodwill appendix uses about $8 million of net tangible assets and about $2 million after tax, “rounded” and “greatly oversimplified.” This desk treats the 1983 table as the most granular operating history Buffett published, the 1991 letter as the most detailed <em>deal-structure</em> reconstruction (asking price, excess cash, $25 million ceiling), and the 2007/2014 letters as later owner’s-earnings recaps. Where they disagree, the difference is flagged rather than averaged into a fake precision.</p>
<p>What is consistent across those tellings: See’s was already earning a high return on a small tangible base, sold for cash, and did not need a large factory empire to grow a little.</p>

<h2 id="opportunity">The opportunity they identified</h2>
<p>The stated insight, in Buffett’s 1991 reconstruction, is short: they saw “untapped pricing power.” He does not publish a 1972 spreadsheet of price tests. He does not claim they ran a formal DCF that we can recover. The 1983 appendix is more explicit about the economic logic they were willing to own after the fact: a business that can earn far above market rates on net tangible assets has economic goodwill — a capitalized extra return — even if accountants later amortize a plug number called goodwill. The product’s value to the purchaser, not its production cost, set the price.</p>
<p>Munger’s role, in the 2014 “Past, Present and Future” letter, is the other half of the opportunity: he thought $30 million was a fair price for that franchise. Buffett did not. The opportunity, in other words, was visible enough that one partner was ready to pay the ask. It was not so obvious that both partners were eager.</p>
<aside class="interp" aria-label="Desk interpretation">
  <p><strong>Desk interpretation — not their memo.</strong> A 1972 buyer who only capitalized trailing earnings at a “cigar-butt” multiple would have seen a full price. A buyer who capitalized the right to lift price through a trusted gift brand would have seen a bargain relative to the cash the business could throw off in an inflationary decade. We do not have their contemporaneous workpapers. We have later letters that name pricing power as the insight and tangible-asset multiples as the hesitation.</p>
</aside>

<h2 id="misread">What the market may have misunderstood</h2>
<p>See’s was a private family company. There was no public equity “Mr. Market” mispricing in the 1973 Washington Post sense. The relevant “market” was the sellers’ reservation price and the scarcity of buyers who would pay three times tangible assets for a regional candy chain.</p>
<p>If there was a misunderstanding, it is the one Buffett later pinned on himself: treating $7–8 million of tangible net worth as the main yardstick when the franchise was the asset. The 1991 letter says they were “not yet fully appreciative of the value of an economic franchise.” That is a confession, not a 1972 newspaper clipping. Treat it as later self-report.</p>
<p>The boxed-chocolate category itself was easy to dismiss. Per-capita consumption, Buffett wrote in 2007, was extremely low and did not grow; many brands had disappeared. A dull industry is not automatically a bad business. It can be a screen that keeps empire-builders away while a regional winner keeps the gift occasion.</p>

<h2 id="thesis">The original investment thesis</h2>
<p>Reconstructed from what they later said they believed, not reverse-engineered from 2014’s $1.9 billion of cumulative pre-tax profit:</p>
<ul>
  <li><strong>Franchise over plants.</strong> The brand and the shop experience could support prices that a generic chocolate bar could not.</li>
  <li><strong>Capital lightness.</strong> Cash sales, short production and distribution cycles, seasonal debt rather than a permanent heavy balance sheet.</li>
  <li><strong>Quality as a non-negotiable.</strong> The 1983 letter treats ingredient quality as “sacred” even when commodity prices move. That is a cost choice, not a margin trick.</li>
  <li><strong>Manager already in the building.</strong> Huggins, not a search for a celebrity CEO after close.</li>
  <li><strong>Price discipline on the way in.</strong> $25 million was a hard ceiling. That is both a thesis (don’t overpay for a franchise you only half-understand) and a process risk (you might not get the franchise).</li>
</ul>
<p>What we should <em>not</em> claim: that they forecasted 2% annual poundage growth for thirty-five years, a 21.6% pre-tax margin in 1991, or that See’s would fund unrelated Berkshire acquisitions. Those are outcomes. The 2007 letter is explicit that unit growth was only about 2% a year from 16 million to 31 million pounds — a turtle, not a volume story.</p>

<h2 id="economics">Business model, moat, and pricing power</h2>
<p>See’s made boxed chocolates and sold them fresh through its own shops, with a large seasonal peak. The 1983 letter says quantity orders were about 25% of the total; the 1991 letter says the last two months of the year normally produced more than 80% of annual profits. That is a working-capital and operations fact as much as a brand fact. You hire thousands of seasonal people. You live or die by December. A gift purchase is less price-sensitive than a snack you buy for yourself — a distinction Munger also drew in later commentary — but it concentrates risk on a few weeks and on whether the name still means “the box you bring.”</p>
<p>Competitive advantage, as they described it, was not a patent or a regulated monopoly. It was accumulated customer experience. The 1983 appendix: a “pervasive favorable reputation” from “countless pleasant experiences” with product and personnel. That is economic goodwill. It can fade. It does not amortize in equal annual slivers just because an accountant is told to write off a $17 million plug over forty years.</p>
<p>Geographic concentration is the other side of the moat. The 2007 letter says See’s got the bulk of its revenues from only a few states and, in Buffett’s belief, accounted for nearly half of the industry’s earnings. A local fortress can be a real advantage and still be hard to clone nationally. They mostly did not clone it nationally. Volume per shop later stalled. Price did the compounding.</p>

<h2 id="management">Management quality and incentives</h2>
<p>Huggins is not a footnote. Buffett’s letters return to him the way they return to the Blumkins: an operator who already knew the business. The 1991 letter’s handshake contract is charming and unverifiable from the outside; we have only Buffett’s account. What is checkable in the operating table is the result under that manager: after-tax profit rising from about $2.1 million in 1972 to $13.7 million in 1983 while pounds went from 17.0 million to 24.7 million and stores from 167 to 207. Dollars grew faster than pounds. That is the pricing-plus-cost story, for better and worse.</p>
<p>The 1983 letter is not a victory lap on costs. Non-ingredient costs per pound had been rising faster than general inflation. Buffett called reversing that “vital.” Raw materials would one day deliver a “nasty surprise.” Quality would not be the release valve. That is a real operating constraint, written while Huggins was still in the chair, not after the legend hardened.</p>

<h2 id="valuation">Financial condition, valuation, and capital allocation</h2>
<p>Deal math, using the 1991 letter’s reconstruction:</p>
<ul>
  <li>Sellers’ nominal ask on a 100% basis: $40 million.</li>
  <li>Excess cash Buffett subtracts: $10 million, so a “true” ask of $30 million.</li>
  <li>Tangible net worth in that telling: $7 million.</li>
  <li>Price paid: $25 million.</li>
</ul>
<p>Desk calculations, labeled as such: $25 million is about 3.6 times the $7 million tangible figure in the 1991 letter, or about 3.1 times the $8 million net tangible assets in the 1983/2007 tellings. Against 1991’s $4.2 million of 1972 pre-tax profit, $25 million is about 6 times pre-tax. Against the 1983 table’s $2.08 million after tax, about 12 times after-tax earnings. The 2007 letter’s “60% pre-tax on invested capital” is $4.8 million on $8 million — consistent with “less than $5 million” pre-tax, and not independently audited here.</p>
<p>Position sizing: this was a controlling purchase of an operating company, not a 5% stock. Blue Chip used cash, not Berkshire shares. That choice looks even better after Dexter Shoe (1993), when Buffett paid $433 million in Berkshire stock for a shoe company whose advantage “vanished,” a mistake he later said cost shareholders far more than the headline price because the shares given away kept compounding (2007 letter: 25,203 A shares, later described as a $3.5 billion error; the 2014 letter restates the opportunity cost of those shares at about $5.7 billion as Berkshire itself grew). See’s is the opposite capital-allocation picture: cash in, cash out, no dilution.</p>
<p>After close, almost all earnings above a thin reinvestment were distributed to Blue Chip/Berkshire. The 1991 letter: $410 million of remaining pre-tax profits sent upstream over twenty years, with only $18 million of reinvested earnings on top of the original $7 million. The 2007 letter: $32 million reinvested, $1.35 billion of cumulative pre-tax earnings, 2006 sales $383 million and pre-tax profit $82 million on $40 million of capital. The 2014 letter: $1.9 billion cumulative pre-tax, $40 million of added investment. Those are different stop dates, not contradictions.</p>
<p>The 1983 Blue Chip merger into Berkshire created a second, accounting-only, goodwill layer: purchase accounting on the remaining 40% assigned $28.4 million of goodwill to See’s (and $23.3 million to the Buffalo News). That is not new candy economics. It is what happens when you pay with a valued stock for a stub you already effectively control. Do not confuse that entry with the 1972 cash decision.</p>

<h2 id="risks">Risks that were visible — and what could have failed</h2>
<p>Knowable in 1972, without magic:</p>
<ul>
  <li><strong>Seasonality.</strong> A business that earns most of its profit in a short holiday window can be wrecked by one bad Christmas, a mall-traffic shock, or a quality scare in November.</li>
  <li><strong>Commodities.</strong> Cocoa, sugar, and other inputs move. The 1983 letter says they will buy the finest ingredients anyway. That is a risk acceptance.</li>
  <li><strong>Cost inflation in shops.</strong> Labor and occupancy can outrun price if customers finally resist. Buffett was already worried about this by 1983.</li>
  <li><strong>Category stagnation.</strong> If pounds do not grow, the entire thesis sits on price and mix. That is fragile if the gift occasion fades or a cheaper box becomes “good enough.”</li>
  <li><strong>Geographic limits.</strong> A California name may not travel. Paying a franchise multiple for a local habit is a mistake if you silently assumed national share.</li>
  <li><strong>Parent distraction.</strong> Blue Chip’s stamp decline and legal overhang could have forced a bad sale, a starved brand, or a leveraged recap. They did not, but that was not guaranteed.</li>
  <li><strong>Key-person risk.</strong> A handshake with one operator is not a system.</li>
</ul>
<p>What would have falsified the purchase: a Daily-close equivalent for a private company — several years of failed price increases that did not stick, a collapse in December poundage, or a need to pour capital into stores just to stand still. The 1983 letter’s same-store poundage declines are a yellow flag they published themselves, even while dollars rose.</p>

<h2 id="after">Decisions after the purchase</h2>
<p>They did not flip the company. They did not lever it to recapture the $25 million. They put Huggins in charge and, by their account, left merchandising and quality with the people who already ran the shops. Prices rose over time — sometimes faster, as in the late 1970s and early 1980s, sometimes more modestly (the 1984 letter describes a much smaller per-pound increase). When non-ingredient costs ran hot, they treated that as a management problem, not as proof the franchise was dead.</p>
<p>They also did not find “another See’s.” Buffett’s 2007 line is the honest sequel: there are not many See’s in Corporate America. A typical company that takes earnings from $5 million to $82 million might need on the order of $400 million of extra capital. That comparison is illustrative, not a census. The transferable lesson is to ask how much extra capital a growth story consumes. The non-transferable lesson is to assume you will locate another cash machine with a fifty-year gift brand in a few states.</p>

<h2 id="results">Results, cash returned, and what changed</h2>
<p>Results below are nominal dollars as reported in the cited letters. They are not inflation-adjusted, not total-return IRRs computed by this desk, and not Berkshire’s share-price return.</p>
<ul>
  <li><strong>1972–1983 (1983 letter table).</strong> Sales $31.3 million → $133.5 million. After-tax operating profit $2.08 million → $13.7 million. Pounds 17.0 million → 24.7 million. Stores 167 → 207. Same-store poundage had already begun to slip.</li>
  <li><strong>1972–1991 (1991 letter).</strong> Sales $29 million → $196 million. Pre-tax $4.2 million → $42.4 million. 1991 pounds down 4% versus 1990, dollars flat, profits +7%, pre-tax margin 21.6%. Upstream pre-tax residual about $410 million.</li>
  <li><strong>Through 1999 (1999 letter).</strong> Cumulative pre-tax $857 million; operating margin a record 24% that year.</li>
  <li><strong>Through 2006/07 (2007 letter).</strong> 31 million pounds (~2% annual from 16 million). Sales $383 million, pre-tax $82 million, capital $40 million, cumulative pre-tax $1.35 billion, incremental capital $32 million.</li>
  <li><strong>Through 2014 (2014 letter).</strong> Cumulative pre-tax $1.9 billion; added investment $40 million.</li>
</ul>
<p>See’s did not pay a public dividend to outside shareholders after it was taken in. The “dividend” that matters is the cash sent to Blue Chip and then Berkshire, after corporate tax, which those letters say was used to buy other businesses. That is capital allocation at the parent, not a candy-coupon yield.</p>
<p>Mistakes and surprises, in their own telling: (1) the $25 million hard stop almost killed the deal; (2) volume growth was poor; (3) shop-level costs could outrun inflation; (4) they never replicated the model at will. The 1975 Waumbec textile purchase is Buffett’s own example, in the 2014 letter, that 1972 did not permanently cure cigar-butt backsliding.</p>

<h2 id="hindsight">Knowable then versus clear only later</h2>
<p><strong>Knowable then, or soon after:</strong> cash conversion, seasonality, regional concentration, high returns on tangible capital, a trusted name, a manager in place, a parent with shrinking stamps and cash to place, inflation already in the air, and a purchase price that was full versus assets and only reasonable versus franchise.</p>
<p><strong>Clear mainly in hindsight:</strong> that price could carry almost all of the economic work for decades; that 16 million pounds would only roughly double in thirty-five years; that cumulative pre-tax would be measured in ten figures; that See’s cash would seed other Berkshire compounders; that the same partnership would later destroy value by paying with Berkshire stock for a shoe company whose moat was not durable. Using 2014’s $1.9 billion to prove that $25 million was “obviously cheap” in 1972 is the error this section exists to block.</p>

<h2 id="principles">Transferable principles — and where they fail</h2>
<p>Useful as research habits, not as slogans:</p>
<ul>
  <li>Separate the tangible capital the business needs from the franchise that lets it price above cost.</li>
  <li>Ask how much extra capital is required to grow earnings. A wonderful business that cannot reinvest at high rates should throw off cash. That is a feature if the owner can redeploy. It is a trap if the owner cannot.</li>
  <li>Inflation is not automatically good for “hard assets.” The 1983 appendix’s point is the reverse: the See’s-type firm is hurt least because it must restock less capital to keep real earnings even.</li>
  <li>Pay with cash when you can. Paying with an undervalued or rapidly compounding parent stock is a different trade.</li>
  <li>Write down what would falsify the franchise: failed price increases, collapsing peak-season volume, capital intensity that was supposed to stay low.</li>
</ul>
<p>Do not apply the See’s lesson to:</p>
<ul>
  <li>Commodity manufacturers that must reinvest heavily just to stand still.</li>
  <li>Brands you cannot test for pricing power except by destroying them.</li>
  <li>High-growth stories whose working capital and capex absorb every dollar of earnings (Buffett’s $400 million illustration).</li>
  <li>Any security today because it “looks like See’s.” There is no ticker in this file to buy.</li>
</ul>

<h2 id="takeaways">Key takeaways</h2>
<ul>
  <li>The 1972 decision was a cash purchase of a regional cash-register franchise, made through Blue Chip, at a price the buyers treated as a ceiling rather than a steal they were sure of.</li>
  <li>The reconstructable thesis is pricing power plus low incremental capital, not a forecast of national expansion.</li>
  <li>Volume was the disappointment; cash generation was the result. Those can coexist.</li>
  <li>Later cumulative profit figures are owner’s scorekeeping. They are not the 1972 memo.</li>
  <li>The partnership still made capital-allocation errors afterward. See’s did not make them permanently wise.</li>
</ul>
"""

TIMELINE = [
    {
        "when": "Dec 21, 1971",
        "what": "Blue Chip and the sellers sign a stock-purchase agreement covering See’s Candy Shops.",
        "source": "Blue Chip Stamps Form 10-K for fiscal 1972, exhibit list",
    },
    {
        "when": "Jan 3–Mar 4, 1972",
        "what": "Blue Chip acquires 93% of See’s common stock for cash. Filings later show 98.5% owned by May 10, 1972.",
        "source": "Blue Chip Stamps Form 10-K for fiscal 1972",
    },
    {
        "when": "1972 operating year",
        "what": "See’s: about 17 million pounds, $31.3 million sales, $2.08 million after-tax operating profit, 167 shops (1983 letter table). Deal price later stated as $25 million cash.",
        "source": "Berkshire 1983 letter; 1991 letter for the $25 million figure",
    },
    {
        "when": "1972–1983",
        "what": "Pounds grow slowly; dollars and profits grow faster. Same-store poundage begins to slip. Non-ingredient costs run hot, then get attention.",
        "source": "Berkshire 1983 letter",
    },
    {
        "when": "1983",
        "what": "Berkshire finishes merging Blue Chip. Purchase accounting assigns additional See’s goodwill on the remaining 40%. Not a new candy thesis.",
        "source": "Berkshire 1983 letter, goodwill appendix",
    },
    {
        "when": "1991",
        "what": "Buffett retells the $40 / $30 / $25 million ask-versus-pay story and twenty years of upstream cash.",
        "source": "Berkshire 1991 letter",
    },
    {
        "when": "2007 / 2014",
        "what": "Owner’s recap: slow poundage, high returns on tangible capital, cumulative pre-tax $1.35 billion then $1.9 billion. Dexter named as the gruesome inverse (stock, not cash; moat that vanished).",
        "source": "Berkshire 2007 letter; 2014 Past, Present and Future",
    },
]

FIGURES = {
    "caption": "See’s operating snapshot as Buffett later published it (nominal dollars)",
    "columns": ["Checkpoint", "Sales", "Profit figure given", "Pounds", "Capital / tangible", "Source"],
    "rows": [
        [
            "1972 (1983 table)",
            "$31.3 million",
            "$2.08 million after tax",
            "16.95 million",
            "167 shops; NTA later rounded to ~$8 million",
            "1983 letter table; 1983 appendix",
        ],
        [
            "1972 (1991 retelling)",
            "$29 million",
            "$4.2 million pre-tax",
            "—",
            "$7 million tangible net worth",
            "1991 letter",
        ],
        [
            "1972 (2007 retelling)",
            "$30 million",
            "Less than $5 million pre-tax",
            "16 million",
            "$8 million capital; ~60% pre-tax return",
            "2007 letter",
        ],
        [
            "1983",
            "$133.5 million",
            "$13.7 million after tax",
            "24.65 million",
            "207 shops",
            "1983 letter table",
        ],
        [
            "1991",
            "$196 million",
            "$42.4 million pre-tax; 21.6% margin",
            "Down 4% vs 1990",
            "$25 million net worth; $18 million reinvested since 1972",
            "1991 letter",
        ],
        [
            "2006 / 2007 letter",
            "$383 million",
            "$82 million pre-tax; $1.35 billion cumulative",
            "31 million",
            "$40 million capital; $32 million reinvested since 1972",
            "2007 letter (prior year)",
        ],
        [
            "2014 letter",
            "—",
            "$1.9 billion cumulative pre-tax",
            "—",
            "$40 million added investment",
            "2014 Past, Present and Future",
        ],
    ],
    "note": "Desk did not restate these figures for inflation, splits, or tax-rate changes. Sales and profit columns mix pre-tax and after-tax on purpose so the source’s own wording is preserved. Empty cells mean that letter did not give the number.",
}

TOC = [
    {"id": "summary", "title": "Executive summary"},
    {"id": "why-it-matters", "title": "Why this case matters"},
    {"id": "who", "title": "Investor and company profiles"},
    {"id": "context", "title": "Historical and market context"},
    {"id": "before", "title": "The company before the purchase"},
    {"id": "opportunity", "title": "The opportunity they identified"},
    {"id": "misread", "title": "What the market may have misunderstood"},
    {"id": "thesis", "title": "The original investment thesis"},
    {"id": "economics", "title": "Business model, moat, and pricing power"},
    {"id": "management", "title": "Management quality and incentives"},
    {"id": "valuation", "title": "Valuation and capital allocation"},
    {"id": "risks", "title": "Risks and what could have failed"},
    {"id": "after", "title": "Decisions after the purchase"},
    {"id": "results", "title": "Results over time"},
    {"id": "hindsight", "title": "Knowable then versus hindsight"},
    {"id": "principles", "title": "Transferable principles"},
    {"id": "takeaways", "title": "Key takeaways"},
    {"id": "sources", "title": "Sources"},
]

SOURCES = [
    {
        "title": "Berkshire Hathaway Chairman’s letter, 1983 (See’s operating table and goodwill appendix)",
        "url": "https://www.berkshirehathaway.com/letters/1983.html",
        "kind": "Primary",
        "date": "1984",
        "note": "Best contemporaneous-style operating series and the economic-goodwill explanation. Buffett notes some figures in the appendix are rounded and simplified.",
    },
    {
        "title": "Berkshire Hathaway Chairman’s letter, 1991 (deal structure: $40 / $30 / $25 million)",
        "url": "https://www.berkshirehathaway.com/letters/1991.html",
        "kind": "Primary",
        "date": "1992",
        "note": "Most detailed published reconstruction of the ask, excess cash, and $25 million ceiling.",
    },
    {
        "title": "Berkshire Hathaway Chairman’s letter, 1999 (cumulative pre-tax $857 million; 24% operating margin)",
        "url": "https://www.berkshirehathaway.com/letters/1999htm.html",
        "kind": "Primary",
        "date": "2000",
    },
    {
        "title": "Berkshire Hathaway Chairman’s letter, 2007 (16 million vs 31 million pounds; $1.35 billion cumulative; Dexter $433 million in 25,203 A shares)",
        "url": "https://www.berkshirehathaway.com/letters/2007ltr.pdf",
        "kind": "Primary",
        "date": "2008",
        "note": "Also the source for “there aren’t many See’s” and the Dexter contrast.",
    },
    {
        "title": "Berkshire Hathaway, “Past, Present and Future” (2014)",
        "url": "https://www.berkshirehathaway.com/SpecialLetters/WEB%20past%20present%20future%202014.pdf",
        "kind": "Primary",
        "date": "2014",
        "note": "Munger’s $30 million view vs Buffett’s $25 million ceiling; $1.9 billion cumulative pre-tax; Dexter share opportunity cost restated at about $5.7 billion.",
    },
    {
        "title": "Berkshire Hathaway shareholder letters index",
        "url": "https://www.berkshirehathaway.com/letters/letters.html",
        "kind": "Primary",
        "date": "ongoing",
        "note": "Official letter library. Letters include copyrighted material reproduced with Berkshire’s permission on that site.",
    },
    {
        "title": "Blue Chip Stamps Form 10-K, fiscal year 1972",
        "url": "https://theoraclesclassroom.com/wp-content/uploads/2019/09/1972-Blue-Chip-Stamps-10K.pdf",
        "kind": "Primary filing (scan)",
        "date": "1972",
        "note": "Confirms cash acquisition of 93% of See’s between January 3 and March 4, 1972; 98.5% by May 10, 1972; December 21, 1971 stock-purchase agreement. OCR quality is poor; the $25 million figure is not independently recovered from this scan in this case study.",
    },
    {
        "title": "Blue Chip Stamps Form 10-K, fiscal year 1973",
        "url": "https://theoraclesclassroom.com/wp-content/uploads/2019/09/1973-Blue-Chip-Stamps-10K.pdf",
        "kind": "Primary filing (scan)",
        "date": "1973",
        "note": "Candy as a separate line of business acquired in January 1972; ownership later described at 99%.",
    },
    {
        "title": "Berkshire Hathaway Chairman’s letter, 1984 (modest 1984 price increase; same-store poundage)",
        "url": "https://www.berkshirehathaway.com/letters/1984.html",
        "kind": "Primary",
        "date": "1985",
    },
    {
        "title": "Berkshire Hathaway Chairman’s letter, 1990 (See’s physical volume; Kuwait/mall traffic)",
        "url": "https://www.berkshirehathaway.com/letters/1990.html",
        "kind": "Primary",
        "date": "1991",
    },
]

pack = {
    "id": "1972-sees-candies",
    "date": "2026-08-31",
    "kicker": "Investor Case Studies · 01",
    "title": "See’s Candies, 1972: the franchise they almost didn’t buy",
    "subtitle": "Blue Chip paid $25 million for a regional chocolatier. The lesson is the decision, not the later billions.",
    "dek": "Buffett and Munger bought See’s through Blue Chip Stamps at a hard $25 million ceiling. Reconstruct the thesis from filings and letters — pricing power, thin tangible capital, and a near-miss on price — without turning the later cash gusher into a 1972 prophecy.",
    "investors": ["Warren Buffett", "Charlie Munger"],
    "companies": ["See’s Candies", "Blue Chip Stamps", "Berkshire Hathaway"],
    "themes": [
        "Pricing power",
        "Economic goodwill",
        "Capital allocation",
        "Inflation",
        "Known risks",
    ],
    "readingMinutes": 22,
    "summaryHtml": SUMMARY.strip(),
    "toc": TOC,
    "timeline": TIMELINE,
    "figures": FIGURES,
    "bodyHtml": BODY.strip(),
    "sources": SOURCES,
    "disclaimer": (
        "This case study is provided for educational and historical purposes only. "
        "It is not investment advice, and historical results do not guarantee future outcomes. "
        "Named investors and firms are subjects of historical research — they do not write these notes "
        "and have not endorsed them. Short quotations from shareholder letters are used for analysis; "
        "read the originals on Berkshire’s site."
    ),
}

catalog = [
    {
        "id": pack["id"],
        "date": pack["date"],
        "kicker": pack["kicker"],
        "title": pack["title"],
        "dek": pack["dek"],
        "investors": pack["investors"],
        "companies": pack["companies"],
        "themes": pack["themes"],
        "readingMinutes": pack["readingMinutes"],
    }
]

OUT.mkdir(parents=True, exist_ok=True)
(OUT / f"{pack['id']}.json").write_text(json.dumps(pack, indent=2) + "\n")
CATALOG.write_text(json.dumps(catalog, indent=2) + "\n")
print("wrote", OUT / f"{pack['id']}.json")
print("wrote", CATALOG)
print("body chars", len(pack["bodyHtml"]))
