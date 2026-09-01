(function () {
  const charts = [];

  function fmtDay(ts) {
    const d = new Date(ts);
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  }

  function destroyAll() {
    while (charts.length) {
      const c = charts.pop();
      try {
        c.destroy();
      } catch (e) {}
    }
  }

  function theme() {
    const s = getComputedStyle(document.documentElement);
    return {
      text: s.getPropertyValue("--text").trim() || "#e9ebed",
      mute: s.getPropertyValue("--mute").trim() || "#9aa4b2",
      stroke: s.getPropertyValue("--stroke").trim() || "#2a2e32",
    };
  }

  function renderDual(canvas, spec) {
    const t = theme();
    const bars = spec.bars || {};
    const line = spec.line || {};
    const barData = bars.data || [];
    const lineData = line.data || [];
    const labels = barData.map((row) => fmtDay(row[0]));
    const barVals = barData.map((row) => row[1]);
    const lineVals = lineData.map((row) => row[1]);
    const unsigned = !!bars.unsigned;
    const barFill = unsigned
      ? "rgba(46, 144, 250, 0.55)"
      : barVals.map((v) => (v >= 0 ? "rgba(50, 213, 131, 0.75)" : "rgba(249, 112, 102, 0.75)"));

    const chart = new Chart(canvas.getContext("2d"), {
      data: {
        labels,
        datasets: [
          {
            type: "bar",
            label: bars.label || "Series",
            data: barVals,
            backgroundColor: barFill,
            borderWidth: 0,
            yAxisID: "y",
            order: 2,
          },
          {
            type: "line",
            label: line.label || "Price",
            data: lineVals,
            borderColor: t.text,
            backgroundColor: "transparent",
            borderWidth: 1.5,
            pointRadius: 0,
            tension: 0.15,
            yAxisID: "y1",
            order: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: {
            labels: { color: t.mute, boxWidth: 12, font: { size: 11 } },
          },
          title: {
            display: true,
            text: spec.title || "",
            color: t.text,
            font: { size: 13, weight: "600" },
            padding: { bottom: 10 },
          },
        },
        scales: {
          x: {
            ticks: { color: t.mute, maxTicksLimit: 8, font: { size: 10 } },
            grid: { color: t.stroke + "99" },
          },
          y: {
            position: "left",
            ticks: { color: t.mute, font: { size: 10 } },
            grid: { color: t.stroke + "99" },
          },
          y1: {
            position: "right",
            ticks: { color: t.mute, font: { size: 10 } },
            grid: { drawOnChartArea: false },
          },
        },
      },
    });
    charts.push(chart);
  }

  function briefHtml(brief) {
    const chartBlocks = (brief.charts || [])
      .map((spec, i) => {
        const id = `chart-${brief.id}-${i}`;
        return `<div class="chart-panel"><canvas id="${id}" height="280"></canvas></div>`;
      })
      .join("");
    return `
      <article class="chart-brief" data-brief="${brief.id}">
        <div class="chart-brief-kicker">${brief.asset || "Desk"}</div>
        <h2>${brief.headline || ""}</h2>
        <p class="chart-brief-lede">${brief.lede || ""}</p>
        <div class="chart-brief-body">${brief.bodyHtml || ""}</div>
        <div class="chart-stack">${chartBlocks}</div>
      </article>`;
  }

  function levelsHtml(levels) {
    if (!levels || !levels.length) return "";
    return `<ul class="thesis-levels">${levels.map((l) => `<li>${l}</li>`).join("")}</ul>`;
  }

  function renderMeta(pack) {
    const meta = document.getElementById("chart-meta");
    const hook = document.getElementById("subscribe-hook-copy");
    if (hook && pack.subscribeHook) hook.textContent = pack.subscribeHook;
    if (!meta) return;

    const thesis = pack.thesis || pack.title || "Weekly chart desk";
    const stakes = pack.stakes || pack.dek || "";
    const letterUrl = pack.letterUrl || "/";
    const letterLabel = pack.letterLabel || "Read the letter";

    meta.innerHTML = `
      <div class="thesis-card">
        <div class="thesis-eyebrow">Current call · Desk</div>
        <h1 class="thesis-title">${thesis}</h1>
        <p class="thesis-stakes">${stakes}</p>
        ${levelsHtml(pack.levels)}
        <div class="thesis-actions">
          <a class="btn btn-primary" href="${letterUrl}">${letterLabel}</a>
          <a class="btn" href="#tape">See the tape ↓</a>
        </div>
        <p class="meta">As-of ${pack.asOf || pack.date} · ${pack.cadence || "weekly"} · pack <code>${pack.id}</code></p>
      </div>
      <details class="source-details">
        <summary>Sources &amp; method</summary>
        <p>${pack.sourceNote || pack.dek || ""}</p>
      </details>`;
  }

  function paintPack(pack) {
    const root = document.getElementById("chart-desk");
    renderMeta(pack);
    root.innerHTML = (pack.briefs || []).map(briefHtml).join("");
    (pack.briefs || []).forEach((brief) => {
      (brief.charts || []).forEach((spec, i) => {
        const canvas = document.getElementById(`chart-${brief.id}-${i}`);
        if (canvas) renderDual(canvas, spec);
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

  async function render() {
    const root = document.getElementById("chart-desk");
    if (!root) return;
    destroyAll();
    root.innerHTML = `<p class="chart-loading">Loading weekly charts…</p>`;
    try {
      const catalog = await loadCatalog();
      if (!catalog.length) {
        root.innerHTML = `<p class="note">No chart packs yet. Run <code>python3 scripts/build_weekly_charts.py</code>.</p>`;
        return;
      }
      const pack = await loadPack(catalog[0].id);
      paintPack(pack);

      const archive = document.getElementById("chart-archive");
      if (archive) {
        archive.innerHTML = catalog
          .map(
            (row) => `
          <button type="button" class="chart-archive-item${row.id === pack.id ? " is-active" : ""}" data-pack="${row.id}">
            <strong>${row.thesis || row.title}</strong>
            <span>${row.date} · ${row.kicker || "Weekly"}</span>
          </button>`
          )
          .join("");
        archive.querySelectorAll("[data-pack]").forEach((btn) => {
          btn.addEventListener("click", async () => {
            const id = btn.getAttribute("data-pack");
            destroyAll();
            root.innerHTML = `<p class="chart-loading">Loading…</p>`;
            try {
              const next = await loadPack(id);
              paintPack(next);
              archive.querySelectorAll(".chart-archive-item").forEach((el) => {
                el.classList.toggle("is-active", el.getAttribute("data-pack") === id);
              });
              window.scrollTo({ top: 0, behavior: "smooth" });
            } catch (err) {
              root.innerHTML = `<p class="note">${err.message || "Load failed."}</p>`;
            }
          });
        });
      }
    } catch (err) {
      root.innerHTML = `<p class="note">${err.message || "Could not load charts."}</p>`;
    }
  }

  window.ChartDesk = { render };
})();
