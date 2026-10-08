/**
 * Every public meeting as an iCalendar feed residents can subscribe to. Route: feeds/meetings.ics
 * Add ?board=city-council (the board page's URL slug) to get one board only. Times are Juniper Falls local time (US Central).
 */
function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v === null || v === undefined ? "" : String(v.ToString()); } catch (e) { return ""; }
}
function rel(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v ? { slug: String(v.RoutePath || "").split("/").pop(), name: String(v.PrimaryField || "") } : { slug: "", name: "" }; } catch (e) { return { slug: "", name: "" }; }
}
function param(query, key) { var p = Array.from(query || []).find(function (x) { return String(x.Key) === key; }); return p ? String(p.Value[0] || "") : ""; }
function base() { return String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, ""); }
function ymd(it) {
  var d = field(it, "start").slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) { var p = new Date(field(it, "start")); if (isNaN(p)) return ""; d = p.toISOString().slice(0, 10); }
  return d.replace(/-/g, "");
}
function hm(it) {
  var t = field(it, "time_label").match(/^(\d{1,2}):(\d{2})\s*(am|pm)$/i);
  if (!t) return "180000";
  return ("0" + ((+t[1] % 12) + (t[3].toLowerCase() === "pm" ? 12 : 0))).slice(-2) + t[2] + "00";
}
function esc(s) { return String(s).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n"); }
function fold(line) { var out = [], s = line; while (s.length > 74) { out.push(s.slice(0, 74)); s = " " + s.slice(74); } out.push(s); return out.join("\r\n"); }
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
function get(query) {
  var b = base(), want = param(query, "board").toLowerCase().replace(/[^a-z0-9\-]/g, "").slice(0, 60);
  var res = API_V1.GetContentItems("meetings", "", "", "", "start asc", 1, 500).Result;
  var stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z";
  var lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//City of Juniper Falls//Public meetings//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
    "X-WR-CALNAME:City of Juniper Falls public meetings", "X-WR-TIMEZONE:America/Chicago",
    "BEGIN:VTIMEZONE", "TZID:America/Chicago", "BEGIN:DAYLIGHT", "TZOFFSETFROM:-0600", "TZOFFSETTO:-0500", "TZNAME:CDT", "DTSTART:19700308T020000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU", "END:DAYLIGHT",
    "BEGIN:STANDARD", "TZOFFSETFROM:-0500", "TZOFFSETTO:-0600", "TZNAME:CST", "DTSTART:19701101T020000", "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU", "END:STANDARD", "END:VTIMEZONE"];
  Array.from(res.Items).forEach(function (it) {
    var board = rel(it, "board");
    if (want && board.slug !== want) return;
    var d = ymd(it); if (!d) return;
    var start = d + "T" + hm(it), h = +start.slice(9, 11) + 2, end = d + "T" + ("0" + Math.min(h, 23)).slice(-2) + start.slice(11);
    var status = field(it, "status"), url = b + "/" + it.RoutePath;
    lines.push("BEGIN:VEVENT", "UID:" + String(it.RoutePath).replace(/\//g, "-") + "@juniperfalls.example", "DTSTAMP:" + stamp,
      "DTSTART;TZID=America/Chicago:" + start, "DTEND;TZID=America/Chicago:" + end,
      fold("SUMMARY:" + esc((status === "cancelled" ? "CANCELLED: " : "") + it.PrimaryField)),
      fold("LOCATION:" + esc(field(it, "location"))), fold("DESCRIPTION:" + esc(field(it, "summary") + " Agenda and documents: " + url)),
      "URL:" + url, "STATUS:" + (status === "cancelled" ? "CANCELLED" : "CONFIRMED"), "CATEGORIES:" + esc(board.name), "END:VEVENT");
  });
  lines.push("END:VCALENDAR");
  return new ContentResult(lines.join("\r\n") + "\r\n", "text/calendar; charset=utf-8");
}
