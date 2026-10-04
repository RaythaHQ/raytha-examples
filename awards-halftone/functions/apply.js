/**
 * Entry form handler. Route: forms/apply (POST from the form on /apply).
 * Checks the fields, saves the entry as a draft "applications" item for the team to review, then redirects to /thanks.
 * Nothing is published automatically. "website" is a honeypot field that people never see.
 */
function param(payload, key) {
  var p = Array.from(payload || []).find(function (x) { return String(x.Key) === key; });
  return p ? String(p.Value[0] || "") : "";
}
function clean(s, max) { return String(s).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").trim().slice(0, max); }
function back(code) { return new RedirectResult("/apply?error=" + code); }
function templateId(name) {
  var t = Array.from(API_V1.GetWebTemplates().Result.Items).find(function (x) { return String(x.DeveloperName) === name; });
  return t ? t.Id : null;
}
function categoryNames() {
  return Array.from(API_V1.GetContentItems("categories", "", "", "", "sort_order asc", 1, 50).Result.Items).map(function (c) { return String(c.PrimaryField); });
}
function get(query) { return new RedirectResult("/apply"); }
function post(payload, query) {
  if (param(payload, "website") !== "") return new RedirectResult("/thanks?f=apply"); // bot: pretend it worked
  var d = {
    entrant_name: clean(param(payload, "entrant_name"), 120),
    email: clean(param(payload, "email"), 160),
    studio: clean(param(payload, "studio"), 120),
    category: clean(param(payload, "category"), 60),
    title: clean(param(payload, "title"), 140),
    link: clean(param(payload, "link"), 300),
    statement: clean(param(payload, "statement"), 1200),
    consent: param(payload, "consent") === "yes"
  };
  if (!d.entrant_name || !d.email || !d.title || !d.link || !d.statement) return back("missing");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)) return back("email");
  if (!/^https?:\/\/\S+$/i.test(d.link)) return back("link");
  if (categoryNames().indexOf(d.category) < 0) return back("category");
  if (!d.consent) return back("consent");
  var res = API_V1.CreateContentItem("applications", true, templateId("ht_detail_submission"), d);
  if (!res.Success) return back("failed");
  return new RedirectResult("/thanks?f=apply");
}
