const { createSubscriber, isValidEmail } = require("../lib/resend");

function cors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
}

module.exports = async function handler(req, res) {
  cors(res);
  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }
  if (req.method !== "POST") {
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  try {
    const body = typeof req.body === "string" ? JSON.parse(req.body || "{}") : req.body || {};
    // Honeypot: bots fill "company"
    if (body.company) {
      return res.status(200).json({ ok: true });
    }
    const email = String(body.email || "")
      .trim()
      .toLowerCase();
    if (!isValidEmail(email)) {
      return res.status(400).json({ ok: false, error: "Enter a valid email address." });
    }

    await createSubscriber(email);
    return res.status(200).json({
      ok: true,
      message: "You are on the list. We will email when a new letter posts.",
    });
  } catch (err) {
    const status = err.status || 500;
    // Duplicate contact is still a successful subscribe for the reader.
    const msg = String(err.message || "");
    if (status === 409 || /already|exists|duplicate/i.test(msg)) {
      return res.status(200).json({
        ok: true,
        message: "You are already subscribed.",
      });
    }
    if (status === 503) {
      return res.status(503).json({
        ok: false,
        error: "Subscriptions are not configured yet (missing Resend keys).",
      });
    }
    console.error("subscribe", err.data || err);
    return res.status(status >= 400 && status < 600 ? status : 500).json({
      ok: false,
      error: "Could not subscribe right now. Try again later.",
    });
  }
};
