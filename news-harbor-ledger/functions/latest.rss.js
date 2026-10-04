/**
 * The latest stories as an RSS 2.0 feed. Route: feeds/latest.rss  (add ?section=harbor-climate for one section)
 */
function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v === null || v === undefined ? "" : String(v.ToString()); } catch (e) { return ""; }
}
function rel(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v ? { name: String(v.PrimaryField || ""), route: String(v.RoutePath || "") } : { name: "", route: "" }; } catch (e) { return { name: "", route: "" }; }
}
function param(query, key) { var p = Array.from(query || []).find(function (x) { return String(x.Key) === key; }); return p ? String(p.Value[0] || "") : ""; }
// Newest 30 stories, optionally only one section (?section=city-hall, matching the section page URL).
function stories(query) {
  var want = param(query, "section").toLowerCase().replace(/[^a-z0-9\-]/g, "").slice(0, 60);
  var res = API_V1.GetContentItems("articles", "", "", "", "published_on desc", 1, 200).Result;
  var items = Array.from(res.Items).filter(function (it) {
    return !want || rel(it, "section").route.split("/").pop() === want;
  }).sort(function (a, b) { return (when(b) || 0) - (when(a) || 0); }).slice(0, 30);
  return { section: want, items: items };
}
function when(it) {
  // Combine the date field with the "9:40 PM" time stamp. Times are Port Merrow local time (US Eastern).
  var d = field(it, "published_on").slice(0, 10), t = field(it, "time_label").match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) { var p = new Date(field(it, "published_on")); if (isNaN(p)) return null; d = p.toISOString().slice(0, 10); }
  var h = 12, m = 0;
  if (t) { h = (+t[1] % 12) + (t[3].toUpperCase() === "PM" ? 12 : 0); m = +t[2]; }
  return new Date(d + "T" + ("0" + h).slice(-2) + ":" + ("0" + m).slice(-2) + ":00-04:00");
}
function base() { return String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, ""); }
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
function get(query) {
  var b = base(), s = stories(query);
  var items = s.items.map(function (it) {
    var d = when(it), url = b + "/" + it.RoutePath;
    return "<item><title>" + esc(it.PrimaryField) + "</title><link>" + url + "</link><guid isPermaLink=\"true\">" + url + "</guid>" +
      (d ? "<pubDate>" + d.toUTCString() + "</pubDate>" : "") + "<dc:creator>" + esc(rel(it, "author").name) + "</dc:creator>" +
      "<category>" + esc(rel(it, "section").name) + "</category><description>" + esc(field(it, "dek")) + "</description></item>";
  }).join("");
  var title = "The Harbor Ledger" + (s.section && s.items.length ? ": " + rel(s.items[0], "section").name : "");
  var self = b + "/feeds/latest.rss" + (s.section ? "?section=" + s.section : "");
  var xml = '<?xml version="1.0" encoding="utf-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel><title>' + esc(title) +
    "</title><link>" + b + "/</link><atom:link href=\"" + esc(self) + "\" rel=\"self\" type=\"application/rss+xml\"/><description>Nonprofit local news for Port Merrow.</description><language>en-us</language>" + items + "</channel></rss>";
  return new ContentResult(xml, "application/rss+xml");
}
