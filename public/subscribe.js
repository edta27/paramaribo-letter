(function () {
  var SUBSCRIBED_KEY = "paramaribo-subscribed";
  var BAR_DISMISSED_KEY = "paramaribo-sub-bar-dismissed";
  var BAR_QUIET_DAYS = 14;

  // Queue Clarity calls made before /clarity.js (deferred) has loaded.
  window.clarity =
    window.clarity ||
    function () {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };

  function pagePath() {
    return window.location.pathname.replace(/\/index\.html$/, "/") || "/";
  }

  function store(key, value) {
    try {
      if (value === undefined) return window.localStorage.getItem(key);
      window.localStorage.setItem(key, value);
    } catch (e) {
      return null;
    }
    return value;
  }

  // Vercel records custom events only on paid plans, so every event also goes
  // to Microsoft Clarity (free) and GA4 when those are loaded. Signups are also
  // counted as page views of /subscribed, which the Hobby plan does record.
  function track(name, data) {
    data = data || {};
    if (typeof window.va === "function") window.va("event", { name: name, data: data });
    if (typeof window.clarity === "function") {
      window.clarity("event", name);
      if (data.form_location) window.clarity("set", "sub_location", String(data.form_location));
    }
    if (typeof window.gtag === "function") window.gtag("event", name, data);
  }

  function formLocation(form) {
    return form.dataset.subLocation || form.id || "subscribe";
  }

  function trackFormStart(form) {
    if (form.dataset.startTracked === "1") return;
    form.dataset.startTracked = "1";
    track("subscribe_form_start", { form_location: formLocation(form), page: pagePath() });
  }

  function watchViews(forms) {
    if (!("IntersectionObserver" in window)) return;
    var seen = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          seen.unobserve(entry.target);
          track("subscribe_view", { form_location: formLocation(entry.target), page: pagePath() });
        });
      },
      { threshold: 0.6 }
    );
    forms.forEach(function (form) {
      seen.observe(form);
    });
  }

  function thanksUrl(outcome, location) {
    var params = new URLSearchParams({ from: pagePath() + window.location.search, via: location });
    if (outcome === "already_subscribed") params.set("already", "1");
    return "/subscribed?" + params.toString();
  }

  function bind(form) {
    if (!form || form.dataset.bound === "1") return;
    form.dataset.bound = "1";
    var status = form.parentElement.querySelector("[data-sub-status]");
    var email = form.querySelector('input[name="email"]');
    var btn = form.querySelector('button[type="submit"]');

    form.addEventListener("focusin", function () { trackFormStart(form); });
    form.addEventListener("input", function () { trackFormStart(form); });

    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      trackFormStart(form);
      if (!email || !email.value.trim()) return;
      if (status) status.textContent = "Sending…";
      if (btn) btn.disabled = true;
      try {
        var res = await fetch("/api/subscribe", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: email.value.trim(),
            company: (form.querySelector('input[name="company"]') || {}).value || "",
          }),
        });
        var data = await res.json().catch(function () { return {}; });
        if (!res.ok || !data.ok) {
          throw new Error(data.error || "Could not subscribe.");
        }
        var msg = data.message || "You are on the list. We will email when a new letter posts.";
        var outcome = /already subscribed/i.test(msg) ? "already_subscribed" : "new_subscriber";
        store(SUBSCRIBED_KEY, "1");
        if (status) status.textContent = msg;
        // The thank-you page sends subscribe_complete, so the event survives the navigation.
        window.location.assign(thanksUrl(outcome, formLocation(form)));
      } catch (err) {
        track("subscribe_error", { form_location: formLocation(form), page: pagePath() });
        if (status) status.textContent = err.message || "Could not subscribe.";
        if (btn) btn.disabled = false;
      }
    });
  }

  // A slim bar on letter pages that points readers at the signup box once they
  // are into the letter, and gets out of the way when the box itself is on screen.
  function mountReadBar() {
    var article = document.querySelector("article.issue-page");
    var box = document.getElementById("new-subscribers");
    if (!article || !box) return;
    if (store(SUBSCRIBED_KEY) === "1") return;
    var dismissed = Number(store(BAR_DISMISSED_KEY) || 0);
    if (dismissed && Date.now() - dismissed < BAR_QUIET_DAYS * 86400000) return;

    var bar = document.createElement("div");
    bar.className = "sub-bar";
    bar.hidden = true;
    bar.innerHTML =
      '<p class="sub-bar-text">Get the next letter by email. Free, and one click to leave.</p>' +
      '<a class="btn btn-primary sub-bar-go" href="#new-subscribers">Subscribe</a>' +
      '<button type="button" class="sub-bar-close" aria-label="Dismiss">×</button>';
    document.body.appendChild(bar);

    var boxVisible = false;
    var shownOnce = false;
    function update() {
      var rect = article.getBoundingClientRect();
      var read = rect.height > 0 ? (window.innerHeight - rect.top) / rect.height : 0;
      var show = read > 0.35 && !boxVisible;
      bar.hidden = !show;
      if (show && !shownOnce) {
        shownOnce = true;
        track("subscribe_bar_view", { form_location: "issue-bar", page: pagePath() });
      }
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        boxVisible = entries[0].isIntersecting;
        update();
      }).observe(box);
    }
    window.addEventListener("scroll", update, { passive: true });

    bar.querySelector(".sub-bar-go").addEventListener("click", function (event) {
      event.preventDefault();
      track("subscribe_bar_click", { form_location: "issue-bar", page: pagePath() });
      box.scrollIntoView({ behavior: "smooth", block: "center" });
      var input = box.querySelector('input[name="email"]');
      if (input) input.focus({ preventScroll: true });
    });
    bar.querySelector(".sub-bar-close").addEventListener("click", function () {
      store(BAR_DISMISSED_KEY, String(Date.now()));
      bar.remove();
      window.removeEventListener("scroll", update);
    });
  }

  var forms = Array.prototype.slice.call(document.querySelectorAll("[data-subscribe-form]"));
  forms.forEach(bind);
  watchViews(forms);
  mountReadBar();

  window.ParamariboSubscribe = { track: track, pagePath: pagePath };
})();
