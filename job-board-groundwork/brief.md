# Brief: Groundwork, a climate tech job board

The brief exactly as the agent got it. It is the only input it had.

> Build a niche, realistic job board on a fresh Raytha instance with the `raytha` CLI: a remote jobs board for
> climate tech or for .NET developers (pick the more visually compelling one). No clicking around the admin.

## Look and feel

- Visually impressive and premium, with a look of its own: its own palette and a Google Fonts pairing.
- Display type that is well proportioned, not overly wide or squished.
- Responsive. It has to look good on a phone as well as a desktop.
- Company logos are generated SVGs, so there are no third-party license issues.

## Content model, with realistic seed content

- **Jobs** (about 25): company, location, remote/hybrid/on-site, salary range, tags and posted date.
- **Companies** (about 10): logo and a profile page that lists their jobs.

## Pages and functionality

- A job list you can filter and search by category, location type, salary and tags, using list views and query
  parameters.
- A page per job with a structured **Apply** link to an external URL. No forms, no payments.
- A featured jobs section.
- An RSS or JSON feed of jobs from a Raytha Function.
- Optionally, JobPosting JSON-LD on job pages for Google for Jobs.
- A members-only saved-search or employer hub page if it fits naturally.
- No registration, payment or job-posting forms.

## Done means

- `raytha check` passes with no broken routes.
- Screenshots of the result on desktop and mobile.
- The schema and theme exported so the site can be rebuilt or deployed elsewhere.
