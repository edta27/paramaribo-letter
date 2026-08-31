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

  const top = document.createElement("header");
  top.className = "portal-top";
  top.innerHTML = `
    <button type="button" class="icon-btn side-toggle" aria-label="Open menu">☰</button>
    <button type="button" class="search-trigger" data-open-search>
      <span>Search research</span>
      <kbd>⌘K</kbd>
    </button>
    <div class="top-actions">
      <button type="button" class="icon-btn" data-theme-toggle aria-label="Toggle theme">Theme</button>
      <a class="btn btn-primary" href="/#new-subscribers">Subscribe</a>
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

  fontLink();
  document.body.classList.add("is-portal");
  document.body.prepend(scrim, side, top);
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
  }
  toggle.addEventListener("click", () => {
    document.body.classList.toggle("side-open");
    scrim.hidden = !document.body.classList.contains("side-open");
  });
  scrim.addEventListener("click", closeSide);

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
    results.innerHTML = rows.slice(0, 12).map((row) => `
      <a class="search-hit" href="/issue?id=${encodeURIComponent(row.id)}">
        <strong>${row.title}</strong>
        <span>${row.kicker || ""} · ${fmt(row.date)}</span>
      </a>`).join("") || `<p class="search-empty">No issues match.</p>`;
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
