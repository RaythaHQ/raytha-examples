# Brief: Pennowick Insurance Agency — an independent insurance agency website (fictional)
Persona: Pennowick Insurance Agency (fictional), a third-generation independent agency with three offices in the invented river town of Pennowick, appointed with ten invented carriers. The same build fits an agency, or a freelancer building sites for agency clients.
Design: "policy folder" — manila and paper tones, oxblood and deep teal ink, a brass stamp accent; navigation drawn as folder tabs; a hand-drawn street-block illustration in the hero where numbered pins (from each coverage line's pin_x / pin_y fields) mark what each policy covers; a carrier × coverage appointment matrix built from content; claims guides laid out as first hour / first day / first week columns; an A–Z glossary. Literata headings, Atkinson Hyperlegible body, Red Hat Mono for labels. No wide display fonts.
IA: home; /coverage (lines), /claims (guides), /carriers (appointments), /agents, /offices, /glossary, /resources (public, policyholder and business resources), /binder (members-only client binder), /about, /disclosures, /search.
Members: user groups `policyholders` and `business`; gating is server-side in Liquid with CurrentUser.UserGroups. Gated bodies are never sent to the browser.
No quote request, payment, registration or contact forms. Everything is labeled fictional; phone numbers use 555.
Buyer target: self-hosted CMS for insurance agencies / open-source .NET CMS for an insurance agency website.
Done: raytha check 0 failed, screenshots, walkthrough, rebuildable kit.
