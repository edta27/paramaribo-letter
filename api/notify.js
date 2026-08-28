const { listAllContacts, sendEmail, requireEnv } = require("../lib/resend");

const SITE = process.env.SITE_URL || "https://paramaribo-letter.vercel.app";

function authorized(req) {
  const secret = process.env.NOTIFY_SECRET;
  if (!secret) return false;
  const header = req.headers.authorization || "";
  const bearer = header.startsWith("Bearer ") ? header.slice(7) : "";
  const alt = req.headers["x-notify-secret"] || "";
  return bearer === secret || alt === secret;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }
  if (!authorized(req)) {
    return res.status(401).json({ ok: false, error: "Unauthorized" });
  }

  try {
    requireEnv("RESEND_API_KEY");
    requireEnv("RESEND_FROM_EMAIL");

    const body = typeof req.body === "string" ? JSON.parse(req.body || "{}") : req.body || {};
    let issue = body.issue || null;

    if (!issue) {
      const catalogRes = await fetch(`${SITE}/catalog.json`, { cache: "no-store" });
      if (!catalogRes.ok) {
        throw Object.assign(new Error("Could not load catalog.json"), { status: 502 });
      }
      const catalog = await catalogRes.json();
      issue = Array.isArray(catalog) ? catalog[0] : null;
    }

    if (!issue || !issue.id || !issue.title) {
      return res.status(400).json({ ok: false, error: "No issue to announce." });
    }

    const url = `${SITE}/issue.html?id=${encodeURIComponent(issue.id)}`;
    const subject = `New Paramaribo Letter: ${issue.title}`;
    const dek = issue.dek || "";
    const kicker = issue.kicker || "The Paramaribo Letter";

    const contacts = await listAllContacts();
    const targets = contacts.filter((c) => c.email && !c.unsubscribed);
    let sent = 0;
    const errors = [];

    for (const contact of targets) {
      const email = contact.email;
      const unsub = `${SITE}/unsubscribe.html?email=${encodeURIComponent(email)}`;
      const html = `
        <div style="font-family: Georgia, serif; color:#1c1712; max-width:560px">
          <p style="font-size:12px; letter-spacing:0.12em; text-transform:uppercase; color:#7a7266">${escapeHtml(kicker)}</p>
          <h1 style="font-size:28px; line-height:1.2; margin:8px 0 12px">${escapeHtml(issue.title)}</h1>
          <p style="font-size:16px; line-height:1.5; color:#4a433a">${escapeHtml(dek)}</p>
          <p style="margin:24px 0">
            <a href="${url}" style="background:#8a2c2c; color:#fcfaf6; text-decoration:none; padding:12px 18px; display:inline-block">
              Read the letter
            </a>
          </p>
          <p style="font-size:12px; color:#7a7266; line-height:1.5">
            Educational research, not personalized advice.
            <a href="${unsub}" style="color:#7a7266">Unsubscribe</a>
          </p>
        </div>`;
      const text = [
        subject,
        "",
        dek,
        "",
        `Read: ${url}`,
        "",
        `Unsubscribe: ${unsub}`,
      ].join("\n");

      try {
        await sendEmail({ to: email, subject, html, text });
        sent += 1;
      } catch (err) {
        errors.push({ email, error: err.message });
      }
    }

    return res.status(200).json({
      ok: true,
      issueId: issue.id,
      subscribers: targets.length,
      sent,
      failed: errors.length,
      errors: errors.slice(0, 5),
    });
  } catch (err) {
    console.error("notify", err.data || err);
    const status = err.status === 503 ? 503 : 500;
    return res.status(status).json({
      ok: false,
      error: err.message || "Notify failed",
    });
  }
};
