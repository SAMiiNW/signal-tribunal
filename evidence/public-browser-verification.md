# Public browser verification

- Date: 2026-10-06
- Production URL: https://signal-tribunal.pages.dev/
- Cloudflare deployment: `f6986cbe`
- Contract: `0xCc2360351758b16E79A475C257Fb3160490b8CdD`

The exact submitted production root displayed the task-first Signal Tribunal home page rather than the obsolete Public Docket 42 demo. Browser checks opened Home, File, Review, Challenge, Lookup, and Guide with no console errors. The deployed application links the submitted StudioNet contract address.

A browser walkthrough opened all six routes as separate pages. File exposed editable source A/source B inputs, an immutable challenge-duration selector, and the publisher-independence warning. Review exposed assessment and finalization as separate actions and stated that assessment starts the full frozen challenge window.

The public Lookup route read case `ST-1789397743` from the deployed contract and rendered `FINAL / HTTP`, the two original authorities, the challenge authority, and all three matching assessment/latest-retrieval digests. The obsolete `PUBLIC DOCKET 42` content was absent from every checked route.
