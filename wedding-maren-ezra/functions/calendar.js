/**
 * Wedding weekend calendar. Route: calendar.ics
 *   GET /calendar.ics          -> every public event of the weekend as one .ics file
 *   GET /calendar.ics?id=<id>  -> just that event
 * Events marked "guests only" are never included. Times are US Eastern.
 */
var DATES = { friday: "20270611", saturday: "20270612", sunday: "20270613" };
var NEXT = { friday: "20270612", saturday: "20270613", sunday: "20270614" };
var VTZ = ["BEGIN:VTIMEZONE", "TZID:America/New_York",
  "BEGIN:DAYLIGHT", "TZOFFSETFROM:-0500", "TZOFFSETTO:-0400", "TZNAME:EDT", "DTSTART:19700308T020000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU", "END:DAYLIGHT",
  "BEGIN:STANDARD", "TZOFFSETFROM:-0400", "TZOFFSETTO:-0500", "TZNAME:EST", "DTSTART:19701101T020000", "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU", "END:STANDARD",
  "END:VTIMEZONE"];
function field(item, key) { try { var v = item.PublishedContent.Item.get(key); return v ? String(v.ToString()) : ""; } catch (e) { return ""; } }
function param(query, key) { var p = Array.from(query || []).find(function (x) { return String(x.Key) === key; }); return p ? String(p.Value[0]) : ""; }
function esc(s) { return String(s || "").replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n"); }
function stamp() { return new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z"); }
function base() { return String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, ""); }
function hhmm(s) { var m = /^(\d{1,2}):(\d{2})$/.exec(s || ""); return m ? ("0" + m[1]).slice(-2) + m[2] + "00" : "120000"; }
function vevent(it) {
  var day = field(it, "day"), st = field(it, "start"), en = field(it, "end") || st;
  var endDate = en < st ? NEXT[day] : DATES[day]; // ends after midnight
  return ["BEGIN:VEVENT", "UID:" + String(it.Id.ToString()) + "@maren-and-ezra.example", "DTSTAMP:" + stamp(),
    "DTSTART;TZID=America/New_York:" + DATES[day] + "T" + hhmm(st), "DTEND;TZID=America/New_York:" + endDate + "T" + hhmm(en),
    "SUMMARY:" + esc(it.PrimaryField + " · Maren & Ezra"), "LOCATION:" + esc(field(it, "venue") + ", " + field(it, "address")),
    "DESCRIPTION:" + esc("Dress code: " + field(it, "dress_code") + "\n\n" + field(it, "summary") + "\n\n" + base() + "/" + it.RoutePath),
    "URL:" + base() + "/" + it.RoutePath, "END:VEVENT"];
}
function get(query) {
  var id = param(query, "id");
  var items = Array.from(API_V1.GetContentItems("events", "", "", "guests_only eq 'false'", "sort_order asc", 1, 50).Result.Items)
    .filter(function (it) { return DATES[field(it, "day")] && (!id || String(it.Id.ToString()) === id); });
  if (id && items.length === 0) return new StatusCodeResult(404, "No such event");
  var lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Maren and Ezra//Raytha Functions//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Maren & Ezra's wedding weekend"].concat(VTZ);
  items.forEach(function (it) { lines = lines.concat(vevent(it)); });
  lines.push("END:VCALENDAR");
  return new ContentResult(lines.join("\r\n") + "\r\n", "text/calendar; charset=utf-8");
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
