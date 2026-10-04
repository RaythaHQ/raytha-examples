/**
 * Booking inquiry handler. Route: forms/booking (POST from the form on /booking).
 * Checks the fields, saves the inquiry as a draft "booking_requests" item that only the band can read in the admin,
 * then redirects to /booking/thanks. Nothing is published and no money changes hands here.
 * "website" is a honeypot field that people never see.
 */
var TYPES = ["club", "festival", "private", "benefit", "college", "other"];
function values(payload, key) {
  var p = Array.from(payload || []).find(function (x) { return String(x.Key) === key; });
  return p ? Array.from(p.Value).map(function (v) { return String(v || ""); }) : [];
}
function param(payload, key) { return values(payload, key)[0] || ""; }
function clean(s, max) { return String(s).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").trim().slice(0, max); }
function back(code) { return new RedirectResult("/booking?error=" + code + "#inquiry"); }
// Search by name: GetWebTemplates() with no arguments only returns the first 50 templates across all themes.
function templateId(name) {
  var t = Array.from(API_V1.GetWebTemplates(name, "", 1, 200).Result.Items).find(function (x) { return String(x.DeveloperName) === name; });
  return t ? t.Id : null;
}
function get(query) { return new RedirectResult("/booking"); }
function post(payload, query) {
  if (param(payload, "website") !== "") return new RedirectResult("/booking/thanks"); // a bot: pretend it worked
  var d = {
    contact_name: clean(param(payload, "contact_name"), 120),
    email: clean(param(payload, "email"), 160),
    phone: clean(param(payload, "phone"), 40),
    organization: clean(param(payload, "organization"), 160),
    event_type: param(payload, "event_type"),
    city: clean(param(payload, "city"), 120),
    sets: clean(param(payload, "sets"), 60),
    message: clean(param(payload, "message"), 2000)
  };
  if (!d.contact_name || !d.email || !d.message) return back("missing");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)) return back("email");
  if (TYPES.indexOf(d.event_type) < 0) return back("type");
  var date = param(payload, "event_date");
  if (date) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || new Date(date + "T23:59:59") < new Date()) return back("date");
    d.event_date = date;
  }
  var cap = parseInt(param(payload, "capacity"), 10);
  if (cap > 0 && cap < 100000) d.capacity = cap;
  var res = API_V1.CreateContentItem("booking_requests", true, templateId("lr_detail_private"), d);
  if (!res.Success) return back("failed");
  return new RedirectResult("/booking/thanks?name=" + encodeURIComponent(d.contact_name.split(" ")[0]));
}
