/**
 * The latest stories as a JSON Feed 1.1 (https://jsonfeed.org). Route: feeds/latest.json  (add ?section=business for one section)
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
function get(query) {
  var b = base(), s = stories(query);
  return new JsonResult({
    version: "https://jsonfeed.org/version/1.1",
    title: "The Harbor Ledger" + (s.section && s.items.length ? ": " + rel(s.items[0], "section").name : ""),
    home_page_url: b + "/",
    feed_url: b + "/feeds/latest.json" + (s.section ? "?section=" + s.section : ""),
    description: "Nonprofit local news for Port Merrow.",
    language: "en-US",
    items: s.items.map(function (it) {
      var d = when(it), sec = rel(it, "section"), au = rel(it, "author");
      return { id: b + "/" + it.RoutePath, url: b + "/" + it.RoutePath, title: String(it.PrimaryField), summary: field(it, "dek"),
               date_published: d ? d.toISOString() : null, authors: [{ name: au.name, url: b + "/" + au.route }], tags: [sec.name],
               _ledger: { section: sec.name, type: field(it, "kind"), breaking: field(it, "breaking") === "True", live: field(it, "is_live") === "True" } };
    })
  });
}
