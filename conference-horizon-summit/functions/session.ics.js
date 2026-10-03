/**
 * Horizon Summit calendar files.
 * Function "session.ics" (route calendar/session.ics):          GET ?id=<session id>  -> one VEVENT
 * Function "event.ics"   (route calendar/horizon-summit-2027.ics): GET               -> the whole conference
 * The same code is deployed as both functions; MODE is set per function.
 */
var MODE = "session";
var DATES = { day_1: "20270413", day_2: "20270414", day_3: "20270415" };
var ROOMS = { main_stage: "Main Stage", hall_a: "Hall A · Colorado", hall_b: "Hall B · Pecan", workshop_lab: "Workshop Lab", studio_5: "Studio 5" };
var VTZ = [
  "BEGIN:VTIMEZONE", "TZID:America/Chicago",
  "BEGIN:DAYLIGHT", "TZOFFSETFROM:-0600", "TZOFFSETTO:-0500", "TZNAME:CDT", "DTSTART:19700308T020000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU", "END:DAYLIGHT",
  "BEGIN:STANDARD", "TZOFFSETFROM:-0500", "TZOFFSETTO:-0600", "TZNAME:CST", "DTSTART:19701101T020000", "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU", "END:STANDARD",
  "END:VTIMEZONE"
];

function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v ? String(v.ToString()) : ""; } catch (e) { return ""; }
}
function esc(s) { return String(s || "").replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n"); }
function param(query, key) { var p = Array.from(query || []).find(function (x) { return x.Key === key; }); return p ? String(p.Value[0]) : ""; }
function stamp() { return new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z"); }
function calendar(events) {
  var lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Horizon Summit//Raytha Functions//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Horizon Summit 2027"].concat(VTZ);
  events.forEach(function (e) { lines = lines.concat(e); });
  lines.push("END:VCALENDAR");
  return new ContentResult(lines.join("\r\n") + "\r\n", "text/calendar; charset=utf-8");
}
function base() { return String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, ""); }

function sessionEvent(item) {
  var day = field(item, "day"), d = DATES[day];
  var st = field(item, "start_time").replace(":", ""), en = field(item, "end_time").replace(":", "");
  var speaker = field(item, "speaker"), co = field(item, "cospeaker");
  var who = co ? speaker + " & " + co : speaker;
  return [
    "BEGIN:VEVENT",
    "UID:" + String(item.Id.ToString()) + "@horizonsummit.example",
    "DTSTAMP:" + stamp(),
    "DTSTART;TZID=America/Chicago:" + d + "T" + st + "00",
    "DTEND;TZID=America/Chicago:" + d + "T" + en + "00",
    "SUMMARY:" + esc(item.PrimaryField + " · Horizon Summit"),
    "LOCATION:" + esc((ROOMS[field(item, "room")] || "") + ", Mueller Commons, 4550 Hangar Lane, Austin, TX 78723"),
    "DESCRIPTION:" + esc(who + " · " + field(item, "track") + "\n\n" + field(item, "summary") + "\n\n" + base() + "/" + item.RoutePath),
    "URL:" + base() + "/" + item.RoutePath,
    "END:VEVENT"
  ];
}

function get(query) {
  if (MODE === "event") {
    return calendar([[
      "BEGIN:VEVENT", "UID:horizon-summit-2027@horizonsummit.example", "DTSTAMP:" + stamp(),
      "DTSTART;VALUE=DATE:20270413", "DTEND;VALUE=DATE:20270416",
      "SUMMARY:Horizon Summit 2027", "LOCATION:" + esc("Mueller Commons, 4550 Hangar Lane, Austin, TX 78723"),
      "DESCRIPTION:" + esc("Three days of AI, platform engineering, product and leadership.\n\nAgenda: " + base() + "/agenda"),
      "URL:" + base() + "/", "END:VEVENT"
    ]]);
  }
  var id = param(query, "id");
  if (!/^[A-Za-z0-9_-]{10,40}$/.test(id)) { return new StatusCodeResult(400, "Pass ?id=<session id>"); }
  var item;
  try { item = API_V1.GetContentItemById(id).Result; } catch (e) { return new StatusCodeResult(404, "Session not found"); }
  if (!item || !item.IsPublished || field(item, "day") === "") { return new StatusCodeResult(404, "Session not found"); }
  return calendar([sessionEvent(item)]);
}

function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
