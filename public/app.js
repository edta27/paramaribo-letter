const ISSUES = window.LETTER_ISSUES || [];

function byId(id) {
  return ISSUES.find((row) => row.id === id);
}

function fmt(date) {
  const d = new Date(date + "T12:00:00");
  return d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
}

function cardHTML(row, featured) {
  return `
    <a class="feed-card${featured ? " feed-card--feature" : ""}" href="/issue?id=${encodeURIComponent(row.id)}">
      <img src="${row.cover}" alt="">
      <div>
        <div class="feed-kicker">${row.kicker || ""}</div>
        <h2>${row.title}</h2>
        <p>${row.dek || ""}</p>
        <div class="feed-meta">${fmt(row.date)} · ${row.byline || "The Paramaribo Letter"}</div>
      </div>
    </a>`;
}

function renderIndex() {
  if (!ISSUES.length) return;
  const feed = document.getElementById("feed") || document.getElementById("archive");
  if (feed) {
    feed.innerHTML = ISSUES.map((row, i) => cardHTML(row, i === 0)).join("");
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
