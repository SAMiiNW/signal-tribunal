# Signal Tribunal

Signal Tribunal adds a real challenge window to source-bound event resolution. A provisional answer is not final: any participant can attach a third, independently hosted record, forcing a fresh validator-reviewed ruling over all evidence.

The contract normalizes IDs, binds content digests, restricts answers to declared choices, verifies stored finding codes and rejects source-host reuse. Unchallenged resolutions become permissionlessly final after the deadline; challenged cases can be finalized immediately after the new review.

Run `python -m pytest -q` and `genvm-lint contract/signal_tribunal.py`. Deployment and full propose, assess, challenge, finalize proof live in `evidence/`.
