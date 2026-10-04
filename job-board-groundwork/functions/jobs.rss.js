/**
 * Every open role as an RSS 2.0 feed. Route: feeds/jobs.rss
 * Optional filters: ?category=data  ?type=remote  ?tag=python
 */
function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v === null || v === undefined ? "" : String(v.ToString()); } catch (e) { return ""; }
}
function param(query, key) { var p = Array.from(query || []).find(function (x) { return x.Key === key; }); return p ? String(p.Value[0]) : ""; }
function filterFrom(query) {
  var parts = [];
  var c = param(query, "category"), t = param(query, "type"), g = param(query, "tag");
  if (/^[a-z_]+$/.test(c)) parts.push("category eq '" + c + "'");
  if (/^(remote|hybrid|onsite)$/.test(t)) parts.push("location_type eq '" + t + "'");
  if (/^[a-z_]+$/.test(g)) parts.push("contains(tags,'" + g + "')");
  return parts.join(" and ");
}
function xml(s) { return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
var SYM = { USD: "$", EUR: "€", GBP: "£", CAD: "CA$" };
var TYPE = { remote: "Remote", hybrid: "Hybrid", onsite: "On-site" };
function where(lt, loc) { var t = TYPE[lt] || lt; return loc.indexOf(t) === 0 ? loc : t + " · " + loc; }
function money(n, cur) { return (SYM[cur] || "") + Math.round(Number(n) / 1000) + "k"; }
function get(query) {
  var base = String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, "");
  var res = API_V1.GetContentItems("jobs", "", "", filterFrom(query), "posted_on desc", 1, 200).Result;
  var out = [];
  out.push('<?xml version="1.0" encoding="UTF-8"?>');
  out.push('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>');
  out.push("<title>Groundwork: climate tech jobs</title><link>" + xml(base + "/jobs") + "</link>");
  out.push("<description>Remote and hybrid roles at climate tech companies, with a salary range on every listing.</description><language>en</language>");
  out.push('<atom:link href="' + xml(base + "/feeds/jobs.rss") + '" rel="self" type="application/rss+xml"/>');
  Array.from(res.Items).forEach(function (it) {
    var co = ""; try { var c = it.PublishedContent.Item.get("company"); co = c && c.PrimaryField ? String(c.PrimaryField) : ""; } catch (e) {}
    var cur = field(it, "currency"), lt = field(it, "location_type");
    var d = new Date(field(it, "posted_on"));
    var url = base + "/" + it.RoutePath;
    out.push("<item><title>" + xml(it.PrimaryField + (co ? " at " + co : "")) + "</title><link>" + xml(url) + "</link>" +
      '<guid isPermaLink="true">' + xml(url) + "</guid>" + (isNaN(d) ? "" : "<pubDate>" + d.toUTCString() + "</pubDate>") +
      "<category>" + xml(field(it, "category")) + "</category>" +
      "<description>" + xml(field(it, "summary") + " " + where(lt, field(it, "location")) + " · " +
        money(field(it, "salary_min"), cur) + "–" + money(field(it, "salary_max"), cur) + " " + cur) + "</description></item>");
  });
  out.push("</channel></rss>");
  return new ContentResult(out.join("\n"), "application/rss+xml; charset=utf-8");
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
