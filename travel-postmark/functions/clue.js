/**
 * Random clue. Route: clue.json (GET).
 * Picks one past reveal and returns the clue from its envelope, plus the answer and a link, so the home page
 * can play "guess the destination". ?n= picks a specific one (1-based) so links can be shared.
 */
function field(item, key) { try { var v = item.PublishedContent.Item.get(key); return v ? String(v.ToString()) : ""; } catch (e) { return ""; } }
function param(query, key) { var p = Array.from(query || []).find(function (x) { return String(x.Key) === key; }); return p ? String(p.Value[0]) : ""; }
function get(query) {
  var items = Array.from(API_V1.GetContentItems("reveals", "", "", "", "sort_order asc", 1, 200).Result.Items);
  if (!items.length) return new StatusCodeResult(404, "No reveals yet");
  var n = parseInt(param(query, "n"), 10);
  var i = n >= 1 && n <= items.length ? n - 1 : Math.floor(Math.random() * items.length);
  var it = items[i];
  return new JsonResult({
    n: i + 1, of: items.length, clue: field(it, "clue"),
    answer: String(it.PrimaryField), country: field(it, "country"), when: field(it, "when"),
    travelers: field(it, "travelers"), reaction: field(it, "reaction"), url: "/" + String(it.RoutePath)
  });
}
function post(payload, query) { return new StatusCodeResult(405, "Use GET"); }
