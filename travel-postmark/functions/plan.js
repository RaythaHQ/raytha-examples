/**
 * Trip planner handler. Route: forms/plan (POST from the form on /plan).
 * Checks the answers, saves them as a draft "trip_requests" item that only the Postmark team can read in the admin,
 * then redirects to /plan/thanks. Nothing is published, and nothing is sold or charged here: quotes go out by email.
 * "website" is a honeypot field that people never see.
 */
var TIERS = ["weekender", "classic", "long-haul", "wildcard", "unsure"];
var VIBES = ["beaches", "cities", "food", "mountains", "culture", "nightlife", "nature", "slow"];
function values(payload, key) {
  var p = Array.from(payload || []).find(function (x) { return String(x.Key) === key; });
  return p ? Array.from(p.Value).map(function (v) { return String(v || ""); }) : [];
}
function param(payload, key) { return values(payload, key)[0] || ""; }
function clean(s, max) { return String(s).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").trim().slice(0, max); }
function back(code, gift) { return new RedirectResult("/plan?error=" + code + (gift ? "&gift=1" : "") + "#planner"); }
// Search by name: GetWebTemplates() with no arguments only returns the first 50 templates across all themes.
function templateId(name) {
  var t = Array.from(API_V1.GetWebTemplates(name, "", 1, 200).Result.Items).find(function (x) { return String(x.DeveloperName) === name; });
  return t ? t.Id : null;
}
function get(query) { return new RedirectResult("/plan"); }
function post(payload, query) {
  if (param(payload, "website") !== "") return new RedirectResult("/plan/thanks"); // a bot: pretend it worked
  var gift = param(payload, "is_gift") === "true";
  var d = {
    contact_name: clean(param(payload, "contact_name"), 120),
    email: clean(param(payload, "email"), 160),
    home_airport: clean(param(payload, "home_airport"), 60).toUpperCase(),
    tier: param(payload, "tier"),
    month: clean(param(payload, "month"), 40),
    vibes: values(payload, "vibes").filter(function (v) { return VIBES.indexOf(v) >= 0; }).join(", "),
    no_go: clean(param(payload, "no_go"), 600),
    passport: param(payload, "passport") === "true",
    is_gift: gift,
    recipient: gift ? clean(param(payload, "recipient"), 120) : "",
    notes: clean(param(payload, "notes"), 1500)
  };
  if (!d.contact_name || !d.email || !d.home_airport) return back("missing", gift);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)) return back("email", gift);
  if (TIERS.indexOf(d.tier) < 0) return back("tier", gift);
  var n = parseInt(param(payload, "travelers"), 10);
  if (!(n >= 1 && n <= 8)) return back("travelers", gift);
  d.travelers = n;
  if (gift && !d.recipient) return back("recipient", gift);
  var res = API_V1.CreateContentItem("trip_requests", true, templateId("pm_detail_private"), d);
  if (!res.Success) return back("failed", gift);
  return new RedirectResult("/plan/thanks?name=" + encodeURIComponent(d.contact_name.split(" ")[0]) + (gift ? "&gift=1" : ""));
}
