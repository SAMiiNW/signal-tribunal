# Public browser verification

- Date: 2026-10-02
- Production URL: https://signal-tribunal-asu.pages.dev/
- Cloudflare deployment: `846c23e2`
- Contract: `0xCc2360351758b16E79A475C257Fb3160490b8CdD`

The production root displayed the task-first Signal Tribunal home page rather than the obsolete Public Docket 42 demo. Independent HTTP checks returned `200` for Home, File, Review, Challenge, Lookup, Guide, and `app.js`. The deployed script contains the submitted StudioNet contract address.

A browser walkthrough opened Home, File, and Review as separate routes. File exposed editable source A/source B inputs, an immutable challenge-duration selector, and the publisher-independence warning. Review exposed assessment and finalization as separate actions and stated that assessment starts the full frozen challenge window. The existing live lifecycle proof remains case `ST-1789397743` in `network-run.json`.

The previously submitted `https://signal-tribunal.pages.dev/` still serves the obsolete one-page `PUBLIC DOCKET 42` build. That hostname is owned by a different Cloudflare account than the API token and OAuth account available in this workspace, so it cannot be overwritten with the credentials currently available.
