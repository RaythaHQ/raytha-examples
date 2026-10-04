/**
 * Song stats as JSON. Route: songs.json (GET).
 * Reads every published setlist and counts how often each song was played, which songs open shows,
 * and which close them. ?song=Name returns the dates for one song. Same numbers as the /songs page.
 */
var SKIP = ["Drums", "Space"];
function field(item, key) { try { var v = item.PublishedContent.Item.get(key); return v ? String(v.ToString()) : ""; } catch (e) { return ""; } }
function param(query, key) { var p = Array.from(query || []).find(function (x) { return String(x.Key) === key; }); return p ? String(p.Value[0]) : ""; }
function iso(s) { var m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(s); return m ? m[3] + "-" + ("0" + m[1]).slice(-2) + "-" + ("0" + m[2]).slice(-2) : String(s).slice(0, 10); }
function lines(s) { return String(s || "").split(/\r?\n/).map(function (l) { return l.replace(/>/g, "").trim(); }).filter(function (l) { return l; }); }
function bump(map, k, date) { if (!map[k]) map[k] = { song: k, times: 0, dates: [] }; map[k].times++; map[k].dates.push(date); }
function ranked(map) { return Object.keys(map).map(function (k) { return map[k]; }).sort(function (a, b) { return b.times - a.times || a.song.localeCompare(b.song); }); }
function get(query) {
  var items = Array.from(API_V1.GetContentItems("setlists", "", "", "", "date desc", 1, 500).Result.Items);
  var all = {}, openers = {}, encores = {};
  items.forEach(function (it) {
    var date = iso(field(it, "date")) || String(it.PrimaryField).slice(0, 10);
    var s1 = lines(field(it, "set1")), s2 = lines(field(it, "set2")), enc = lines(field(it, "encore"));
    s1.concat(s2, enc).forEach(function (s) { if (SKIP.indexOf(s) < 0) bump(all, s, date); });
    if (s1.length) bump(openers, s1[0], date);
    enc.forEach(function (s) { bump(encores, s, date); });
  });
  var want = param(query, "song").toLowerCase();
  if (want) {
    var hit = ranked(all).find(function (r) { return r.song.toLowerCase() === want; });
    return hit ? new JsonResult(hit) : new StatusCodeResult(404, "We haven't played that one yet");
  }
  var songs = ranked(all);
  return new JsonResult({
    band: "Lantern Ramblers", shows: items.length, distinct_songs: songs.length,
    songs_played: songs.reduce(function (n, r) { return n + r.times; }, 0),
    top_songs: songs.map(function (r) { return { song: r.song, times: r.times, last_played: r.dates[0] }; }),
    openers: ranked(openers).map(function (r) { return { song: r.song, times: r.times }; }),
    encores: ranked(encores).map(function (r) { return { song: r.song, times: r.times }; })
  });
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
