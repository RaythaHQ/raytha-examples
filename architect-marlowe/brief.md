# Brief: Marlowe Architecture, a web design agency site

The brief as the agent got it.

> Build the website of a fictional web design and development studio on a fresh Raytha instance with the `raytha` CLI. No clicking around the admin.

## Look and feel

- Confident and editorial, the way a design studio presents itself. Large, readable headings, generous whitespace, real case study imagery. No wide display fonts.
- Responsive. It has to look good on a phone as well as a desktop.
- Accessible markup: landmarks, a skip link, visible focus, alt text, labelled controls.
- Server-rendered templates. No client-side app in the layout.

## Content and pages

- A home page with selected work, a client logo wall, services, the process, a testimonial and recent insights.
- Case studies filterable by industry, each with the challenge, what the studio did, results, the stack and a client quote.
- Services with deliverables and timelines, a studio page with the team, an insights blog, careers with open roles, contact and search.
- A members-only client portal: each client signs in and sees only their own projects, status updates, deliverables and brand assets. The studio team sees every client.
- No payment, registration or job application forms. Every client, person and project is fictional.
- Make it obvious everywhere that the studio and its clients are fictional.

## Done means

- `raytha check` passes with no broken routes.
- Screenshots of the result on desktop and mobile, and a walkthrough video.
- A kit in the examples repository that rebuilds the site on a fresh install.
