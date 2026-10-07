(function () {
  "use strict";

  const data = window.EMILY_LIVE;
  const root = document.getElementById("emily-live-root");
  if (!data || !root) return;

  const esc = (value) => String(value == null ? "—" : value)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  const n = (value, digits = 1) => Number.isFinite(Number(value)) ? Number(value).toFixed(digits) : "—";
  const signed = (value, suffix = "%", digits = 1) => {
    if (!Number.isFinite(Number(value))) return "—";
    const number = Number(value);
    return `${number >= 0 ? "+" : ""}${number.toFixed(digits)}${suffix}`;
  };
  const usd = (value) => {
    const number = Number(value);
    if (!Number.isFinite(number)) return "—";
    if (Math.abs(number) >= 1e12) return `$${(number / 1e12).toFixed(2)}T`;
    if (Math.abs(number) >= 1e9) return `$${(number / 1e9).toFixed(1)}B`;
    if (Math.abs(number) >= 1e6) return `$${(number / 1e6).toFixed(1)}M`;
    return `$${number.toLocaleString(undefined, {maximumFractionDigits: number >= 1000 ? 0 : 2})}`;
  };
  const when = (value) => {
    const date = new Date(value);
    if (Number.isNaN(date.valueOf())) return "—";
    return new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Chicago", month: "long", day: "numeric", year: "numeric",
      hour: "numeric", minute: "2-digit", timeZoneName: "short"
    }).format(date);
  };
  const metric = (label, score, note, slug, aria) => `
    <article class="emily-stat">
      <span class="emily-stat-label">${esc(label)}</span>
      <strong class="emily-score">${esc(score)} / 100</strong>
      <span class="emily-stat-note">${esc(note)}</span>
      <div class="emily-meter emily-meter--${esc(slug)}" aria-label="${esc(aria)}"><span style="width:${Math.max(0, Math.min(100, Number(score) || 0))}%"></span></div>
    </article>`;

  const deltaText = (value, suffix = "") => {
    if (!Number.isFinite(Number(value))) return "—";
    const number = Number(value);
    return `${number > 0 ? "+" : ""}${number.toFixed(1).replace(".0", "")}${suffix}`;
  };

  const dailyChangeCard = (label, value, note, tone) => `
    <article class="emily-change-card emily-change-card--${esc(tone)}">
      <span>${esc(label)}</span>
      <strong>${esc(value)}</strong>
      <p>${esc(note)}</p>
    </article>`;

  async function renderDailyChange() {
    const target = document.getElementById("emily-change-grid");
    const copy = document.getElementById("emily-change-copy");
    if (!target || !copy) return;
    try {
      const response = await fetch("/emily-history.json", { cache: "no-store" });
      if (!response.ok) throw new Error("History unavailable");
      const history = await response.json();
      const currentTime = new Date(data.updated_at).getTime();
      const previous = (Array.isArray(history) ? history : [])
        .filter((row) => new Date(row.updated_at).getTime() < currentTime)
        .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))[0];
      if (!previous) throw new Error("No prior snapshot");

      const btcMove = (Number(data.crypto.btc_price_usd) / Number(previous.btc_price_usd) - 1) * 100;
      const rotationMove = Number(data.scores.rotation) - Number(previous.rotation);
      const vulnerabilityMove = Number(data.scores.vulnerability) - Number(previous.vulnerability);
      const activeMove = Number(data.scores.active) - Number(previous.active);
      const priorLabel = new Intl.DateTimeFormat("en-US", {
        timeZone: "America/Chicago", month: "short", day: "numeric", hour: "numeric", minute: "2-digit"
      }).format(new Date(previous.updated_at));

      copy.textContent = `Compared with the prior automated snapshot from ${priorLabel} Central.`;
      target.innerHTML = [
        dailyChangeCard("BTC price", deltaText(btcMove, "%"), btcMove < 0 ? "Price weakened between snapshots." : "Price strengthened between snapshots.", btcMove < 0 ? "risk" : "calm"),
        dailyChangeCard("Alt rotation", deltaText(rotationMove, " pts"), rotationMove < 0 ? "Breadth weakened toward Bitcoin shelter." : "Participation broadened beyond Bitcoin.", rotationMove < 0 ? "risk" : "calm"),
        dailyChangeCard("Vulnerability", deltaText(vulnerabilityMove, " pts"), vulnerabilityMove > 0 ? "Shock-transmission capacity increased." : "Structural fragility eased.", vulnerabilityMove > 0 ? "watch" : "calm"),
        dailyChangeCard("Active panic", deltaText(activeMove, " pts"), activeMove > 0 ? `Stress evidence rose; the current band remains ${data.scores.active_band.toLowerCase()}.` : "Visible panic evidence receded.", activeMove > 0 ? "watch" : "calm"),
      ].join("");
    } catch (error) {
      copy.textContent = "The daily comparison will appear after two valid automated snapshots are available.";
      target.innerHTML = dailyChangeCard("Baseline", "Established", "Today's verified reading is the starting comparison point.", "neutral");
    }
  }

  const c = data.crypto || {};
  const s = data.scores || {};
  const fgi = data.sentiment || {};
  const d = data.derivatives || {};
  const agg = data.aggregated_derivatives || {};
  const st = data.stablecoins || {};
  const treasury = data.corporate_treasuries || {};
  const m = data.macro || {};
  const consumer = data.consumer || {};
  const equityRates = data.equity_rates || {};
  const wildcard = data.wildcard || {};
  const model = data.model || {};
  const sourceLinks = (data.sources || []).map((item) =>
    `<a href="${esc(item.url)}">${esc(item.label)}</a>`).join(" · ");
  const gaps = (model.missing || []).length
    ? `<p class="emily-sources"><strong>Unavailable today:</strong> ${esc(model.missing.join(" · "))}</p>`
    : `<p class="emily-sources"><strong>Coverage:</strong> all configured free feeds returned usable observations.</p>`;

  const vix = m.vix ? n(m.vix.value, 2) : "unknown";
  const ten = m.ten_year ? `${n(m.ten_year.value, 2)}%` : "unknown";
  const hy = m.hy ? `${n(m.hy.value, 2)}%` : "unknown";
  const oil = m.oil ? `$${n(m.oil.value, 2)}` : "unknown";
  const sp = m.sp500 ? signed(m.sp500.change_5obs_pct) : "unknown";
  const dollar = m.dollar ? signed(m.dollar.change_5obs_pct) : "unknown";
  const treasuryTotal = Number.isFinite(Number(treasury.total_holdings_btc))
    ? `${(Number(treasury.total_holdings_btc) / 1e6).toFixed(2)}M BTC`
    : "Awaiting snapshot";
  const treasuryDelta = Number.isFinite(Number(treasury.change_since_last_snapshot_btc))
    ? `${deltaText(treasury.change_since_last_snapshot_btc, " BTC")} since prior snapshot`
    : "Baseline being established";

  root.innerHTML = `
    <nav class="chart-jump-nav emily-jump-nav" aria-label="Emily dashboard sections">
      <a href="#emily-summary">Today</a>
      <a href="#emily-core">Market structure</a>
      <a href="#emily-context">Broader context</a>
      <a href="#emily-rules">Decision rules</a>
      <a href="#emily-method">Method</a>
    </nav>

    <section class="emily-hero" id="emily-summary">
      <div class="thesis-eyebrow"><i class="chart-live-dot" aria-hidden="true"></i> Emily · Daily automated market intelligence</div>
      <h1>${esc(data.headline)}</h1>
      <p class="lede">${esc(data.summary)}</p>
      <p class="emily-updated">Updated <time datetime="${esc(data.updated_at)}">${esc(when(data.updated_at))}</time> · ${esc(data.quality)} · Decision: <span class="emily-call">${esc(data.decision)}</span></p>
    </section>

    <section class="emily-status-grid" aria-label="Emily's market meters">
      ${metric("BTC / Alt rotation", s.rotation, s.rotation_regime, "green", `Rotation score ${s.rotation} out of 100`)}
      ${metric("Panic vulnerability", s.vulnerability, `${s.vulnerability_band}. Can a future shock travel quickly?`, s.vulnerability_slug, `Panic vulnerability ${s.vulnerability} out of 100`)}
      ${metric("Active panic", s.active, `${s.active_band}. Is synchronized panic visible now?`, s.active_slug, `Active panic ${s.active} out of 100`)}
    </section>

    <section class="emily-change" aria-labelledby="emily-change-title">
      <div class="emily-change-head">
        <div>
          <span class="chart-page-eyebrow">Since the last snapshot</span>
          <h2 id="emily-change-title">What changed today?</h2>
        </div>
        <p id="emily-change-copy">Loading the prior verified snapshot…</p>
      </div>
      <div id="emily-change-grid" class="emily-change-grid" aria-live="polite"></div>
    </section>

    <div class="note emily-meter-note"><strong>How to read this:</strong> vulnerability is not a crash probability. It measures the structure available to transmit a future surprise; active panic requires visible price damage, volatility, credit stress, deleveraging and liquidity contraction.</div>

    <section class="emily-section" id="emily-core" aria-labelledby="emily-core-title">
      <div class="chart-section-head emily-section-head">
        <div><span>01 · CURRENT STRUCTURE</span><h2 id="emily-core-title">What the market is doing now</h2></div>
        <p>The two highest-frequency modules remain open by default.</p>
      </div>
      <div class="emily-grid emily-grid--primary">
      <article class="emily-panel">
        <div class="feed-kicker">Daily crypto structure</div>
        <h2>Bitcoin and participation</h2>
        <ul>
          <li>BTC ${usd(c.btc_price_usd)} · ${signed(c.btc_change_24h_pct)} in 24 hours · ${signed(c.btc_change_7d_pct)} over seven days.</li>
          <li>ETH ${signed(c.eth_change_7d_pct)} over seven days and ${signed(c.eth_excess_7d_pp, " pp")} versus BTC.</li>
          <li>${n(c.alt_breadth_pct, 0)}% of ${esc(c.eligible_alts)} eligible large alts beat BTC; median excess return ${signed(c.median_alt_excess_pp, " pp")}.</li>
          <li>BTC dominance ${n(c.btc_dominance_pct, 2)}% · ${esc(c.dominance_read)}.</li>
        </ul>
        <p><strong>Read:</strong> ${esc(s.rotation_regime)}.</p>
      </article>

      <article class="emily-panel">
        <div class="feed-kicker">Leverage and liquidity</div>
        <h2>The propagation layer</h2>
        <ul>
          <li>Fear &amp; Greed: ${esc(fgi.value)} · ${esc(fgi.classification)}.</li>
          <li>Global derivatives open interest: ${usd(agg.global_open_interest_usd)} · ${n(agg.global_open_interest_to_market_cap_pct, 2)}% of crypto market cap across ${esc(agg.global_derivatives_venues)} venues.</li>
          <li>BTC cross-venue funding: ${signed(agg.btc_weighted_funding_pct, "%", 4)} · basis ${signed(agg.btc_weighted_basis_pct, "%", 3)} across ${esc(agg.btc_venues)} venues.</li>
          <li>Global liquidations: ${usd(agg.global_liquidations_24h_usd)} over 24 hours · BTC ${usd(agg.btc_liquidations_24h_usd)}.</li>
          <li>OKX cross-check: funding ${signed(d.funding_8h_pct, "%", 4)} · open interest ${usd(d.oi_usd)} · seven-day change ${signed(d.oi_change_7d_pct)}.</li>
          <li>USD stablecoin supply: ${usd(st.supply_usd)} · seven-day change ${signed(st.change_7d_pct)}.</li>
        </ul>
        <p><strong>Read:</strong> CoinMarketCap supplies the cross-venue view; OKX remains an independent venue check. Missing values remain unknown.</p>
      </article>

      </div>
    </section>

    <section class="emily-section" id="emily-context" aria-labelledby="emily-context-title">
      <div class="chart-section-head emily-section-head">
        <div><span>02 · BROADER CONTEXT</span><h2 id="emily-context-title">The slower transmission map</h2></div>
        <p>Open a module when you need its full evidence table and methodology.</p>
      </div>
      <div class="emily-grid emily-grid--disclosures">

      <details class="emily-panel emily-panel--wide emily-disclosure">
        <summary>
          <span><small>Consumer exhaustion</small><strong>Are households spending beyond their income support?</strong></span>
          <span class="emily-disclosure-status">${esc(consumer.score)} / 100 · ${esc(consumer.band)}</span>
        </summary>
        <div class="emily-disclosure-body">
        <div class="emily-table-wrap">
          <table class="emily-table">
            <thead><tr><th>Evidence</th><th>Latest reading</th><th>Interpretation</th></tr></thead>
            <tbody>
              <tr><td>Real consumer spending</td><td>${signed(consumer.real_spending_change_3obs_pct)}</td><td>Three-observation change in inflation-adjusted spending.</td></tr>
              <tr><td>Real disposable income</td><td>${signed(consumer.real_income_change_3obs_pct)}</td><td>The income available to sustain that spending.</td></tr>
              <tr><td>Spending minus income</td><td>${signed(consumer.spending_income_gap_3obs_pp, " pp")}</td><td>A persistent positive gap can signal reliance on saving or credit.</td></tr>
              <tr><td>Personal saving rate</td><td>${n(consumer.saving_rate_pct, 1)}%</td><td>A thinner household buffer raises sensitivity to a labor or price shock.</td></tr>
              <tr><td>Consumer sentiment</td><td>${n(consumer.sentiment_index, 1)}</td><td>Soft data can weaken before hard spending rolls over.</td></tr>
            </tbody>
          </table>
        </div>
        <p><strong>Consumer Exhaustion score:</strong> ${esc(consumer.score)} / 100 · ${esc(consumer.band)}. It raises panic vulnerability only when spending-income divergence, low saving and weak sentiment agree.</p>
        <p class="emily-updated">Latest monthly observation set through ${esc(consumer.date)}. This is a slow-moving vulnerability signal, not evidence of active panic.</p>
        </div>
      </details>

      <details class="emily-panel emily-panel--wide emily-disclosure">
        <summary>
          <span><small>Equity–rates divergence</small><strong>Are growth equities ignoring expensive money?</strong></span>
          <span class="emily-disclosure-status">${esc(equityRates.score)} / 100 · ${esc(equityRates.band)}</span>
        </summary>
        <div class="emily-disclosure-body">
        <div class="emily-table-wrap">
          <table class="emily-table">
            <thead><tr><th>Evidence</th><th>Latest reading</th><th>Interpretation</th></tr></thead>
            <tbody>
              <tr><td>Nasdaq momentum</td><td>${signed(equityRates.nasdaq_change_5obs_pct)}</td><td>Strong growth-stock momentum can conceal weakening participation elsewhere.</td></tr>
              <tr><td>Distance from 45-day high</td><td>${signed(equityRates.nasdaq_distance_from_45d_high_pct)}</td><td>A reading near zero means the Nasdaq remains close to its recent high.</td></tr>
              <tr><td>10-year Treasury</td><td>${n(equityRates.ten_year_yield_pct, 2)}% · ${signed(equityRates.ten_year_change_5obs_bp, " bp", 0)}</td><td>High or rising long yields increase the discount rate applied to future earnings.</td></tr>
              <tr><td>Nasdaq minus S&amp;P 500</td><td>${signed(equityRates.nasdaq_vs_sp500_5obs_pp, " pp")}</td><td>A leadership proxy—not a full breadth measure—for whether growth stocks are doing most of the lifting.</td></tr>
              <tr><td>Shock pricing</td><td>VIX ${n(equityRates.vix, 2)} · HY ${n(equityRates.hy_spread_pct, 2)}%</td><td>Calm volatility and credit alongside expensive money can indicate latent complacency.</td></tr>
            </tbody>
          </table>
        </div>
        <p><strong>Equity–Rates Divergence score:</strong> ${esc(equityRates.score)} / 100 · ${esc(equityRates.band)}. ${esc(equityRates.interpretation)}</p>
        <p class="emily-updated">Latest available observation: ${esc(equityRates.latest_date)}. This module contributes to panic vulnerability but never raises active panic by itself.</p>
        </div>
      </details>

      <details class="emily-panel emily-panel--wide emily-disclosure">
        <summary>
          <span><small>Surrounding markets</small><strong>Is stress synchronizing?</strong></span>
          <span class="emily-disclosure-status">VIX ${esc(vix)} · HY ${esc(hy)}</span>
        </summary>
        <div class="emily-disclosure-body">
        <div class="emily-table-wrap">
          <table class="emily-table">
            <thead><tr><th>Channel</th><th>Latest</th><th>Why it matters</th></tr></thead>
            <tbody>
              <tr><td>Equity volatility</td><td>VIX ${esc(vix)}</td><td>A rapid rise shows fear spreading beyond crypto.</td></tr>
              <tr><td>Credit</td><td>HY spread ${esc(hy)}</td><td>Widening credit spreads reduce the market's shock absorber.</td></tr>
              <tr><td>Rates</td><td>10-year ${esc(ten)}</td><td>High long yields tighten financial conditions.</td></tr>
              <tr><td>Energy</td><td>WTI ${esc(oil)}</td><td>An oil shock can revive inflation and policy stress.</td></tr>
              <tr><td>Equities</td><td>Five-observation move ${esc(sp)}</td><td>Confirms or rejects broad risk-off transmission.</td></tr>
              <tr><td>Dollar</td><td>Five-observation move ${esc(dollar)}</td><td>A fast dollar rise can drain global liquidity.</td></tr>
            </tbody>
          </table>
        </div>
        <p class="emily-updated">Latest available macro date: ${esc(model.latest_macro_date)}. Traditional-market feeds naturally lag on weekends and holidays.</p>
        </div>
      </details>

      <details class="emily-panel emily-panel--wide emily-disclosure">
        <summary>
          <span><small>Corporate treasury concentration</small><strong>Who is absorbing Bitcoin supply—and how concentrated is it?</strong></span>
          <span class="emily-disclosure-status">${esc(treasuryTotal)} · ${n(treasury.top_holder_share_pct, 1)}% top holder</span>
        </summary>
        <div class="emily-disclosure-body">
        <div class="emily-table-wrap">
          <table class="emily-table">
            <thead><tr><th>Evidence</th><th>Latest reading</th><th>Interpretation</th></tr></thead>
            <tbody>
              <tr><td>Public companies</td><td>${esc(treasury.company_count)}</td><td>Companies included in CoinMarketCap's current public treasury table.</td></tr>
              <tr><td>Total holdings</td><td>${Number.isFinite(Number(treasury.total_holdings_btc)) ? `${Number(treasury.total_holdings_btc).toLocaleString()} BTC` : "—"}</td><td>${n(treasury.share_of_max_supply_pct, 2)}% of Bitcoin's fixed 21 million maximum supply.</td></tr>
              <tr><td>Largest holder</td><td>${esc(treasury.top_holder?.name)} · ${Number.isFinite(Number(treasury.top_holder?.holdings_btc)) ? `${Number(treasury.top_holder.holdings_btc).toLocaleString()} BTC` : "—"}</td><td>${n(treasury.top_holder_share_pct, 2)}% of reported public-company holdings.</td></tr>
              <tr><td>Top-ten concentration</td><td>${n(treasury.top_10_share_pct, 2)}%</td><td>Higher concentration makes aggregate treasury demand more dependent on a small number of issuers.</td></tr>
              <tr><td>Largest country exposure</td><td>${esc(treasury.top_country)} · ${n(treasury.top_country_share_pct, 1)}%</td><td>Shows the jurisdiction where reported corporate holdings are most concentrated.</td></tr>
              <tr><td>Daily history</td><td>${esc(treasuryDelta)}</td><td>A change appears after two valid Emily snapshots; it is not inferred when the source is unavailable.</td></tr>
            </tbody>
          </table>
        </div>
        <p><strong>Read:</strong> corporate accumulation can absorb liquid supply, while concentrated ownership can create reflexive risk if a major holder faces financing pressure. This context does not change Active Panic by itself.</p>
        <p class="emily-updated">Latest source-table observation: ${esc(treasury.latest_disclosure_date)}. ${esc(treasury.source_caveat)} The feed is optional and fail-closed.</p>
        </div>
      </details>

      <details class="emily-panel emily-panel--wide emily-disclosure">
        <summary>
          <span><small>Wildcard early warning</small><strong>What could abruptly change the regime?</strong></span>
          <span class="emily-disclosure-status">Gate · ${esc(wildcard.market_gate)}</span>
        </summary>
        <div class="emily-disclosure-body">
        <p><strong>External-event evidence:</strong> ${esc(wildcard.evidence_state)}. <strong>Jump risk:</strong> ${esc(wildcard.jump_risk)}. <strong>Market-transmission gate:</strong> ${esc(wildcard.market_gate)}.</p>
        <p>${esc(wildcard.market_read)}</p>
        <div class="emily-table-wrap">
          <table class="emily-table">
            <thead><tr><th>State</th><th>Evidence requirement</th><th>Examples Emily watches</th></tr></thead>
            <tbody>
              <tr><td>0 · Unverified signal</td><td>A claim, isolated event or anomaly without independent confirmation.</td><td>Rumors, a single report or an unexplained market move.</td></tr>
              <tr><td>1 · Verified first-order event</td><td>Multiple credible sources establish that the event occurred.</td><td>Confirmed outbreak, policy action, conflict or infrastructure failure.</td></tr>
              <tr><td>2 · Sustained transmission</td><td>The effect persists beyond its origin instead of remaining contained.</td><td>Secondary spread, supply interruption, funding stress or repeated operational failures.</td></tr>
              <tr><td>3 · Geographic or sector expansion</td><td>Independent regions, industries or financial channels become affected.</td><td>Cross-border spread, shipping rerouting, energy/fertilizer shock or banking contagion.</td></tr>
              <tr><td>4 · Behavioral or policy response</td><td>Households, firms or governments materially change behavior.</td><td>Travel restrictions, closures, emergency policy, sanctions, tariffs or inventory hoarding.</td></tr>
              <tr><td>5 · Macro-market shock</td><td>Credit, volatility, equities, commodities and crypto reprice together.</td><td>Liquidity withdrawal, forced deleveraging and discontinuous price gaps.</td></tr>
            </tbody>
          </table>
        </div>
        <h3>Candidate transmission paths</h3>
        <ul>
          <li><strong>Public health:</strong> transmission → behavioral restrictions → growth and liquidity shock.</li>
          <li><strong>Geopolitics and shipping:</strong> chokepoint disruption → freight, oil and fertilizer → inflation and rates.</li>
          <li><strong>Trade and policy:</strong> enacted tariffs, sanctions or capital controls → dollar, yields, earnings and risk appetite.</li>
          <li><strong>Financial plumbing:</strong> stablecoin, exchange, ETF or funding stress → market depth loss → forced deleveraging.</li>
        </ul>
        <p class="emily-updated">Rule: the wildcard state never changes because a story sounds frightening. It changes only when independent evidence crosses a defined gate. A low observed state is not the same as low jump risk.</p>
        </div>
      </details>

      </div>
    </section>

    <section class="emily-section" id="emily-rules" aria-labelledby="emily-rules-title">
      <div class="chart-section-head emily-section-head">
        <div><span>03 · DECISION RULES</span><h2 id="emily-rules-title">What changes Emily's position</h2></div>
        <p>Precommitted evidence gates keep the call from moving with the mood.</p>
      </div>
      <div class="emily-grid emily-grid--rules">

      <article class="emily-panel">
        <div class="feed-kicker">Escalation test</div>
        <h2>Would raise the meter</h2>
        <ul>
          <li>BTC price damage and open-interest liquidation occurring together.</li>
          <li>VIX, high-yield spreads and equity losses rising in the same window.</li>
          <li>Stablecoin contraction, depegs or exchange withdrawal stress.</li>
          <li>Higher funding and open interest without matching spot participation.</li>
          <li>Oil, yields and the dollar tightening financial conditions together.</li>
          <li>A Nasdaq near its highs while long yields rise, followed by weakening leadership, volatility or credit confirmation.</li>
        </ul>
      </article>

      <article class="emily-panel">
        <div class="feed-kicker">De-escalation test</div>
        <h2>Would lower the meter</h2>
        <ul>
          <li>Price advances supported by broad participation rather than leverage alone.</li>
          <li>Stable or expanding stablecoin liquidity.</li>
          <li>Calm equity volatility and tight credit spreads.</li>
          <li>Open interest resetting without price damage.</li>
          <li>Lower yields and energy prices without a growth shock.</li>
          <li>Broader equity participation or falling yields that resolves the equity–rates divergence.</li>
        </ul>
      </article>

      </div>
    </section>

    <section class="emily-section" id="emily-method" aria-labelledby="emily-method-title">
      <div class="chart-section-head emily-section-head">
        <div><span>04 · TRANSPARENCY</span><h2 id="emily-method-title">Method, limits and sources</h2></div>
        <p>The full calculation boundaries and research trail remain available.</p>
      </div>
      <div class="emily-grid emily-grid--disclosures">
      <details class="emily-panel emily-panel--wide emily-disclosure">
        <summary>
          <span><small>Method and limits</small><strong>Free data, fail-closed publishing</strong></span>
          <span class="emily-disclosure-status">View method</span>
        </summary>
        <div class="emily-disclosure-body">
        <p>Emily separates market vulnerability from active panic. Required BTC and breadth data must be fresh. Optional feeds that fail are disclosed and removed from the calculation; they never become artificial green signals. If too little evidence remains, the daily job fails and yesterday's page stays in place.</p>
        <p>ETF flows, options positioning, order-book depth, shipping, public-health developments and breaking geopolitical news still require an event-driven research review. Corporate treasury holdings are displayed as secondary structural context and do not alter Active Panic by themselves. X posts are not used in the automatic score because reliable automated access is not free.</p>
        <p>The Wildcard Early Warning module is deliberately separate from the Panic Meter. Unverified external-event claims cannot raise the automated market score; verified consequences can trigger a full reassessment.</p>
        </div>
      </details>

      <details class="emily-panel emily-panel--wide emily-disclosure">
        <summary>
          <span><small>Research trail</small><strong>Sources behind today's automated desk</strong></span>
          <span class="emily-disclosure-status">${esc(data.quality)} · View sources</span>
        </summary>
        <div class="emily-disclosure-body">
      <p class="emily-sources">${sourceLinks}</p>
      ${gaps}
      <p class="emily-sources"><strong>Model note:</strong> This is an evidence meter, not a statistically calibrated crash probability and not personalized financial advice.</p>
        </div>
      </details>
      </div>
    </section>`;

  renderDailyChange();
})();
