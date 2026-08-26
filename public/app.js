const ISSUES = window.LETTER_ISSUES || [];

function byId(id) {
  return ISSUES.find((row) => row.id === id);
}

function fmt(date) {
  const d = new Date(date + "T12:00:00");
  return d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
}

function renderIndex() {
  if (!ISSUES.length) return;
  const featured = ISSUES[0];
  const rest = ISSUES.slice(1);
  const hero = document.getElementById("hero");
  if (hero) {
    hero.innerHTML = `
      <a href="issue.html?id=${encodeURIComponent(featured.id)}"><img src="${featured.cover}" alt=""></a>
      <div>
        <div class="kicker">${featured.kicker}</div>
        <h1 class="issue-title">${featured.title}</h1>
        <p class="lede">${featured.dek}</p>
        <div class="meta">${fmt(featured.date)} · ${featured.byline}</div>
        <a class="btn" href="issue.html?id=${encodeURIComponent(featured.id)}">Read the letter</a>
      </div>`;
  }
  const grid = document.getElementById("archive");
  if (grid) {
    grid.innerHTML = rest.map((row) => `
      <a class="card" href="issue.html?id=${encodeURIComponent(row.id)}">
        <img src="${row.cover}" alt="">
        <div class="kicker">${row.kicker}</div>
        <h2>${row.title}</h2>
        <p>${row.dek}</p>
        <div class="meta" style="margin-top:10px">${fmt(row.date)}</div>
      </a>`).join("");
  }
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
}

window.Letter = { renderIndex, renderIssue, ISSUES };
