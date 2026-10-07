(function () {
  "use strict";

  const charts = [];
  let activePack = null;
  let themeObserver = null;

  const esc = (value) => String(value == null ? "" : value)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#039;");

  function fmtDay(ts) {
    const d = new Date(Number(ts));
    const day = d.toLocaleDateString("en-US", { timeZone: "UTC", month: "short", day: "numeric", year: "numeric" });
    if (d.getUTCHours() === 0 && d.getUTCMinutes() === 0) return day;
    const time = d.toLocaleTimeString("en-US", { timeZone: "UTC", hour: "numeric", minute: "2-digit" });
    return `${day}, ${time} UTC`;
  }

  function asTime(ts) {
    return Math.floor(Number(ts) / 1000);
  }

  function compact(value) {
    if (value == null || value === "") return "—";
    const number = Number(value);
    if (!Number.isFinite(number)) return "—";
    const abs = Math.abs(number);
    if (abs >= 1e9) return `${(number / 1e9).toFixed(2)}B`;
    if (abs >= 1e6) return `${(number / 1e6).toFixed(2)}M`;
    if (abs >= 1e3) return `${(number / 1e3).toFixed(2)}K`;
    return number.toLocaleString(undefined, { maximumFractionDigits: 2 });
  }

  function destroyAll() {
    while (charts.length) {
      const item = charts.pop();
      try {
        item.chart.remove();
      } catch (e) {}
    }
  }

  function theme() {
    const s = getComputedStyle(document.documentElement);
    return {
      page: s.getPropertyValue("--sunken").trim() || "#11161c",
      text: s.getPropertyValue("--text").trim() || "#e9ebed",
      mute: s.getPropertyValue("--mute").trim() || "#9aa4b2",
      stroke: s.getPropertyValue("--stroke").trim() || "#2a2e32",
      grid: s.getPropertyValue("--stroke-subtle").trim() || "#20262d",
      accent: s.getPropertyValue("--accent").trim() || "#2e90fa",
    };
  }

  function chartOptions(t) {
    return {
      autoSize: true,
      layout: {
        background: { type: LightweightCharts.ColorType.Solid, color: t.page },
        textColor: t.mute,
        attributionLogo: true,
        panes: {
          separatorColor: t.stroke,
          separatorHoverColor: t.accent,
          enableResize: true,
        },
      },
      grid: {
        vertLines: { color: t.grid },
        horzLines: { color: t.grid },
      },
      crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
        vertLine: { color: t.mute, width: 1, style: LightweightCharts.LineStyle.Dashed, labelBackgroundColor: t.stroke },
        horzLine: { color: t.mute, width: 1, style: LightweightCharts.LineStyle.Dashed, labelBackgroundColor: t.stroke },
      },
      rightPriceScale: { borderColor: t.stroke },
      timeScale: {
        borderColor: t.stroke,
        timeVisible: true,
        secondsVisible: false,
        rightOffset: 1,
      },
      handleScale: { axisPressedMouseMove: true, mouseWheel: true, pinch: true },
      handleScroll: { mouseWheel: true, pressedMouseMove: true, horzTouchDrag: true, vertTouchDrag: false },
      localization: { locale: "en-US" },
    };
  }

  function tableHtml(spec) {
    const bars = (spec.bars && spec.bars.data) || [];
    const line = (spec.line && spec.line.data) || [];
    const rows = new Map();
    bars.forEach((row) => rows.set(Number(row[0]), { bar: row[1], line: null }));
    line.forEach((row) => {
      const current = rows.get(Number(row[0])) || { bar: null, line: null };
      current.line = row[1];
      rows.set(Number(row[0]), current);
    });
    const body = Array.from(rows.entries())
      .sort((a, b) => a[0] - b[0])
      .map(([ts, row]) => `<tr><td>${esc(fmtDay(ts))}</td><td>${esc(compact(row.line))}</td><td>${esc(compact(row.bar))}</td></tr>`)
      .join("");
    return `
      <details class="chart-data-table">
        <summary>View chart data</summary>
        <div class="chart-data-scroll">
          <table>
            <thead><tr><th>Date</th><th>${esc((spec.line || {}).label || "Price")}</th><th>${esc((spec.bars || {}).label || "Series")}</th></tr></thead>
            <tbody>${body}</tbody>
          </table>
        </div>
      </details>`;
  }

  function renderInteractive(container, legend, spec) {
    if (!window.LightweightCharts) {
      container.innerHTML = '<p class="note">Interactive chart renderer could not load. The complete data table remains available below.</p>';
      return;
    }

    const t = theme();
    const bars = spec.bars || {};
    const line = spec.line || {};
    const chart = LightweightCharts.createChart(container, chartOptions(t));
    const lineSeries = chart.addSeries(LightweightCharts.LineSeries, {
      title: line.label || "Price",
      color: t.text,
      lineWidth: 2,
      crosshairMarkerVisible: true,
      crosshairMarkerRadius: 4,
      priceLineVisible: false,
      lastValueVisible: true,
    }, 0);
    const histogram = chart.addSeries(LightweightCharts.HistogramSeries, {
      title: bars.label || "Series",
      priceFormat: { type: "volume" },
      priceLineVisible: false,
      lastValueVisible: true,
    }, 1);

    const lineData = (line.data || [])
      .filter((row) => Number.isFinite(Number(row[0])) && Number.isFinite(Number(row[1])))
      .map((row) => ({ time: asTime(row[0]), value: Number(row[1]) }));
    const barData = (bars.data || [])
      .filter((row) => Number.isFinite(Number(row[0])))
      .map((row) => {
        const time = asTime(row[0]);
        const value = Number(row[1]);
        if (!Number.isFinite(value)) return { time };
        return {
          time,
          value,
          color: bars.unsigned || value >= 0 ? "rgba(50, 213, 131, 0.72)" : "rgba(249, 112, 102, 0.78)",
        };
      });

    lineSeries.setData(lineData);
    histogram.setData(barData);
    chart.timeScale().fitContent();

    requestAnimationFrame(() => {
      const panes = chart.panes();
      if (panes[0]) panes[0].setHeight(220);
      if (panes[1]) panes[1].setHeight(110);
    });

    const defaultLegend = `${esc(line.label || "Price")} · move across the chart for an exact reading`;
    legend.innerHTML = defaultLegend;
    chart.subscribeCrosshairMove((param) => {
      if (!param || !param.time) {
        legend.innerHTML = defaultLegend;
        return;
      }
      const pricePoint = param.seriesData.get(lineSeries);
      const barPoint = param.seriesData.get(histogram);
      const date = new Date(Number(param.time) * 1000);
      const dateText = date.toLocaleString("en-US", {
        timeZone: "UTC", month: "short", day: "numeric", year: "numeric",
        hour: "numeric", minute: "2-digit", timeZoneName: "short",
      });
      const price = pricePoint && Number.isFinite(pricePoint.value) ? compact(pricePoint.value) : "—";
      const bar = barPoint && Number.isFinite(barPoint.value) ? compact(barPoint.value) : "—";
      legend.innerHTML = `<strong>${esc(dateText)}</strong> · ${esc(line.label || "Price")}: ${esc(price)} · ${esc(bars.label || "Series")}: ${esc(bar)}`;
    });

    const fit = container.parentElement.querySelector("[data-chart-fit]");
    if (fit) fit.addEventListener("click", () => chart.timeScale().fitContent());
    charts.push({ chart, lineSeries, histogram });
  }

  function briefHtml(brief) {
    const chartBlocks = (brief.charts || [])
      .map((spec, i) => {
        const id = `chart-${brief.id}-${i}`;
        return `
          <section class="chart-panel" aria-labelledby="${id}-title">
            <div class="chart-panel-head">
              <div>
                <strong id="${id}-title">${esc(spec.title || "Interactive chart")}</strong>
                <span>Drag to pan · scroll or pinch to zoom · drag the pane divider to resize</span>
              </div>
              <button type="button" class="chart-fit" data-chart-fit>Fit data</button>
            </div>
            <div id="${id}" class="lwc-chart" role="img" aria-label="Interactive financial chart: ${esc(spec.title || "chart")}"></div>
            <p id="${id}-legend" class="chart-crosshair-readout" aria-live="polite"></p>
            ${tableHtml(spec)}
          </section>`;
      })
      .join("");
    return `
      <article class="chart-brief" data-brief="${esc(brief.id)}">
        <div class="chart-brief-kicker">${esc(brief.asset || "Desk")}</div>
        <h2>${esc(brief.headline || "")}</h2>
        <p class="chart-brief-lede">${esc(brief.lede || "")}</p>
        <div class="chart-brief-body">${brief.bodyHtml || ""}</div>
        <div class="chart-stack">${chartBlocks}</div>
      </article>`;
  }

  function levelsHtml(levels) {
    if (!levels || !levels.length) return "";
    return `<ul class="thesis-levels">${levels.map((level) => `<li>${esc(level)}</li>`).join("")}</ul>`;
  }

  function renderMeta(pack) {
    const meta = document.getElementById("chart-meta");
    const hook = document.getElementById("subscribe-hook-copy");
    if (hook && pack.subscribeHook) hook.textContent = pack.subscribeHook;
    if (!meta) return;

    const thesis = pack.thesis || pack.title || "Weekly chart desk";
    const stakes = pack.stakes || pack.dek || "";
    const latest = (window.LETTER_ISSUES || [])[0];
    const letterUrl = latest
      ? "/issue?id=" + encodeURIComponent(latest.id)
      : pack.letterUrl || "/";
    const letterLabel = latest
      ? latest.kicker || "Latest letter"
      : pack.letterLabel || "Read the letter";

    meta.innerHTML = `
      <div class="thesis-card">
        <div class="thesis-eyebrow">Current call · Desk</div>
        <h1 class="thesis-title">${esc(thesis)}</h1>
        <p class="thesis-stakes">${esc(stakes)}</p>
        ${levelsHtml(pack.levels)}
        <div class="thesis-actions">
          <a class="btn btn-primary" href="${esc(letterUrl)}">${esc(letterLabel)}</a>
          <a class="btn" href="#tape">See the tape ↓</a>
        </div>
        <p class="meta">As-of ${esc(pack.asOf || pack.date)} · ${esc(pack.cadence || "weekly")} · pack <code>${esc(pack.id)}</code></p>
      </div>
      <details class="source-details">
        <summary>Sources &amp; method</summary>
        <p>${esc(pack.sourceNote || pack.dek || "")}</p>
      </details>`;
  }

  function paintPack(pack) {
    const root = document.getElementById("chart-desk");
    activePack = pack;
    renderMeta(pack);
    root.innerHTML = (pack.briefs || []).map(briefHtml).join("");
    (pack.briefs || []).forEach((brief) => {
      (brief.charts || []).forEach((spec, i) => {
        const id = `chart-${brief.id}-${i}`;
        const container = document.getElementById(id);
        const legend = document.getElementById(`${id}-legend`);
        if (container && legend) renderInteractive(container, legend, spec);
      });
    });
  }

  async function loadPack(id) {
    const res = await fetch(`/charts/packs/${encodeURIComponent(id)}.json`);
    if (!res.ok) throw new Error("Could not load chart pack.");
    return res.json();
  }

  async function loadCatalog() {
    const res = await fetch("/charts/catalog.json");
    if (!res.ok) throw new Error("Could not load chart catalog.");
    return res.json();
  }

  function installThemeObserver() {
    if (themeObserver) return;
    themeObserver = new MutationObserver(() => {
      if (!activePack) return;
      destroyAll();
      paintPack(activePack);
    });
    themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  }

  async function render() {
    const root = document.getElementById("chart-desk");
    if (!root) return;
    installThemeObserver();
    destroyAll();
    root.innerHTML = '<p class="chart-loading">Loading interactive charts…</p>';
    try {
      const catalog = await loadCatalog();
      if (!catalog.length) {
        root.innerHTML = '<p class="note">No chart packs are available yet.</p>';
        return;
      }
      const pack = await loadPack(catalog[0].id);
      paintPack(pack);

      const archive = document.getElementById("chart-archive");
      if (archive) {
        archive.innerHTML = catalog
          .map((row) => `
            <button type="button" class="chart-archive-item${row.id === pack.id ? " is-active" : ""}" data-pack="${esc(row.id)}">
              <strong>${esc(row.thesis || row.title)}</strong>
              <span>${esc(row.date)} · ${esc(row.kicker || "Weekly")}</span>
            </button>`)
          .join("");
        archive.querySelectorAll("[data-pack]").forEach((btn) => {
          btn.addEventListener("click", async () => {
            const id = btn.getAttribute("data-pack");
            destroyAll();
            root.innerHTML = '<p class="chart-loading">Loading interactive charts…</p>';
            try {
              const next = await loadPack(id);
              paintPack(next);
              archive.querySelectorAll(".chart-archive-item").forEach((el) => {
                el.classList.toggle("is-active", el.getAttribute("data-pack") === id);
              });
              window.scrollTo({ top: 0, behavior: "smooth" });
            } catch (err) {
              root.innerHTML = `<p class="note">${esc(err.message || "Load failed.")}</p>`;
            }
          });
        });
      }
    } catch (err) {
      root.innerHTML = `<p class="note">${esc(err.message || "Could not load charts.")}</p>`;
    }
  }

  window.ChartDesk = { render };
})();
