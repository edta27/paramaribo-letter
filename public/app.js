const ISSUES = window.LETTER_ISSUES || [];

function byId(id) {
  return ISSUES.find((row) => row.id === id);
}

function fmt(date) {
  const d = new Date(date + "T12:00:00");
  return d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
}

function esc(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function cardHTML(row) {
  return `
    <a class="feed-card" href="/issue?id=${encodeURIComponent(row.id)}">
      <img src="${row.cover}" alt="">
      <div>
        <div class="feed-kicker">${row.kicker || ""}</div>
        <h2>${row.title}</h2>
        <p>${row.dek || ""}</p>
        <div class="feed-meta">${fmt(row.date)} · ${row.byline || "The Paramaribo Letter"}</div>
      </div>
    </a>`;
}

function levelsHtml(levels) {
  if (!levels || !levels.length) return "";
  return `<ul class="thesis-levels">${levels.map((l) => `<li>${esc(l)}</li>`).join("")}</ul>`;
}

async function renderHomeThesis() {
  const mount = document.getElementById("home-thesis");
  if (!mount) return;
  const latest = ISSUES[0];
  try {
    const res = await fetch("/charts/catalog.json");
    if (!res.ok) return;
    const catalog = await res.json();
    const pack = catalog[0];
    if (!pack || !pack.thesis) return;
    // Current call is the market map (from Chart Desk). Do not label it with an
    // issue number — that fought the featured letter when ISSUES[0] advanced.
    const stakes = pack.stakes || "";
    const letterUrl = latest
      ? "/issue?id=" + encodeURIComponent(latest.id)
      : pack.letterUrl || "/";
    const letterLabel = latest
      ? latest.kicker || "Latest letter"
      : pack.letterLabel || "Read the letter";
    mount.innerHTML = `
      <div class="thesis-card">
        <div class="thesis-eyebrow">Current call · Desk</div>
        <h1 class="thesis-title">${esc(pack.thesis)}</h1>
        <p class="thesis-stakes">${esc(stakes)}</p>
        ${levelsHtml(pack.levels)}
        <div class="thesis-actions">
          <a class="btn btn-primary" href="${esc(letterUrl)}">${esc(letterLabel)}</a>
          <a class="btn" href="/charts">See the tape</a>
        </div>
      </div>`;
  } catch (e) {}
}

function renderIndex() {
  renderHomeThesis();
  if (!ISSUES.length) return;
  const feed = document.getElementById("feed") || document.getElementById("archive");
  if (feed) {
    feed.innerHTML = ISSUES.map((row) => cardHTML(row)).join("");
  }
  const hero = document.getElementById("hero");
  if (hero) hero.innerHTML = "";
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

function renderIssue() {
  const params = new URLSearchParams(location.search);
  const row = byId(params.get("id") || "") || ISSUES[0];
  if (!row) return;
  document.title = row.title + " · The Paramaribo Letter";
  document.getElementById("kicker").textContent = row.kicker;
  document.getElementById("title").textContent = row.title;
  document.getElementById("dek").textContent = row.dek;
  document.getElementById("meta").textContent = `${fmt(row.date)} · ${row.byline}`;
  const cover = document.getElementById("cover");
  cover.src = row.cover;
  cover.alt = row.title;
  document.getElementById("body").innerHTML = row.body || "";
  setMeta("og-title", "content", row.title + " · The Paramaribo Letter");
  setMeta("og-desc", "content", row.dek || row.title);
  setMeta("og-image", "content", absUrl(row.cover));
  setMeta("og-url", "content", absUrl("/issue?id=" + encodeURIComponent(row.id)));
}

window.Letter = { renderIndex, renderIssue, ISSUES };
