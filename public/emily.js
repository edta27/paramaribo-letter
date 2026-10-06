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

  const c = data.crypto || {};
  const s = data.scores || {};
  const fgi = data.sentiment || {};
  const d = data.derivatives || {};
  const st = data.stablecoins || {};
  const m = data.macro || {};
  const consumer = data.consumer || {};
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

  root.innerHTML = `
    <section class="emily-hero">
      <div class="thesis-eyebrow">Emily · Daily automated market intelligence</div>
      <h1>${esc(data.headline)}</h1>
      <p class="lede">${esc(data.summary)}</p>
      <p class="emily-updated">Updated <time datetime="${esc(data.updated_at)}">${esc(when(data.updated_at))}</time> · ${esc(data.quality)} · Decision: <span class="emily-call">${esc(data.decision)}</span></p>
    </section>

    <section class="emily-status-grid" aria-label="Emily's market meters">
      ${metric("BTC / Alt rotation", s.rotation, s.rotation_regime, "green", `Rotation score ${s.rotation} out of 100`)}
      ${metric("Panic vulnerability", s.vulnerability, `${s.vulnerability_band}. Can a future shock travel quickly?`, s.vulnerability_slug, `Panic vulnerability ${s.vulnerability} out of 100`)}
      ${metric("Active panic", s.active, `${s.active_band}. Is synchronized panic visible now?`, s.active_slug, `Active panic ${s.active} out of 100`)}
    </section>

    <div class="note">The vulnerability meter is not a crash probability. It measures the structure available to transmit a future surprise. The active-panic meter requires current evidence of price damage, volatility, credit stress, deleveraging and liquidity contraction.</div>

    <section class="emily-grid">
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
          <li>OKX BTC funding: ${signed(d.funding_8h_pct, "%", 4)} per eight hours.</li>
          <li>OKX BTC aggregate open interest: ${usd(d.oi_usd)} · seven-day change ${signed(d.oi_change_7d_pct)}.</li>
          <li>USD stablecoin supply: ${usd(st.supply_usd)} · seven-day change ${signed(st.change_7d_pct)}.</li>
        </ul>
        <p><strong>Read:</strong> these figures test crowding and absorption; unavailable values remain unknown.</p>
      </article>

      <article class="emily-panel emily-panel--wide">
        <div class="feed-kicker">Consumer exhaustion</div>
        <h2>Are households spending beyond their income support?</h2>
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
      </article>

      <article class="emily-panel emily-panel--wide">
        <div class="feed-kicker">Surrounding markets</div>
        <h2>Is stress synchronizing?</h2>
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
      </article>

      <article class="emily-panel">
        <div class="feed-kicker">Escalation test</div>
        <h2>Would raise the meter</h2>
        <ul>
          <li>BTC price damage and open-interest liquidation occurring together.</li>
          <li>VIX, high-yield spreads and equity losses rising in the same window.</li>
          <li>Stablecoin contraction, depegs or exchange withdrawal stress.</li>
          <li>Higher funding and open interest without matching spot participation.</li>
          <li>Oil, yields and the dollar tightening financial conditions together.</li>
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
        </ul>
      </article>

      <article class="emily-panel emily-panel--wide">
        <div class="feed-kicker">Method and limits</div>
        <h2>Free data, fail-closed publishing</h2>
        <p>Emily separates market vulnerability from active panic. Required BTC and breadth data must be fresh. Optional feeds that fail are disclosed and removed from the calculation; they never become artificial green signals. If too little evidence remains, the daily job fails and yesterday's page stays in place.</p>
        <p>ETF flows, full consolidated derivatives, order-book depth, shipping and breaking geopolitical news still require an event-driven research review. X posts are not used in the automatic score because reliable automated access is not free.</p>
      </article>
    </section>

    <section class="emily-panel">
      <div class="feed-kicker">Research trail</div>
      <h2>Sources behind today's automated desk</h2>
      <p class="emily-sources">${sourceLinks}</p>
      ${gaps}
      <p class="emily-sources"><strong>Model note:</strong> This is an evidence meter, not a statistically calibrated crash probability and not personalized financial advice.</p>
    </section>`;
})();
