(function () {
  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function fmt(date) {
    const d = new Date(date + "T12:00:00");
    return d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
  }

  function tags(row) {
    const bits = []
      .concat(row.investors || [])
      .concat(row.companies || []);
    if (!bits.length) return "";
    return `<ul class="case-tags">${bits.map((t) => `<li>${esc(t)}</li>`).join("")}</ul>`;
  }

  function themes(row) {
    if (!row.themes || !row.themes.length) return "";
    return `<p class="case-themes">${row.themes.map((t) => esc(t)).join(" · ")}</p>`;
  }

  function cardHTML(row, featured) {
    return `
      <a class="case-card${featured ? " case-card--feature" : ""}" href="/case?id=${encodeURIComponent(row.id)}">
        <div class="feed-kicker">${esc(row.kicker || "Case study")}</div>
        <h2>${esc(row.title)}</h2>
        <p>${esc(row.dek || "")}</p>
        ${themes(row)}
        <div class="feed-meta">${fmt(row.date)} · ${row.readingMinutes || "—"} min read</div>
      </a>`;
  }

  async function loadCatalog() {
    const res = await fetch("/cases/catalog.json");
    if (!res.ok) throw new Error("Could not load case catalog.");
    return res.json();
  }

  async function loadCase(id) {
    const res = await fetch("/cases/" + encodeURIComponent(id) + ".json");
    if (!res.ok) throw new Error("Could not load this case study.");
    return res.json();
  }

  function absUrl(path) {
    try {
      return new URL(path, location.origin).href;
    } catch (e) {
      return path;
    }
  }

  function setMeta(id, attr, value) {
    const el = document.getElementById(id);
    if (el && value) el.setAttribute(attr, value);
  }

  function timelineHTML(items) {
    if (!items || !items.length) return "";
    return `
      <ol class="case-timeline" aria-label="Decision timeline">
        ${items
          .map(
            (row) => `
          <li>
            <span class="tl-when">${esc(row.when)}</span>
            <span class="tl-what">${esc(row.what)}</span>
            ${row.source ? `<span class="tl-src">${esc(row.source)}</span>` : ""}
          </li>`
          )
          .join("")}
      </ol>`;
  }

  function figuresHTML(table) {
    if (!table || !table.rows || !table.rows.length) return "";
    const head = (table.columns || []).map((c) => `<th>${esc(c)}</th>`).join("");
    const body = table.rows
      .map(
        (row) =>
          `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`
      )
      .join("");
    return `
      <figure class="case-figure">
        <figcaption>${esc(table.caption || "Key figures")}</figcaption>
        <div class="case-table-wrap" tabindex="0">
          <table>
            <thead><tr>${head}</tr></thead>
            <tbody>${body}</tbody>
          </table>
        </div>
        <p class="case-figure-note">${esc(table.note || "")}</p>
      </figure>`;
  }

  function tocHTML(toc) {
    if (!toc || !toc.length) return "";
    return `
      <nav class="case-toc" aria-label="On this page">
        <h2>On this page</h2>
        <ol>
          ${toc.map((row) => `<li><a href="#${esc(row.id)}">${esc(row.title)}</a></li>`).join("")}
        </ol>
      </nav>`;
  }

  function sourcesHTML(sources) {
    if (!sources || !sources.length) return "";
    return `
      <ol class="case-sources">
        ${sources
          .map((s) => {
            const label = esc(s.title);
            const meta = [s.kind, s.date].filter(Boolean).map(esc).join(" · ");
            const link = s.url
              ? `<a href="${esc(s.url)}" rel="noopener noreferrer">${label}</a>`
              : label;
            return `<li>${link}${meta ? ` <span class="src-meta">${meta}</span>` : ""}${
              s.note ? ` — ${esc(s.note)}` : ""
            }</li>`;
          })
          .join("")}
      </ol>`;
  }

  async function renderIndex() {
    const feature = document.getElementById("case-feature");
    const list = document.getElementById("case-list");
    if (!feature && !list) return;
    try {
      const catalog = await loadCatalog();
      window.CASE_STUDIES = catalog;
      if (!catalog.length) {
        if (list) list.innerHTML = `<p class="note">No case studies yet.</p>`;
        return;
      }
      if (feature) feature.innerHTML = cardHTML(catalog[0], true);
      if (list) {
        if (catalog.length === 1) {
          list.innerHTML =
            `<p class="case-library-note">One completed case is live. The next one will show up in this list when it is finished. Unpublished names and dates stay off this page.</p>`;
        } else {
          list.innerHTML = catalog.slice(1).map((row) => cardHTML(row, false)).join("");
        }
      }
    } catch (err) {
      if (list) list.innerHTML = `<p class="note">${esc(err.message)}</p>`;
    }
  }

  async function renderCase() {
    const root = document.getElementById("case-root");
    if (!root) return;
    const params = new URLSearchParams(location.search);
    const id = params.get("id") || "";
    try {
      const catalog = await loadCatalog();
      window.CASE_STUDIES = catalog;
      const row = catalog.find((r) => r.id === id) || catalog[0];
      if (!row) throw new Error("No case studies in the catalog.");
      const pack = await loadCase(row.id);
      const title = pack.title || row.title;
      document.title = title + " · The Paramaribo Letter";
      setMeta("og-title", "content", title + " · The Paramaribo Letter");
      setMeta("og-desc", "content", pack.dek || row.dek || title);
      setMeta("og-url", "content", absUrl("/case?id=" + encodeURIComponent(row.id)));

      root.innerHTML = `
        <div class="kicker">${esc(pack.kicker || "Investor Case Studies")}</div>
        <h1 id="title">${esc(title)}</h1>
        <p class="lede">${esc(pack.subtitle || pack.dek || "")}</p>
        <div class="meta">${fmt(pack.date || row.date)} · ${pack.readingMinutes || row.readingMinutes || "—"} min read · The Paramaribo Letter</div>
        ${tags(pack)}
        ${themes(pack)}
        ${tocHTML(pack.toc)}
        ${pack.summaryHtml ? `<section class="case-summary" id="summary">${pack.summaryHtml}</section>` : ""}
        ${timelineHTML(pack.timeline)}
        ${figuresHTML(pack.figures)}
        <div class="body">${pack.bodyHtml || ""}</div>
        <section id="sources">
          <h2>Sources and further reading</h2>
          ${sourcesHTML(pack.sources)}
        </section>
        <p class="disclaimer">${esc(
          pack.disclaimer ||
            "This case study is provided for educational and historical purposes only. It is not investment advice, and historical results do not guarantee future outcomes."
        )}</p>`;
    } catch (err) {
      root.innerHTML = `<p class="note">${esc(err.message || "Could not load case study.")}</p>`;
    }
  }

  window.CaseStudies = { renderIndex, renderCase };
})();
