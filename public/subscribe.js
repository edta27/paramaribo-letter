(function () {
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
        if (status) {
          status.innerHTML =
            (data.message || "Subscribed.") +
            ' <a href="unsubscribe.html">Unsubscribe</a> any time.';
        }
        form.reset();
      } catch (err) {
        if (status) status.textContent = err.message || "Could not subscribe.";
      } finally {
        if (btn) btn.disabled = false;
      }
    });
  }

  document.querySelectorAll("[data-subscribe-form]").forEach(bind);
})();
