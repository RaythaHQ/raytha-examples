/**
 * Every published rate as JSON, for branch lobby screens, a mobile app or a partner site. Route: feeds/rates.json
 * Add ?table=certificates (or savings, auto, home, personal) for one rate table only.
 * The rates are fictional: Kestrel Valley Credit Union is a made-up example.
 */
function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v === null || v === undefined ? "" : String(v.ToString()); } catch (e) { return ""; }
}
function rel(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v ? String(v.PrimaryField || "") : ""; } catch (e) { return ""; }
}
function param(query, key) { var p = Array.from(query || []).find(function (x) { return String(x.Key) === key; }); return p ? String(p.Value[0] || "") : ""; }
function base() { return String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, ""); }
var TABLES = { savings: "Savings and checking", certificates: "Certificates", auto: "Auto loans", home: "Home loans", personal: "Personal loans and cards" };
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
function get(query) {
  var table = param(query, "table").toLowerCase();
  if (!TABLES[table]) table = "";
  var res = API_V1.GetContentItems("rates", "", "", "", "sort_order asc", 1, 500).Result;
  var rates = Array.from(res.Items).filter(function (it) { return !table || field(it, "table") === table; }).map(function (it) {
    return {
      label: String(it.PrimaryField), table: field(it, "table"), tableLabel: TABLES[field(it, "table")] || "",
      product: rel(it, "product"), term: field(it, "term"), rate: parseFloat(field(it, "rate")) || null,
      rateType: field(it, "rate_type").toUpperCase(), asLowAs: field(it, "as_low_as").toLowerCase() === "true",
      minimum: field(it, "minimum"), note: field(it, "note"), effective: field(it, "effective").slice(0, 10), url: base() + "/" + it.RoutePath
    };
  });
  var body = { institution: "Kestrel Valley Credit Union", fictional: true,
    disclaimer: "Fictional rates for a Raytha example site. Not a real financial institution and not an offer of credit.",
    table: table || null, count: rates.length, rates: rates };
  return new JsonResult(body);
}
