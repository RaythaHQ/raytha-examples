# AGENTS.md: building Raytha sites with the CLI

Rules for coding agents (Cursor, Claude Code, Codex and the like) that build or change a Raytha site with the
[`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Copy this file into your own project. It goes with the
official skill at [`raytha-cli/skills/raytha/SKILL.md`](https://github.com/RaythaHQ/raytha-cli/blob/main/skills/raytha/SKILL.md)
and doesn't replace it: read that first, then this.

## Setup

- The CLI reads `RAYTHA_URL` and `RAYTHA_API_KEY` from the environment. `--url` and `--api-key` override them.
- Start every session with `raytha doctor` (connection, version, permissions), then `raytha guide build-a-site`.
  The built-in guides match the installed CLI version, so prefer them over memory.
- **Never print, log or commit an API key, password or connection string.** Keep them in the environment or in an
  untracked `.env`. Run `bash scripts/scan-secrets.sh` before any commit.

## The output contract

- stdout is always exactly one JSON document: `{"ok":true,"data":...}` or
  `{"ok":false,"error":{"code","message","hint"}}`. Parse it with `jq`. Don't scrape text.
- Exit codes: `0` ok, `2` usage or config, `3` auth or permission, `4` not found, `5` validation, `6` server or network.
- On an error, read `error.hint` and do what it says. On exit `3`, stop and report which permission is missing.
  Don't look for a way around it.
- List commands are paged. Use `--all` when you need everything.

## Work from files

- The site lives in a directory under git: `theme/`, `schema.json`, `functions/`, `seed/`, `pages/`, `menus/`.
  Edit files, then push them. Avoid one-off inline edits you can't reproduce.
- Start a theme from the built-ins: `raytha theme pull raytha_default_theme ./site/theme`, rename it in
  `theme.json`, then rewrite.
- **Dry-run first, every time:** `raytha theme push ./theme --dry-run`, `raytha schema import schema.json --dry-run`.
  A Liquid syntax error comes back with line and column before anything is saved.
- After every change, fetch the public page and read the HTML. Some Liquid errors (a bad filter argument, a nil
  object) only show up at render time.
- Finish with `raytha check`: it requests every public route like a visitor and exits `6` if any fail.
- Write the build as an idempotent script (see any `build.sh` in this repo) so the site can be rebuilt anywhere.

## Pitfalls we actually hit

These are from real builds on Raytha 2.0.1 with CLI 0.1.1.

1. **Set list view templates explicitly after a schema import.** A schema document names each view's template,
   but on a fresh site the import warns `template 'x' is not available in the active theme for this content type;
   using the default list template`, because the theme's templates can only be bound to a type once it exists. The
   views then render with the default list template. After the import (and the second theme push below), run
   `raytha content-type views settings <type> <view-id> --template <your_list_template>` for every view. Get the
   IDs from `raytha content-type views list <type>`.
2. **Push the theme again after the schema import.** Templates are bound to content types by developer name
   (`contentTypes` in each template's `.json`). If the theme goes in before the types exist, push it a second
   time once they do.
3. **Absolute URLs in Functions come from the site's configured URL.** `CurrentOrganization.WebsiteUrl` is
   whatever was set in the setup wizard or settings, not the host of the request. If it's wrong, every link in a
   feed, `.ics` file or sitemap is wrong. Check it before you debug the function.
4. **Prefer CDN assets in themes.** Load CSS frameworks, icon fonts and web fonts from a CDN (jsDelivr, Google
   Fonts) instead of theme media. The theme then moves between instances with no media to upload or re-link.
   Put the site's own images in the media library or in seed content.
5. **Dropdown values are objects in Liquid.** `{{ item.PublishedContent.day }}` prints `day_1`, but
   `{% if item.PublishedContent.day == "day_1" %}` is false. Capture it into a string first:
   `{% capture d %}{{ item.PublishedContent.day }}{% endcapture %}`. The same goes for IDs.
6. **Functions see content as .NET objects.** Read a field with
   `item.PublishedContent.Item.get("start_time").ToString()`, and call `.ToString()` on IDs. Wrap reads in
   `try`, because a missing field throws.
7. **Item URLs keep the primary field's capitals.** A route template like `speakers/{PrimaryField}` gives
   `speakers/Maya-Okafor`. Lowercase them after import with `raytha content settings <type> <id> --route-path ...`
   if you want clean URLs.
8. **`content import` isn't idempotent.** Running it twice creates duplicates. Check
   `raytha content list <type> --page-size 1` (`totalCount`) first.
9. **Destructive commands need `--yes`.** Deleting a menu item, page or item refuses to run without it. Never add
   `--yes` to anything you weren't asked to delete.
10. **Site pages save to a draft.** `site-page sections` writes a draft. Add `--publish`, or run
    `raytha site-page publish`.
11. **A fresh install isn't empty.** It has a Home and an About page, a `posts` content type, and Home, About and
    Posts links in the main menu. Decide what to do with them. Don't ignore them.
12. **Gate members-only content on the server.** Check `CurrentUser.UserGroups` in Liquid and don't render the
    HTML at all for non-members. Hiding it with CSS or JavaScript doesn't protect anything.
13. **CLI 0.1.1: `theme push --dry-run` can crash on a theme that doesn't exist yet** (a panic on a multi-byte
    character). Create the theme with a real push, or dry-run only against an existing theme.
14. **Number fields need converting before maths in Liquid.** `{{ job.PublishedContent.salary_min | divided_by: 1000 }}`
    fails with `Unable to cast ... DecimalFieldValue to IConvertible`. Turn the value into a string first:
    `{{ job.PublishedContent.salary_min | append: "" | divided_by: 1000 | floor }}`.
15. **Dates and the `json` filter need the raw value.** Use `{{ item.PublishedContent.posted_on.Value | date: "%b %-d" }}`
    (without `.Value` the date prints nothing), and `{{ item.PublishedContent.content | append: "" | json }}`
    (without `append` you get an object with `Value` and `Text` keys, which breaks JSON-LD).
16. **Checkbox filters compare to a string.** `featured eq 'true'` matches; `featured eq true` returns nothing.
17. **In Functions, a relationship field returns the related item.** `item.PublishedContent.Item.get("company")`
    is the company itself: read `.PrimaryField` and `.RoutePath` from it, no second lookup needed.
18. **Route paths can't start a segment with a dot.** A title like ".NET Engineer" gives `jobs/.NET-Engineer`;
    changing it with `content settings` is rejected until you drop the dot.

## Content and assets

- Use fictional, clearly placeholder data: `example.com` emails and URLs, 555 phone numbers, invented people and
  companies.
- Only use images you may redistribute: generated SVGs, your own screenshots, or images with an explicit license
  (credit them). No hotlinked stock photos, and no real people's photos attached to invented names.
- Respect `prefers-reduced-motion` and test at 390px wide as well as on desktop.
