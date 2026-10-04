/**
 * Nomination form handler. Route: forms/nominate (POST from the form on /nominate).
 * Checks the fields, saves the nomination as a draft "nominations" item for the team to review, then redirects to /thanks.
 * Nothing is published automatically. "website" is a honeypot field that people never see.
 */
function param(payload, key) {
  var p = Array.from(payload || []).find(function (x) { return String(x.Key) === key; });
  return p ? String(p.Value[0] || "") : "";
}
function clean(s, max) { return String(s).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").trim().slice(0, max); }
function back(code) { return new RedirectResult("/nominate?error=" + code); }
function templateId(name) {
  var t = Array.from(API_V1.GetWebTemplates().Result.Items).find(function (x) { return String(x.DeveloperName) === name; });
  return t ? t.Id : null;
}
function categoryNames() {
  return Array.from(API_V1.GetContentItems("categories", "", "", "", "sort_order asc", 1, 50).Result.Items).map(function (c) { return String(c.PrimaryField); });
}
function get(query) { return new RedirectResult("/nominate"); }
function post(payload, query) {
  if (param(payload, "website") !== "") return new RedirectResult("/thanks?f=nominate"); // bot: pretend it worked
  var d = {
    nominee: clean(param(payload, "nominee"), 120),
    nominee_link: clean(param(payload, "nominee_link"), 300),
    category: clean(param(payload, "category"), 60),
    reason: clean(param(payload, "reason"), 1500),
    nominator_name: clean(param(payload, "nominator_name"), 120),
    nominator_email: clean(param(payload, "nominator_email"), 160)
  };
  if (!d.nominee || !d.reason || !d.nominator_name || !d.nominator_email) return back("missing");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.nominator_email)) return back("email");
  if (d.nominee_link && !/^https?:\/\/\S+$/i.test(d.nominee_link)) return back("link");
  if (categoryNames().indexOf(d.category) < 0) return back("category");
  var res = API_V1.CreateContentItem("nominations", true, templateId("ht_detail_submission"), d);
  if (!res.Success) return back("failed");
  return new RedirectResult("/thanks?f=nominate");
}
