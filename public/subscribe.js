(function () {
  function ensureModal() {
    let root = document.getElementById("subscribe-thanks");
    if (root) return root;
    root = document.createElement("div");
    root.id = "subscribe-thanks";
    root.className = "sub-modal";
    root.hidden = true;
    root.innerHTML =
      '<div class="sub-modal-backdrop" data-sub-close></div>' +
      '<div class="sub-modal-card" role="dialog" aria-modal="true" aria-labelledby="sub-thanks-title">' +
      '<p class="sub-modal-kicker">The Paramaribo Letter</p>' +
      '<h2 id="sub-thanks-title">Thank you for subscribing</h2>' +
      '<p class="sub-modal-body" data-sub-modal-body>' +
      "You are on the list. We will email you when the next letter posts." +
      "</p>" +
      '<button type="button" class="btn sub-modal-btn" data-sub-close>Continue reading</button>' +
      '<p class="sub-modal-foot"><a href="unsubscribe.html">Unsubscribe</a> any time.</p>' +
      "</div>";
    document.body.appendChild(root);

    function close() {
      root.hidden = true;
      document.body.classList.remove("sub-modal-open");
    }
    root.querySelectorAll("[data-sub-close]").forEach((el) => {
      el.addEventListener("click", close);
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !root.hidden) close();
    });
    return root;
  }

  function showThanks(message) {
    const root = ensureModal();
    const body = root.querySelector("[data-sub-modal-body]");
    if (body && message) body.textContent = message;
    root.hidden = false;
    document.body.classList.add("sub-modal-open");
    const btn = root.querySelector(".sub-modal-btn");
    if (btn) btn.focus();
  }

  function bind(form) {
    if (!form || form.dataset.bound === "1") return;
    form.dataset.bound = "1";
    const status = form.querySelector("[data-sub-status]");
    const email = form.querySelector('input[name="email"]');
    const btn = form.querySelector('button[type="submit"]');

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!email || !email.value.trim()) return;
      if (status) status.textContent = "Sending…";
      if (btn) btn.disabled = true;
      try {
        const res = await fetch("/api/subscribe", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: email.value.trim(),
            company: (form.querySelector('input[name="company"]') || {}).value || "",
          }),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok || !data.ok) {
          throw new Error(data.error || "Could not subscribe.");
        }
        const msg =
          data.message || "You are on the list. We will email when a new letter posts.";
        if (status) {
          status.innerHTML =
            msg + ' <a href="unsubscribe.html">Unsubscribe</a> any time.';
        }
        form.reset();
        showThanks(msg);
      } catch (err) {
        if (status) status.textContent = err.message || "Could not subscribe.";
      } finally {
        if (btn) btn.disabled = false;
      }
    });
  }

  document.querySelectorAll("[data-subscribe-form]").forEach(bind);
})();
