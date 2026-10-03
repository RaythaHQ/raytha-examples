/**
 * Public JSON feed of the published agenda. Route: calendar/agenda.json
 * Optional ?day=day_1|day_2|day_3
 */
function field(item, key) {
  try { var v = item.PublishedContent.Item.get(key); return v ? String(v.ToString()) : ""; } catch (e) { return ""; }
}
function param(query, key) { var p = Array.from(query || []).find(function (x) { return x.Key === key; }); return p ? String(p.Value[0]) : ""; }
var ROOMS = { main_stage: "Main Stage", hall_a: "Hall A · Colorado", hall_b: "Hall B · Pecan", workshop_lab: "Workshop Lab", studio_5: "Studio 5" };
function get(query) {
  var day = param(query, "day");
  var filter = /^day_[123]$/.test(day) ? "day eq '" + day + "'" : "";
  var res = API_V1.GetContentItems("sessions", "", "", filter, "sort_key asc", 1, 200).Result;
  var base = String(CurrentOrganization.WebsiteUrl || "").replace(/\/$/, "");
  var items = Array.from(res.Items).map(function (it) {
    return {
      id: String(it.Id.ToString()), title: it.PrimaryField, url: base + "/" + it.RoutePath,
      day: field(it, "day"), start: field(it, "start_time"), end: field(it, "end_time"), timezone: "America/Chicago",
      room: ROOMS[field(it, "room")] || field(it, "room"), format: field(it, "format"), level: field(it, "level"),
      track: field(it, "track"), speakers: [field(it, "speaker"), field(it, "cospeaker")].filter(Boolean),
      summary: field(it, "summary"),
      ics: base + "/calendar/session.ics?id=" + String(it.Id.ToString())
    };
  });
  return new JsonResult({ event: "Horizon Summit 2027", dates: "2027-04-13/2027-04-15", total: res.TotalCount, sessions: items });
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
