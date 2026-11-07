# Bounded recovery and resume

Read after the monitor reports `attention`, `stalled`, `stopped` or `invalid`.

## State classification

- `running`: process alive and artifacts progressing; wait.
- `batch_complete`: one planned batch finished; run L3 acceptance, then choose the next research round or a terminal state.
- `attention`: fatal signal or suspicious artifact; inspect limited evidence.
- `stalled`: process alive but artifacts exceed the declared stale threshold; inspect accelerator, child process and latest candidate before intervening.
- `stopped`: process exited without completion; preserve evidence and determine resumability.
- `invalid`: corrupt/non-finite artifacts, fingerprint conflict, data leakage or contract violation; hard stop.
- `idle`: no process and no completion evidence; do not imply training is active.

## Safe automatic actions

When the experiment contract is unchanged, automation may:

- resume the same command in the same run directory and skip fingerprint-matching completed candidates;
- rerun only a candidate lacking an atomic completion artifact;
- quarantine incomplete/corrupt artifacts with a timestamp rather than deleting them;
- clean an orphan process only after proving it belongs to this run;
- rebuild an isolated, locked training environment without changing the research environment contract.

Do not silently change data, split, sample filtering, metrics, model capacity, batch size, learning rate, seeds or test-set access. Those are new experiments with new fingerprints.

## Repair record and retry bound

For every repair write: timestamp, failure signature, affected candidate, evidence, action, fingerprint effect, retry number and verification result. Allow at most two automatic retries for one normalized failure signature. On the third recurrence, stop that branch and report it; continue independent branches only if the failure is proven local.

Typical diagnoses:

- OOM: first rule out leaked tensors, stale processes and missing candidate isolation; a smaller batch is a new configuration.
- NaN/Inf: stop the branch and inspect data, transforms, learning rate, loss and gradients; never filter the result only at aggregation.
- Native crash: isolate candidates in subprocesses and retain the last atomic artifact.
- Interrupted run: verify the last complete artifact and checkpoint before resuming; never trust a filename alone.
- Code/config change: invalidate silent reuse unless the full fingerprint still matches.

Three consecutive turns with the same external blocker and no safe progress may be marked blocked. Slowness alone is not blockage.
