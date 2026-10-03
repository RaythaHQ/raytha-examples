---
name: raytha-site-builder
description: Build a complete Raytha website from a written brief in one pass with the raytha CLI, from content model and theme to seed content, pages, functions, menus, verification, screenshots and an idempotent rebuild script. Use when asked to build, one-shot or prototype a whole site on Raytha from a brief, or to turn a site into a reproducible example.
---

# Raytha site builder

This skill turns a brief into a finished, verified Raytha site that you can rebuild from files. It sits on top of
the official CLI skill, which covers the commands themselves:
[raytha-cli/skills/raytha/SKILL.md](https://github.com/RaythaHQ/raytha-cli/blob/main/skills/raytha/SKILL.md).
Load that too, and follow [AGENTS.md](../../AGENTS.md) for the rules and known pitfalls.

## Before you start

- `RAYTHA_URL` and `RAYTHA_API_KEY` must be set. Run `raytha doctor`. If a permission is missing, stop and say which.
- Read `raytha guide build-a-site`, and `raytha guide liquid` before writing templates.
- Read the brief twice. Write down anything it leaves open, pick a sensible default, and note it in your final
  report. Don't stop to ask unless the choice is destructive or can't be undone.

## Workflow

Work in a git-tracked directory, e.g. `./site`, laid out like the examples in this repo.

1. **Plan the content model.** List the content types, fields (type, required, choices, relationships) and the
   public views (route, sort, filter). Write `schema.json`. Look at
   [conference-horizon-summit/schema.json](../../conference-horizon-summit/schema.json) for the format, or export
   one with `raytha schema export`.
2. **Plan the routes.** List every URL: list views, item routes, site pages, function routes. Each should have a
   template.
3. **Theme.** `raytha theme pull raytha_default_theme ./site/theme`, rename it in `theme.json`, then write the base
   layout (head, SEO tags, navigation from `get_main_menu()`, footer), the list and detail templates per type, and
   the widget templates with settings forms for site pages. Load frameworks and fonts from a CDN.
   `raytha theme push ./site/theme --dry-run`, then push with `--activate`.
4. **Schema.** `raytha schema import schema.json --dry-run`, then import. Push the theme again so templates bind to
   the new types. Bind every view to its list template with `content-type views settings --template`.
5. **Seed content.** Write realistic, fictional content as JSON Lines in `seed/`. Images are generated SVGs or files
   you may redistribute, referenced as `@file:./path`. Import parents before children
   (`raytha content import <type> --file ... --template <detail_template>`). Lowercase item routes if needed.
6. **Site pages.** Build home and other landing pages from widgets: keep each page's sections in
   `pages/<page>.json` and create them with `raytha site-page create ... --sections @pages/<page>.json`.
7. **Functions, groups, menus.** Add Raytha Functions where the brief needs dynamic output (feeds, downloads, JSON).
   Create user groups for gated content. Create the menus.
8. **Verify.** Fetch every kind of page and read the HTML. Run `raytha check` until it's clean. Take desktop
   (1440px) and phone (390px) screenshots, look at them, and fix what's off. Repeat until it looks finished,
   not just until it works.
9. **Make it reproducible.** Write `build.sh`: idempotent, configured from `RAYTHA_URL` and `RAYTHA_API_KEY`, with a
   `DRY_RUN=1` mode, ending in `raytha check`. If you can, test it against a second, empty instance.
10. **Report.** What was built, the feature-to-Raytha mapping, decisions you made, anything left open, the
    screenshots, and how to rebuild.

## Quality bar

- It looks designed: a type scale, spacing rhythm, a palette, hover and focus states, and real empty states.
- It works at 390px wide with no horizontal scroll.
- Every page has a title, a meta description and a canonical URL.
- No secrets, real personal data or unlicensed images in the files.
- `raytha check` passes, and `build.sh` rebuilds the site from nothing.

## Example

[conference-horizon-summit/](../../conference-horizon-summit/) was built with this workflow from
[its brief](../../conference-horizon-summit/brief.md) in about 30 minutes.
