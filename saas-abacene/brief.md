# Brief: Abacene — a SaaS product marketing site (fictional)
Persona: Abacene Labs (fictional), maker of Abacene, a usage-metering and billing-ledger product for API companies.
Design: "ledger tape" — warm paper, ink and forest green with a signal-orange accent; a printed invoice tape in the hero, a four-stage Meter → Aggregate → Rate → Invoice flow, an invoice-explain tree in monospace, spec-sheet feature rows, git-log style changelog. System sans + monospace numerals, no wide display fonts.
IA: home; /product (features), /pricing (plans as content), /docs (public, customer and beta docs), /changelog (release notes; beta entries members-only), /customers (stories), /integrations (directory), /security, /about, /beta (members-only customer & beta hub), /search.
Members: user groups `customers` and `beta`; gating is done in server-rendered Liquid with CurrentUser.UserGroups — gated bodies are never sent to the browser.
No payment, trial sign-up, registration or contact forms. Everything is story-labeled.
Buyer target: open-source .NET CMS for a SaaS marketing site / self-hosted headless-capable CMS for SaaS companies.
Done: raytha check 0 failed, screenshots, walkthrough, rebuildable kit.
