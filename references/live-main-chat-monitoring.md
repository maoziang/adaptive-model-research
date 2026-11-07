# Live monitoring in the current main chat

Read this whenever a formal or long-running training job is started or monitored.

## Non-negotiable hosting rule

The training process must remain attached to an observable execution session owned by the **current main chat**. Do not host it with hidden windows, `Start-Process`, scheduled tasks, `nohup`, a detached shell, another chat, a background agent, or an automation that can finish without returning here.

“Low token usage” means passive waiting between sparse evidence checks. It does **not** mean moving responsibility away from the main chat. The main chat remains active until training, bounded repair, research decisions, acceptance and the final report reach a terminal state.

Keep the execution session ID or PID, command, run directory and log path. The user must be able to ask for status and receive evidence from that same run.

## Cadence

1. Immediately report the command scope, run identity, expected duration range and what counts as completion.
2. Check after roughly 5–10 minutes to confirm process health, accelerator use and the first valid artifact.
3. Once stable, passively wait and check about every 30 minutes by default. If the user requests another interval, use it.
4. After a repair, recheck within 5–10 minutes, then return to the normal cadence.
5. Report key milestones immediately even if the next heartbeat is not due.

Use the product’s attached-session wait or poll mechanism. Never busy-loop and never perform per-epoch language-model analysis.

## Compact heartbeat

Run the included inspector when the run layout is compatible:

```powershell
python scripts/inspect_training_run.py --run-dir <run> --pid <pid> --started-at <ISO-8601> --log <log> --accelerator-status-file <optional-json>
```

Each visible heartbeat should fit in a few lines and state:

- current research phase and current candidate;
- completed/total candidates or the best available progress measure;
- process/accelerator health and newest artifact age;
- last completed milestone and next expected check time;
- only if needed, the problem and action being taken.

Do not reread full logs while status is healthy. Use four evidence levels:

- **L0 heartbeat**: one compact JSON/status record.
- **L1 anomaly triage**: last 100–200 log lines, latest candidate result and specification.
- **L2 repair analysis**: relevant code, data statistics, checkpoint and full curve only after a real fault is established.
- **L3 acceptance**: full results only when a batch completes or a quality gate fails.

## Events that require immediate visible reporting

- attached run started and first artifact verified;
- candidate, stage or research round completed;
- anomaly detected, diagnostic conclusion, repair action and recovery confirmation;
- experiment-contract or fingerprint change;
- transition from a completed batch to the next hypothesis round;
- terminal state and final report.

The process ending is not the same as the work finishing. The main chat must perform acceptance and proactively deliver the final report.

The inspector treats `research-state.json` as orchestration state, not training progress. Updating a heartbeat therefore cannot hide stale results or checkpoints. Final `complete` requires a matching contract fingerprint, an explicit terminal reason, and a completion artifact whose `complete` field is true; `batch_complete` remains a separate state.

Provide `--started-at` or persist `started_at` in `research-state.json` when reusing an old run directory; directory modification time is only a compatibility fallback. Accelerator status is optional and includes its age so a stale GPU snapshot cannot be presented as current health.
