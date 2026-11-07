# Research state schema

Persist a `research-state.json` file atomically. It is the source of truth for resumption and reporting, not a substitute for raw artifacts.

Minimum shape:

```json
{
  "schema_version": 1,
  "research_id": "stable-id",
  "mode": "continuous",
  "phase": "screen",
  "status": "running",
  "contract_fingerprint": "sha256:...",
  "run_directory": "...",
  "started_at": "ISO-8601",
  "current_round": 2,
  "current_candidate": "model-medium-seed0",
  "planned_candidates": 20,
  "completed_candidates": 7,
  "best_development_candidate": "model-small-seed0",
  "test_locked": true,
  "last_artifact_at": "ISO-8601",
  "last_heartbeat_at": "ISO-8601",
  "next_check_at": "ISO-8601",
  "repair_attempts": {},
  "terminal_reason": null
}
```

Allowed active statuses: `preparing`, `running`, `attention`, `stalled`, `batch_complete`, `repairing`. Allowed terminal statuses: `complete`, `converged`, `budget_stop`, `needs_new_data`, `blocked`, `user_stop`, `invalid`.

Validate that counts are non-negative, completed does not exceed planned, test remains locked before `frozen_test`, fingerprints are non-empty, and terminal states include a reason. Write via temporary file plus atomic replace. Preserve a transition log with previous/new phase, previous/new status, timestamp, reason and evidence path.
