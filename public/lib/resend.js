/** Small Resend REST helpers for Paramaribo Letter subscribers. */

const RESEND = "https://api.resend.com";

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    const err = new Error(`Missing ${name}`);
    err.status = 503;
    throw err;
  }
  return value;
}

async function resend(path, { method = "GET", body } = {}) {
  const key = requireEnv("RESEND_API_KEY");
  const res = await fetch(`${RESEND}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { raw: text };
  }
  if (!res.ok) {
    const err = new Error((data && (data.message || data.error)) || `Resend ${res.status}`);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

function segmentId() {
  return process.env.RESEND_SEGMENT_ID || "";
}

async function createSubscriber(email) {
  const body = {
    email,
    unsubscribed: false,
  };
  const seg = segmentId();
  if (seg) {
    body.segments = [{ id: seg }];
  }
  return resend("/contacts", { method: "POST", body });
}

async function unsubscribeEmail(email) {
  // Prefer update-by-email when available; fall back to list + patch.
  try {
    return await resend(`/contacts/${encodeURIComponent(email)}`, {
      method: "PATCH",
      body: { unsubscribed: true },
    });
  } catch (err) {
    if (err.status !== 404) throw err;
  }
  const listed = await listAllContacts();
  const hit = listed.find((c) => (c.email || "").toLowerCase() === email.toLowerCase());
  if (!hit) {
    const err = new Error("Email not found");
    err.status = 404;
    throw err;
  }
  return resend(`/contacts/${hit.id}`, {
    method: "PATCH",
    body: { unsubscribed: true },
  });
}

async function listAllContacts() {
  const seg = segmentId();
  const contacts = [];
  let after = null;
  for (let i = 0; i < 50; i += 1) {
    const qs = new URLSearchParams({ limit: "100" });
    if (seg) qs.set("segment_id", seg);
    if (after) qs.set("after", after);
    const page = await resend(`/contacts?${qs.toString()}`);
    const rows = page.data || page.contacts || [];
    contacts.push(...rows);
    const next = page.has_more && rows.length ? rows[rows.length - 1].id : null;
    if (!next) break;
    after = next;
  }
  return contacts;
}

async function sendEmail({ to, subject, html, text }) {
  const from = requireEnv("RESEND_FROM_EMAIL");
  return resend("/emails", {
    method: "POST",
    body: {
      from,
      to: [to],
      subject,
      html,
      text,
    },
  });
}

function isValidEmail(email) {
  if (typeof email !== "string") return false;
  const e = email.trim().toLowerCase();
  if (e.length < 5 || e.length > 254) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);
}

module.exports = {
  createSubscriber,
  unsubscribeEmail,
  listAllContacts,
  sendEmail,
  isValidEmail,
  requireEnv,
};
