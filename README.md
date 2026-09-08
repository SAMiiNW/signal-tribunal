# Signal Tribunal

Signal Tribunal adds a real challenge window to source-bound event resolution. A provisional answer is not final: any participant can attach a third, independently hosted record, forcing a fresh validator-reviewed ruling over all evidence.

The contract normalizes IDs, binds content digests, restricts answers to declared choices, verifies stored finding codes and rejects source-host reuse. Unchallenged resolutions become permissionlessly final after the deadline; challenged cases can be finalized immediately after the new review.

## Public interface

The public application is deliberately split into focused routes instead of one long dashboard:

- `index.html` — orientation and task selection
- `file.html` — create a source-bound proposal
- `review.html` — request assessment or finalize an eligible case
- `challenge.html` — lodge an independent third-source challenge
- `lookup.html` — read canonical contract state without a wallet
- `guide.html` — plain-language lifecycle and safety rules

Each write screen distinguishes wallet approval, transaction submission, and validator finalization. The lookup screen renders live contract data; the example ID is labelled as an example and is not used as hidden application state.

Run `python -m pytest case_tests -q` and `genvm-lint tribunal_core/signal_tribunal.py`. Serve `docket_app/` (or `docs/`) over HTTP and open `index.html`; every route works as an independent page. Clerk tools and full propose, assess, challenge, finalize proof live beside the public docket evidence.
