(function () {
  if (document.getElementById("portal-side")) return;

  function fontLink() {
    if (document.getElementById("portal-fonts")) return;
    const l = document.createElement("link");
    l.id = "portal-fonts";
    l.rel = "stylesheet";
    l.href =
      "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;600;700&display=swap";
    document.head.appendChild(l);
  }

  const active = document.body.getAttribute("data-nav") || "";
  const item = (href, id, label) =>
    `<a class="side-link${active === id ? " is-active" : ""}" href="${href}">${label}</a>`;

  const side = document.createElement("aside");
  side.className = "portal-side";
  side.id = "portal-side";
  side.innerHTML = `
    <a class="side-brand" href="/">
      <img src="/favicon.svg" alt="" width="28" height="28" />
      <span>The Paramaribo Letter</span>
    </a>
    <nav class="side-nav" aria-label="Primary">
      ${item("/", "home", "Home")}
      ${item("/#feed", "feed", "Research")}
      ${item("/topics", "topics", "Topics")}
      ${item("/charts", "charts", "Charts")}
      ${item("/cases", "cases", "Case studies")}
      ${item("/agents", "agents", "Agents")}
      ${item("/desk/", "desk", "Desk")}
    </nav>
    <div class="side-block">
      <div class="side-label">Account</div>
      ${item("/#new-subscribers", "subscribe", "Subscribe")}
      ${item("/unsubscribe", "unsubscribe", "Unsubscribe")}
    </div>
    <p class="side-foot">Educational research. Not advice.</p>
  `;

  const svg = (d) =>
    `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const ICONS = {
    menu: svg('<path d="M4 6h16M4 12h16M4 18h16"/>'),
    search: svg('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>'),
    sun: svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>').replace("<svg", '<svg class="i-sun"'),
    moon: svg('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>').replace("<svg", '<svg class="i-moon"'),
  };

  const top = document.createElement("header");
  top.className = "portal-top";
  top.innerHTML = `
    <button type="button" class="icon-btn side-toggle" aria-label="Open menu" aria-controls="portal-side" aria-expanded="false">${ICONS.menu}</button>
    <button type="button" class="search-trigger" data-open-search>
      ${ICONS.search}
      <span>Search <span class="search-long">research</span></span>
      <kbd>⌘K</kbd>
    </button>
    <div class="top-actions">
      <button type="button" class="icon-btn theme-btn" data-theme-toggle aria-label="Switch light or dark theme">${ICONS.sun}${ICONS.moon}</button>
      <a class="btn btn-primary" href="${document.getElementById("new-subscribers") ? "#new-subscribers" : "/#new-subscribers"}">Subscribe</a>
    </div>
  `;

  const modal = document.createElement("div");
  modal.className = "search-modal";
  modal.id = "search-modal";
  modal.hidden = true;
  modal.innerHTML = `
    <div class="search-backdrop" data-close-search></div>
    <div class="search-panel" role="dialog" aria-modal="true" aria-label="Search issues">
      <input class="search-input" type="search" placeholder="Search issues…" autocomplete="off" />
      <div class="search-results" id="search-results"></div>
    </div>
  `;

  const scrim = document.createElement("div");
  scrim.className = "side-scrim";
  scrim.hidden = true;

  const stage = document.querySelector(".portal-stage");
  const skip = document.createElement("a");
  skip.className = "skip-link";
  skip.textContent = "Skip to content";
  if (stage) {
    if (!stage.id) stage.id = "main";
    if (!document.querySelector("main, [role=main]")) stage.setAttribute("role", "main");
    skip.href = "#" + stage.id;
  }

  fontLink();
  document.body.classList.add("is-portal");
  document.body.prepend(...(stage ? [skip] : []), scrim, side, top);
  document.body.appendChild(modal);

  function setTheme(next) {
    document.documentElement.dataset.theme = next;
    try {
      localStorage.setItem("paramaribo-theme", next);
    } catch (e) {}
  }
  try {
    const saved = localStorage.getItem("paramaribo-theme");
    if (saved === "light" || saved === "dark") setTheme(saved);
  } catch (e) {}

  top.querySelector("[data-theme-toggle]").addEventListener("click", () => {
    const cur = document.documentElement.dataset.theme === "light" ? "light" : "dark";
    setTheme(cur === "light" ? "dark" : "light");
  });

  const toggle = top.querySelector(".side-toggle");
  function closeSide() {
    document.body.classList.remove("side-open");
    scrim.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
  }
  toggle.addEventListener("click", () => {
    const open = document.body.classList.toggle("side-open");
    scrim.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  });
  scrim.addEventListener("click", closeSide);

  let caseRows = window.CASE_STUDIES || [];
  fetch("/cases/catalog.json")
    .then((res) => (res.ok ? res.json() : []))
    .then((rows) => {
      if (Array.isArray(rows)) {
        caseRows = rows;
        window.CASE_STUDIES = rows;
      }
    })
    .catch(() => {});

  function issues() {
    return window.LETTER_ISSUES || [];
  }
  function fmt(date) {
    const d = new Date(date + "T12:00:00");
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
  }
  const results = modal.querySelector("#search-results");
  const input = modal.querySelector(".search-input");
  function renderSearch(q) {
    const needle = (q || "").trim().toLowerCase();
    const rows = issues().filter((row) => {
      if (!needle) return true;
      return [row.title, row.dek, row.kicker, row.id].join(" ").toLowerCase().includes(needle);
    });
    const caseHits = caseRows.filter((row) => {
      if (!needle) return true;
      return [row.title, row.dek, row.kicker, row.id, ...(row.investors || []), ...(row.companies || [])]
        .join(" ")
        .toLowerCase()
        .includes(needle);
    });
    const issueHits = rows.slice(0, 8).map(
      (row) => `
      <a class="search-hit" href="/issue?id=${encodeURIComponent(row.id)}">
        <strong>${row.title}</strong>
        <span>${row.kicker || ""} · ${fmt(row.date)}</span>
      </a>`
    );
    const studyHits = caseHits.slice(0, 4).map(
      (row) => `
      <a class="search-hit" href="/case?id=${encodeURIComponent(row.id)}">
        <strong>${row.title}</strong>
        <span>Case study · ${row.kicker || ""} · ${fmt(row.date)}</span>
      </a>`
    );
    results.innerHTML =
      studyHits.join("") + issueHits.join("") || `<p class="search-empty">No issues or case studies match.</p>`;
  }
  function openSearch() {
    modal.hidden = false;
    renderSearch("");
    input.value = "";
    input.focus();
  }
  function closeSearch() {
    modal.hidden = true;
  }
  top.querySelector("[data-open-search]").addEventListener("click", openSearch);
  modal.querySelector("[data-close-search]").addEventListener("click", closeSearch);
  input.addEventListener("input", () => renderSearch(input.value));
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      if (modal.hidden) openSearch();
      else closeSearch();
    }
    if (event.key === "Escape") {
      closeSearch();
      closeSide();
    }
  });
})();
