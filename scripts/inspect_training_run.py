#!/usr/bin/env python3
"""Emit one compact, read-only health record for a model-training run."""

from __future__ import annotations

import argparse
import ctypes
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

FATAL_PATTERNS = {
    "traceback": re.compile(r"Traceback \(most recent call last\):", re.I),
    "accelerator_oom": re.compile(r"(?:CUDA|MPS|XPU).*out of memory|CUBLAS_STATUS_ALLOC_FAILED", re.I),
    "fatal_runtime": re.compile(r"Fatal Python error|segmentation fault", re.I),
    "native_crash": re.compile(r"0xC0000005|access violation", re.I),
    "nonfinite_training": re.compile(r"(?:loss|metric|gradient)[^\r\n]{0,48}(?:nan|\+?inf|-inf)", re.I),
}


def process_alive(pid: Optional[int]) -> Optional[bool]:
    if pid is None:
        return None
    if pid <= 0:
        return False
    if os.name == "nt":
        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)  # type: ignore[attr-defined]
        if not handle:
            return False
        ctypes.windll.kernel32.CloseHandle(handle)  # type: ignore[attr-defined]
        return True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def contains_nonfinite(value: Any) -> bool:
    if isinstance(value, float):
        return not math.isfinite(value)
    if isinstance(value, dict):
        return any(contains_nonfinite(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_nonfinite(item) for item in value)
    return False


def inspect_json(paths: Iterable[Path]) -> tuple[list[str], list[str]]:
    invalid, nonfinite = [], []
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            invalid.append(path.name)
            continue
        if contains_nonfinite(payload):
            nonfinite.append(path.name)
    return invalid, nonfinite


def read_state(path: Path) -> tuple[dict[str, Any], Optional[str]]:
    if not path.is_file():
        return {}, None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}, "invalid_research_state"
    if not isinstance(payload, dict):
        return {}, "invalid_research_state"
    return payload, None


def read_json_object(path: Path) -> tuple[dict[str, Any], Optional[str]]:
    if not path.is_file():
        return {}, "missing"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}, "invalid"
    if not isinstance(payload, dict):
        return {}, "invalid"
    return payload, None


def log_signals(path: Optional[Path], tail_bytes: int) -> list[str]:
    if path is None or not path.is_file():
        return []
    with path.open("rb") as source:
        source.seek(0, os.SEEK_END)
        source.seek(max(0, source.tell() - tail_bytes))
        tail = source.read().decode("utf-8", errors="replace")
    return [name for name, pattern in FATAL_PATTERNS.items() if pattern.search(tail)]


def newest_age_minutes(paths: list[Path]) -> Optional[float]:
    if not paths:
        return None
    newest = max(path.stat().st_mtime for path in paths)
    return round(max(0.0, datetime.now(timezone.utc).timestamp() - newest) / 60.0, 2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--pid", type=int)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--stale-minutes", type=float, default=75.0)
    parser.add_argument("--startup-grace-minutes", type=float, default=10.0)
    parser.add_argument("--tail-bytes", type=int, default=131_072)
    parser.add_argument("--completion-files", default="final-summary.json")
    parser.add_argument("--accelerator-status-file", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    if not run_dir.is_dir():
        print(json.dumps({"schema_version": 1, "status": "invalid", "recommended_action": "verify_run_directory", "run_dir": str(run_dir)}, separators=(",", ":")))
        return 2

    result_paths = sorted((run_dir / "results").glob("*.json"))
    checkpoint_paths = sorted((run_dir / "checkpoints").glob("*")) if (run_dir / "checkpoints").is_dir() else []
    spec_paths = sorted((run_dir / "specs").glob("*.json"))
    summary_paths = sorted(run_dir.glob("*summary.json"))
    state_path = run_dir / "research-state.json"
    state, state_error = read_state(state_path)
    invalid_json, nonfinite_json = inspect_json(result_paths + spec_paths + summary_paths)
    if state_error:
        invalid_json.append(state_path.name)
    completion_files = [run_dir / item.strip() for item in args.completion_files.split(",") if item.strip()]
    completion_payloads = [read_json_object(path) for path in completion_files]
    completion_present = all(error is None for _, error in completion_payloads)
    completion_declared = completion_present and all(payload.get("complete") is True for payload, _ in completion_payloads)
    fingerprints = {payload.get("contract_fingerprint") for payload, _ in completion_payloads}
    state_fingerprint = state.get("contract_fingerprint")
    fingerprint_matches = bool(state_fingerprint) and fingerprints == {state_fingerprint}
    state_status = state.get("status")
    state_terminal_reason = state.get("terminal_reason")
    progress_artifacts = result_paths + checkpoint_paths + spec_paths + summary_paths
    age_minutes = newest_age_minutes(progress_artifacts)
    run_age_minutes = round(max(0.0, datetime.now(timezone.utc).timestamp() - run_dir.stat().st_mtime) / 60.0, 2)
    alive = process_alive(args.pid)
    signals = log_signals(args.log, max(1024, args.tail_bytes))

    accelerator_status: Any = None
    if args.accelerator_status_file and args.accelerator_status_file.is_file():
        try:
            accelerator_status = json.loads(args.accelerator_status_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            accelerator_status = args.accelerator_status_file.read_text(encoding="utf-8", errors="replace").strip()[:512]

    if invalid_json or nonfinite_json:
        status, action = "invalid", "inspect_corrupt_or_nonfinite_artifacts"
    elif state_status == "batch_complete":
        status, action = "batch_complete", "run_level_3_audit_then_choose_next_research_round"
    elif completion_declared and state_status == "complete" and state_terminal_reason and fingerprint_matches:
        status, action = "complete", "run_full_acceptance_and_report_in_main_chat"
    elif completion_present:
        status, action = "attention", "verify_completion_state_reason_and_fingerprint"
    elif signals:
        status, action = "attention", "read_log_tail_and_latest_candidate"
    elif alive is False:
        status, action = "stopped", "inspect_last_atomic_artifact_then_resume"
    elif alive is True and age_minutes is None and run_age_minutes > args.startup_grace_minutes:
        status, action = "stalled", "no_progress_artifact_after_startup_grace"
    elif alive is True and age_minutes is not None and age_minutes > args.stale_minutes:
        status, action = "stalled", "check_accelerator_child_process_and_latest_candidate"
    elif alive is True:
        status, action = "running", "wait_for_next_30_minute_heartbeat"
    else:
        status, action = "idle", "provide_attached_session_pid_or_confirm_not_started"

    record = {
        "schema_version": 1,
        "status": status,
        "recommended_action": action,
        "process_alive": alive,
        "accelerator_status": accelerator_status,
        "phase": state.get("phase"),
        "current_candidate": state.get("current_candidate"),
        "progress": {"completed": state.get("completed_candidates", len(result_paths)), "planned": state.get("planned_candidates")},
        "newest_artifact_age_minutes": age_minutes,
        "counts": {"results": len(result_paths), "checkpoints": len(checkpoint_paths), "specs": len(spec_paths), "summaries": len(summary_paths)},
        "completion_present": completion_present,
        "completion_declared": completion_declared,
        "completion_fingerprint_matches": fingerprint_matches,
        "invalid_json": invalid_json,
        "nonfinite_json": nonfinite_json,
        "fatal_signals": signals,
    }
    print(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
    return 2 if status == "invalid" else 0


if __name__ == "__main__":
    sys.exit(main())
