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

Current StudioNet contract: [`0xCc2360351758b16E79A475C257Fb3160490b8CdD`](https://explorer-studio.genlayer.com/address/0xCc2360351758b16E79A475C257Fb3160490b8CdD). Fresh case `ST-1789397743` completed propose, assess, challenge, and finalize with `MAJORITY_AGREE`; canonical readback is `FINAL / HTTP` with three stored digests.

| Lifecycle record | Verified receipt |
| --- | --- |
| Deployment | [`0x0049…1308`](https://explorer-studio.genlayer.com/transactions/0x0049a3f0f9276ef92d77a753dd17ddd48c461baa400bf1d082b44ee6946f1308) — `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| Propose | [`0x0f85…42af`](https://explorer-studio.genlayer.com/transactions/0x0f858040d6b73125aae3fe68f11de5a89dd3a286bc0ba55b27d0b2b8aea242af) — `FINALIZED / MAJORITY_AGREE`, recorded leader executions `SUCCESS, ERROR`; later lifecycle readback proves the proposal persisted |
| Assess | [`0x7524…a767`](https://explorer-studio.genlayer.com/transactions/0x7524ffac1f0a8d71b8d3d0bb34818cc4905f30f6dee6e91049670c3475fea767) — `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| Challenge | [`0x2eed…c35e`](https://explorer-studio.genlayer.com/transactions/0x2eed68cff9d5ea99e334fe67ddf090cf8da49a70c9a8feee10a36dc54881c35e) — `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| Finalize | [`0xbf07…29d7`](https://explorer-studio.genlayer.com/transactions/0xbf07a81ec974395534d38ad1e6dd5162ead72af5dd5468ab1a7b8cb3847629d7) — `FINALIZED / MAJORITY_AGREE / SUCCESS` |

Canonical six-page application in the currently authorized Cloudflare account: https://signal-tribunal-asu.pages.dev/

Run `python -m pytest case_tests -q` and `genvm-lint tribunal_core/signal_tribunal.py`. Serve `docket_app/` (or `docs/`) over HTTP and open `index.html`; every route works as an independent page. Clerk tools and full propose, assess, challenge, finalize proof live beside the public docket evidence.
