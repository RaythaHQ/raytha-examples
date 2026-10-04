/**
 * Instant search for the help center. Route: search.json?q=invite
 * Returns {"query": "...", "results": [{url, title, category, summary}]}, title matches first.
 */
function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v === null || v === undefined ? "" : String(v.ToString()); } catch (e) { return ""; }
}
function param(query, key) { var p = Array.from(query || []).find(function (x) { return x.Key === key; }); return p ? String(p.Value[0]) : ""; }
function categoryOf(item) {
  try { var c = item.PublishedContent.Item.get("category"); return c && c.PrimaryField ? String(c.PrimaryField) : ""; } catch (e) { return ""; }
}
function get(query) {
  // Keep letters, digits, spaces and a little punctuation so the value is safe inside the filter.
  var q = param(query, "q").replace(/[^\p{L}\p{N} .\-]/gu, " ").replace(/\s+/g, " ").trim().slice(0, 60);
  if (q.length < 2) return new JsonResult({ query: q, results: [] });
  var filter = "contains(title,'" + q + "') or contains(summary,'" + q + "') or contains(content,'" + q + "')";
  var res = API_V1.GetContentItems("articles", "", "", filter, "updated_on desc", 1, 25).Result;
  var lower = q.toLowerCase();
  var results = Array.from(res.Items).map(function (it) {
    return { url: "/" + it.RoutePath, title: String(it.PrimaryField), category: categoryOf(it), summary: field(it, "summary"),
             _rank: String(it.PrimaryField).toLowerCase().indexOf(lower) >= 0 ? 0 : 1 };
  }).sort(function (a, b) { return a._rank - b._rank; }).slice(0, 8)
    .map(function (r) { delete r._rank; return r; });
  return new JsonResult({ query: q, results: results });
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
