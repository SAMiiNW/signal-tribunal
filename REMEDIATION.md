# Steward remediation

| Requirement | Code path | Targeted proof | Status |
| --- | --- | --- | --- |
| Publish the six-page application at the originally submitted production hostname `signal-tribunal.pages.dev` | Cloudflare Pages project `signal-tribunal` built from `docs/` | Deployment `f6986cbe`; browser walkthrough of the exact submitted hostname; obsolete `PUBLIC DOCKET 42` content absent | PASS live |
| Provide Explorer links and per-transaction finality/execution records for the complete lifecycle | `evidence/network-run.json` and `README.md` | RPC receipt audit for deployment, propose, assess, challenge, and finalize | PASS live |
| Production bundle contains the six-page workflow | `docs/index.html`, `file.html`, `review.html`, `challenge.html`, `lookup.html`, `guide.html` | Home, File, Review, Challenge, Lookup and Guide verified at `signal-tribunal.pages.dev`; no browser errors | PASS live |
| Proposal and lifecycle controls call the deployed contract | `docs/app.js` points to `0xCc23...8CdD` and requires `MAJORITY_AGREE` | fresh SDK lifecycle plus frontend tests | PASS live |
| Challenge duration is fixed at proposal and starts after assessment | `propose`, `assess` | `test_delayed_assessment_gets_the_full_frozen_window` | PASS locally |
| Empty or malformed questions and invalid windows fail | `propose` | `test_empty_question_duplicate_sources_and_window_bounds_fail` | PASS locally |
| Web retrieval failure and malformed model output fail | `_judge`, `shape` | `test_failed_retrieval_and_malformed_model_output_fail` | PASS locally |
| Validator disagreement and truthy strings fail | `_judge.validate` uses `is True` | `test_validator_rejects_forged_output_disagreement_and_truthy_string` | PASS locally |
| Mutable source divergence cannot silently rewrite a ruling | `finalize` records `SOURCE_DIVERGED` and preserves provisional result | `test_mutable_original_source_divergence_is_terminal_and_explicit` | PASS locally |
| Challenge and finalization time boundaries are explicit | `challenge`, `finalize` | boundary tests | PASS locally |
| Source authority claims are not overstated | stored host authorities plus README and UI disclosure | documentation inspection | PASS locally |
| Evidence discovery and model limitations are explicit | README documents supplied-URL discovery, immutable challenge authority, bounded output, and failure modes | documentation inspection | PASS locally |
| Corrected deployment and complete onchain workflow | deployment manifest and `ST-1789397743` | deploy `0x0049...1308`; four finalized majority-agree lifecycle transactions; `FINAL / HTTP` readback | PASS live |
