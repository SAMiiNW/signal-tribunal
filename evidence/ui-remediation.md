# Signal Tribunal UI remediation

Reviewer request: improve UI/UX, use different pages, and remove confusing one-page navigation.

| Mandatory requirement | Implementation | Verification | Status |
| --- | --- | --- | --- |
| Easy to understand and use | Task-first home screen, numbered lifecycle, contextual help, plain-language errors and explicit progress states | Static route/link audit plus published browser walkthrough | PASS |
| Use different pages | Separate Home, File, Review, Challenge, Lookup, and Guide documents | Six independent HTML entry points | PASS |
| Remove confusing one-page workflow | One primary task per page; shared persistent navigation and breadcrumbs | All six routes opened independently; published routes verified after Pages deployment | PASS |
| Preserve working contract integration | All write pages use deployed address and current method signatures; Lookup reads canonical state | JS syntax check, 3 contract tests, published StudioNet lookup of `ST-1788573405` returned `FINAL` / `PASSED` | PASS |
| Avoid false finality | UI labels wallet approval, submitted state, and FINALIZED receipt separately | Source review | PASS |

Optional polish: responsive layout, keyboard-visible form focus, reduced-motion support, and labelled read-only example.
