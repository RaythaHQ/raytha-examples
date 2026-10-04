/**
 * RSVP form handler. Route: forms/rsvp (POST from the form on /rsvp).
 * Checks every field, saves the reply as a draft "rsvps" item that only the couple can see in the admin,
 * then redirects to /rsvp/thanks. Nothing is ever published. "website" is a honeypot field people never see.
 */
var DEADLINE = "2027-04-15"; // replies are accepted until the end of this day (US Eastern)
var MEALS = ["short_rib", "halibut", "risotto", "kids"];
function values(payload, key) {
  var p = Array.from(payload || []).find(function (x) { return String(x.Key) === key; });
  return p ? Array.from(p.Value).map(function (v) { return String(v || ""); }) : [];
}
function param(payload, key) { return values(payload, key)[0] || ""; }
function clean(s, max) { return String(s).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").trim().slice(0, max); }
function back(code) { return new RedirectResult("/rsvp?error=" + code); }
// Search by name: GetWebTemplates() with no arguments only returns the first 50 templates across all themes.
function templateId(name) {
  var t = Array.from(API_V1.GetWebTemplates(name, "", 1, 200).Result.Items).find(function (x) { return String(x.DeveloperName) === name; });
  return t ? t.Id : null;
}
function publicEvents() {
  return Array.from(API_V1.GetContentItems("events", "", "", "guests_only eq 'false'", "sort_order asc", 1, 50).Result.Items).map(function (e) { return String(e.PrimaryField); });
}
function get(query) { return new RedirectResult("/rsvp"); }
function post(payload, query) {
  if (param(payload, "website") !== "") return new RedirectResult("/rsvp/thanks"); // a bot: pretend it worked
  if (new Date() > new Date(DEADLINE + "T23:59:59-04:00")) return back("closed");
  var attending = param(payload, "attending");
  var d = {
    guest_name: clean(param(payload, "guest_name"), 120),
    email: clean(param(payload, "email"), 160),
    attending: attending,
    note: clean(param(payload, "note"), 1000)
  };
  if (!d.guest_name || !d.email || (attending !== "yes" && attending !== "no")) return back("missing");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)) return back("email");
  if (attending === "yes") {
    var size = parseInt(param(payload, "party_size"), 10);
    if (!(size >= 1 && size <= 6)) return back("party");
    var meal = param(payload, "meal");
    if (MEALS.indexOf(meal) < 0) return back("meal");
    var known = publicEvents();
    d.party_size = size;
    d.meal = meal;
    d.events = values(payload, "events").filter(function (e) { return known.indexOf(e) >= 0; }).join(", ");
    d.other_guests = clean(param(payload, "other_guests"), 600);
    d.dietary = clean(param(payload, "dietary"), 300);
    d.song = clean(param(payload, "song"), 140);
  } else {
    d.party_size = 0;
  }
  var res = API_V1.CreateContentItem("rsvps", true, templateId("wb_detail_private"), d);
  if (!res.Success) return back("failed");
  var first = d.guest_name.split(" ")[0];
  return new RedirectResult("/rsvp/thanks?a=" + attending + "&name=" + encodeURIComponent(first));
}
