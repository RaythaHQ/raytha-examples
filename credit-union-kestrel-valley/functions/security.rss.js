/**
 * Security alerts (scam warnings, service notices) as RSS 2.0. Route: feeds/security.rss
 * Add ?level=scam (or service, info) for one level only.
 */
function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v === null || v === undefined ? "" : String(v.ToString()); } catch (e) { return ""; }
}
function param(query, key) { var p = Array.from(query || []).find(function (x) { return String(x.Key) === key; }); return p ? String(p.Value[0] || "") : ""; }
function base() { return String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, ""); }
function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
var LEVELS = { scam: "Scam warning", service: "Service notice", info: "Good to know" };
function posted(it) {
  var d = field(it, "posted_on").slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) { var p = new Date(field(it, "posted_on")); if (isNaN(p)) return null; d = p.toISOString().slice(0, 10); }
  return new Date(d + "T08:00:00-05:00");
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
function get(query) {
  var b = base(), level = param(query, "level").toLowerCase();
  if (!LEVELS[level]) level = "";
  var res = API_V1.GetContentItems("alerts", "", "", "", "posted_on desc", 1, 200).Result;
  var items = Array.from(res.Items).filter(function (it) { return !level || field(it, "level") === level; })
    .sort(function (a, b2) { return (posted(b2) || 0) - (posted(a) || 0); }).slice(0, 40);
  var body = items.map(function (it) {
    var d = posted(it), url = b + "/" + it.RoutePath;
    return "<item><title>" + esc(it.PrimaryField) + "</title><link>" + url + "</link><guid isPermaLink=\"true\">" + url + "</guid>" +
      (d ? "<pubDate>" + d.toUTCString() + "</pubDate>" : "") + "<category>" + esc(LEVELS[field(it, "level")] || "Alert") + "</category>" +
      "<description>" + esc(field(it, "message")) + "</description></item>";
  }).join("");
  var self = b + "/feeds/security.rss" + (level ? "?level=" + level : "");
  var xml = '<?xml version="1.0" encoding="utf-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Kestrel Valley Credit Union: security alerts' + (level ? " (" + esc(LEVELS[level]) + ")" : "") +
    "</title><link>" + b + "/security</link><atom:link href=\"" + esc(self) + "\" rel=\"self\" type=\"application/rss+xml\"/><description>Scam warnings and service notices from Kestrel Valley Credit Union (a fictional credit union).</description><language>en-us</language>" + body + "</channel></rss>";
  return new ContentResult(xml, "application/rss+xml");
}
