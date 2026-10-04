/**
 * The changelog as an RSS 2.0 feed. Route: feeds/changelog.rss
 */
function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v === null || v === undefined ? "" : String(v.ToString()); } catch (e) { return ""; }
}
function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function get(query) {
  var base = String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, "");
  var res = API_V1.GetContentItems("releases", "", "", "", "released_on desc", 1, 50).Result;
  var items = Array.from(res.Items).map(function (it) {
    var d = new Date(field(it, "released_on"));
    return "<item><title>" + esc(field(it, "version") + ": " + it.PrimaryField) + "</title><link>" + base + "/" + it.RoutePath +
      "</link><guid>" + base + "/" + it.RoutePath + "</guid>" + (isNaN(d) ? "" : "<pubDate>" + d.toUTCString() + "</pubDate>") +
      "<category>" + esc(field(it, "kind")) + "</category><description>" + esc(field(it, "summary")) + "</description></item>";
  }).join("");
  var xml = '<?xml version="1.0" encoding="utf-8"?><rss version="2.0"><channel><title>Orbitly changelog</title><link>' + base +
    "/changelog</link><description>New features, improvements and fixes in Orbitly.</description>" + items + "</channel></rss>";
  return new ContentResult(xml, "application/rss+xml");
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
