const { unsubscribeEmail, isValidEmail } = require("../lib/resend");

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
    const email = String(body.email || "")
      .trim()
      .toLowerCase();
    if (!isValidEmail(email)) {
      return res.status(400).json({ ok: false, error: "Enter a valid email address." });
    }
    await unsubscribeEmail(email);
    return res.status(200).json({ ok: true, message: "You are unsubscribed." });
  } catch (err) {
    if (err.status === 404) {
      return res.status(200).json({ ok: true, message: "You are unsubscribed." });
    }
    if (err.status === 503) {
      return res.status(503).json({
        ok: false,
        error: "Unsubscribe is not configured yet (missing Resend keys).",
      });
    }
    console.error("unsubscribe", err.data || err);
    return res.status(500).json({ ok: false, error: "Could not unsubscribe right now." });
  }
};
