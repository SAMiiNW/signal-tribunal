# Signal Tribunal

Signal Tribunal adds a real challenge window to source-bound event resolution. A provisional answer is not final: any participant can attach a third, independently hosted record, forcing a fresh validator-reviewed ruling over all evidence. The challenge duration is selected and frozen when the proposal is filed, but its deadline begins only after assessment finalizes. A delayed assessment therefore cannot consume the protected challenge period.

The contract normalizes IDs, binds content digests, restricts answers to declared choices, strictly verifies stored finding codes and rejects source-host reuse. During challenged finalization it refetches the original records. If either original digest changed, the case becomes `SOURCE_DIVERGED`, the provisional ruling is preserved, and the changed retrieval digests remain visible instead of silently rewriting the decision. Unchallenged resolutions become permissionlessly final only after the deadline; challenged cases can be finalized immediately after a fresh review.

## Source authority boundary

Different HTTPS hostnames provide transport separation, not proof that different organizations control the records. Signal Tribunal stores each hostname as an explicit authority identifier and exposes it in the public record, but filers and reviewers must verify the real-world publisher behind each source. Repository-hosted records in `evidence/` are labelled demo fixtures controlled by the project operator and are not presented as independent third-party authorities. Production cases should use stable, publicly auditable records from genuinely independent publishers. Content digests detect later mutation but do not authenticate the publisher.

Evidence discovery is intentionally explicit: the filer supplies the two public records and validators independently retrieve those exact URLs; the contract does not perform open-ended web search. The first accepted challenge stores its source and authority, changes the state to `CHALLENGED`, and makes that challenge immutable because a second challenge is rejected by the state machine. Model output is limited to declared answer choices and enumerated finding codes, then independently rechecked by validators. Retrieval failures, malformed output, disagreement, or changed original content fail safely or become an explicit `SOURCE_DIVERGED` record instead of being treated as arbitrary truth.

## Public interface

The public application is deliberately split into focused routes instead of one long dashboard:

- `index.html` — orientation and task selection
- `file.html` — create a source-bound proposal
- `review.html` — request assessment or finalize an eligible case
- `challenge.html` — lodge an independent third-source challenge
- `lookup.html` — read canonical contract state without a wallet
- `guide.html` — plain-language lifecycle and safety rules

Each write screen distinguishes wallet approval, transaction submission, and validator finalization. The filing screen freezes the challenge duration; the review screen cannot replace or shorten it. The lookup screen renders live contract data, stored source authorities, assessment and latest-retrieval digests, and explicit source-divergence state. The example ID is labelled as an example and is not used as hidden application state.

Current StudioNet contract: [`0xCc2360351758b16E79A475C257Fb3160490b8CdD`](https://explorer-studio.genlayer.com/address/0xCc2360351758b16E79A475C257Fb3160490b8CdD). Fresh case `ST-1789397743` completed propose, assess, challenge, and finalize with `MAJORITY_AGREE`; canonical readback is `FINAL / HTTP` with three stored digests. Exact transaction hashes are in `evidence/network-run.json`.

Published six-page application: https://samiinw-signal-tribunal.pages.dev/

Run `python -m pytest case_tests -q` and `genvm-lint tribunal_core/signal_tribunal.py`. Serve `docket_app/` (or `docs/`) over HTTP and open `index.html`; every route works as an independent page. Clerk tools and full propose, assess, challenge, finalize proof live beside the public docket evidence.
