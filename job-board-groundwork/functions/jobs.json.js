/**
 * Every open role as a JSON Feed 1.1 document (https://jsonfeed.org/version/1.1).
 * Route: feeds/jobs.json   Optional filters: ?category=data  ?type=remote  ?tag=python
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
// A relation field returns the related content item itself.
function companyOf(item) {
  try { var c = item.PublishedContent.Item.get("company"); return c && c.PrimaryField ? { name: String(c.PrimaryField), route: String(c.RoutePath) } : null; } catch (e) { return null; }
}
function isoDate(s) { var d = new Date(s); return isNaN(d) ? "" : d.toISOString().slice(0, 10); }
function where(lt, loc) { var t = TYPE[lt] || lt; return loc.indexOf(t) === 0 ? loc : t + " · " + loc; }
var SYM = { USD: "$", EUR: "€", GBP: "£", CAD: "CA$" };
var TYPE = { remote: "Remote", hybrid: "Hybrid", onsite: "On-site" };
function money(n, cur) { return (SYM[cur] || "") + Math.round(Number(n) / 1000) + "k"; }
function get(query) {
  var base = String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, "");
  var res = API_V1.GetContentItems("jobs", "", "", filterFrom(query), "posted_on desc", 1, 200).Result;
  var items = Array.from(res.Items).map(function (it) {
    var co = companyOf(it), cur = field(it, "currency"), lt = field(it, "location_type");
    var posted = new Date(field(it, "posted_on"));
    var tags = field(it, "tags").split(/[,;\s]+/).filter(Boolean);
    return {
      id: String(it.Id.ToString()),
      url: base + "/" + it.RoutePath,
      external_url: field(it, "apply_url"),
      title: it.PrimaryField + (co ? " at " + co.name : ""),
      summary: field(it, "summary"),
      content_html: "<p>" + field(it, "summary") + "</p><p>" + where(lt, field(it, "location")) +
        " · " + money(field(it, "salary_min"), cur) + "–" + money(field(it, "salary_max"), cur) + " " + cur + "</p>",
      date_published: isNaN(posted) ? undefined : posted.toISOString(),
      tags: tags,
      _job: {
        company: co ? co.name : "", company_url: co ? base + "/" + co.route : "",
        category: field(it, "category"), location_type: lt, location: field(it, "location"),
        salary: { min: Number(field(it, "salary_min")), max: Number(field(it, "salary_max")), currency: cur },
        employment_type: field(it, "employment_type"), seniority: field(it, "seniority"),
        featured: field(it, "featured").toLowerCase() === "true", valid_through: isoDate(field(it, "valid_through"))
      }
    };
  });
  return new JsonResult({
    version: "https://jsonfeed.org/version/1.1",
    title: "Groundwork: climate tech jobs",
    home_page_url: base + "/jobs",
    feed_url: base + "/feeds/jobs.json",
    description: "Remote and hybrid roles at climate tech companies, with a salary range on every listing.",
    items: items
  });
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
