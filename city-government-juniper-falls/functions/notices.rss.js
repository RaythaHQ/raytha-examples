/**
 * Public notices (hearings, bids, ordinances, elections, construction) as RSS 2.0. Route: feeds/notices.rss
 * Add ?kind=hearing (or bid, ordinance, election, construction) for one kind only.
 */
function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v === null || v === undefined ? "" : String(v.ToString()); } catch (e) { return ""; }
}
function rel(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v ? String(v.PrimaryField || "") : ""; } catch (e) { return ""; }
}
function param(query, key) { var p = Array.from(query || []).find(function (x) { return String(x.Key) === key; }); return p ? String(p.Value[0] || "") : ""; }
function base() { return String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, ""); }
function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
var KINDS = { hearing: "Public hearing", bid: "Bid or RFP", ordinance: "Ordinance", election: "Election", construction: "Construction" };
function posted(it) {
  var d = field(it, "posted_on").slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) { var p = new Date(field(it, "posted_on")); if (isNaN(p)) return null; d = p.toISOString().slice(0, 10); }
  return new Date(d + "T08:00:00-05:00");
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
function get(query) {
  var b = base(), kind = param(query, "kind").toLowerCase();
  if (!KINDS[kind]) kind = "";
  var res = API_V1.GetContentItems("notices", "", "", "", "posted_on desc", 1, 200).Result;
  var items = Array.from(res.Items).filter(function (it) { return !kind || field(it, "kind") === kind; })
    .sort(function (a, b2) { return (posted(b2) || 0) - (posted(a) || 0); }).slice(0, 40);
  var body = items.map(function (it) {
    var d = posted(it), url = b + "/" + it.RoutePath, k = KINDS[field(it, "kind")] || "Notice";
    return "<item><title>" + esc(it.PrimaryField) + "</title><link>" + url + "</link><guid isPermaLink=\"true\">" + url + "</guid>" +
      (d ? "<pubDate>" + d.toUTCString() + "</pubDate>" : "") + "<category>" + esc(k) + "</category><dc:creator>" + esc(rel(it, "department")) + "</dc:creator>" +
      "<description>" + esc(field(it, "summary")) + "</description></item>";
  }).join("");
  var self = b + "/feeds/notices.rss" + (kind ? "?kind=" + kind : "");
  var xml = '<?xml version="1.0" encoding="utf-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel><title>City of Juniper Falls: public notices' + (kind ? " (" + esc(KINDS[kind]) + ")" : "") +
    "</title><link>" + b + "/notices</link><atom:link href=\"" + esc(self) + "\" rel=\"self\" type=\"application/rss+xml\"/><description>Public hearings, bids, ordinances, election notices and construction from the City of Juniper Falls, Texas (a fictional city).</description><language>en-us</language>" + body + "</channel></rss>";
  return new ContentResult(xml, "application/rss+xml");
}
