from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


class TrainingRunInspectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.run_dir = Path(self.temporary.name)
        for name in ("results", "checkpoints", "specs"):
            (self.run_dir / name).mkdir()
        self.script = Path(__file__).with_name("inspect_training_run.py")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def inspect(self, *extra: str) -> tuple[int, dict[str, object]]:
        completed = subprocess.run([sys.executable, str(self.script), "--run-dir", str(self.run_dir), *extra], check=False, capture_output=True, text=True, encoding="utf-8")
        return completed.returncode, json.loads(completed.stdout)

    def test_complete_run_requires_main_chat_acceptance(self) -> None:
        fingerprint = "sha256:contract"
        (self.run_dir / "research-state.json").write_text(json.dumps({"status": "complete", "terminal_reason": "frozen test and report complete", "contract_fingerprint": fingerprint}), encoding="utf-8")
        (self.run_dir / "results" / "candidate.json").write_text('{"metric":1.0}', encoding="utf-8")
        (self.run_dir / "final-summary.json").write_text(json.dumps({"complete": True, "contract_fingerprint": fingerprint}), encoding="utf-8")
        code, payload = self.inspect()
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "complete")
        self.assertIn("main_chat", str(payload["recommended_action"]))

    def test_false_summary_is_not_complete(self) -> None:
        fingerprint = "sha256:contract"
        (self.run_dir / "research-state.json").write_text(json.dumps({"status": "complete", "terminal_reason": "done", "contract_fingerprint": fingerprint}), encoding="utf-8")
        (self.run_dir / "final-summary.json").write_text(json.dumps({"complete": False, "contract_fingerprint": fingerprint}), encoding="utf-8")
        _, payload = self.inspect()
        self.assertEqual(payload["status"], "attention")

    def test_batch_complete_is_not_final_complete(self) -> None:
        fingerprint = "sha256:contract"
        (self.run_dir / "research-state.json").write_text(json.dumps({"status": "batch_complete", "contract_fingerprint": fingerprint}), encoding="utf-8")
        (self.run_dir / "final-summary.json").write_text(json.dumps({"complete": True, "contract_fingerprint": fingerprint}), encoding="utf-8")
        _, payload = self.inspect()
        self.assertEqual(payload["status"], "batch_complete")
        self.assertIn("next_research_round", str(payload["recommended_action"]))

    def test_state_is_exposed_in_compact_heartbeat(self) -> None:
        (self.run_dir / "research-state.json").write_text(json.dumps({"phase": "screen", "current_candidate": "tcn-medium", "completed_candidates": 3, "planned_candidates": 9}), encoding="utf-8")
        _, payload = self.inspect("--pid", str(os.getpid()))
        self.assertEqual(payload["status"], "running")
        self.assertEqual(payload["phase"], "screen")
        self.assertEqual(payload["progress"], {"completed": 3, "planned": 9})

    def test_nonfinite_result_is_hard_invalid(self) -> None:
        (self.run_dir / "results" / "candidate.json").write_text('{"metric":NaN}', encoding="utf-8")
        code, payload = self.inspect()
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "invalid")

    def test_fatal_log_requests_attention(self) -> None:
        log = self.run_dir / "training.log"
        log.write_text("Traceback (most recent call last):\nRuntimeError: CUDA out of memory\n", encoding="utf-8")
        _, payload = self.inspect("--pid", str(os.getpid()), "--log", str(log))
        self.assertEqual(payload["status"], "attention")
        self.assertEqual(payload["fatal_signals"], ["traceback", "accelerator_oom"])

    def test_live_process_without_artifacts_stalls_after_grace(self) -> None:
        _, payload = self.inspect("--pid", str(os.getpid()), "--startup-grace-minutes", "-1")
        self.assertEqual(payload["status"], "stalled")
        self.assertIn("no_progress_artifact", str(payload["recommended_action"]))

    def test_state_heartbeat_does_not_hide_stale_training_artifact(self) -> None:
        result = self.run_dir / "results" / "old.json"
        result.write_text('{"metric":1.0}', encoding="utf-8")
        old = result.stat().st_mtime - 7200
        os.utime(result, (old, old))
        (self.run_dir / "research-state.json").write_text(json.dumps({"status": "running", "last_heartbeat_at": "now"}), encoding="utf-8")
        _, payload = self.inspect("--pid", str(os.getpid()), "--stale-minutes", "60")
        self.assertEqual(payload["status"], "stalled")

    def test_explicit_start_time_prevents_old_directory_false_stall(self) -> None:
        old = self.run_dir.stat().st_mtime - 7200
        os.utime(self.run_dir, (old, old))
        started_at = datetime.now(timezone.utc).isoformat()
        _, payload = self.inspect("--pid", str(os.getpid()), "--started-at", started_at)
        self.assertEqual(payload["status"], "running")
        self.assertEqual(payload["startup_time_source"], "argument_or_state")

    def test_accelerator_status_reports_freshness(self) -> None:
        status_file = self.run_dir / "accelerator.json"
        status_file.write_text('{"gpu_utilization":42}', encoding="utf-8")
        _, payload = self.inspect("--pid", str(os.getpid()), "--accelerator-status-file", str(status_file))
        self.assertEqual(payload["accelerator_status"], {"gpu_utilization": 42})
        self.assertIsNotNone(payload["accelerator_status_age_seconds"])

    def test_batch_complete_with_wrong_fingerprint_requests_attention(self) -> None:
        (self.run_dir / "research-state.json").write_text(json.dumps({"status": "batch_complete", "contract_fingerprint": "sha256:new"}), encoding="utf-8")
        (self.run_dir / "final-summary.json").write_text(json.dumps({"complete": True, "contract_fingerprint": "sha256:old"}), encoding="utf-8")
        _, payload = self.inspect()
        self.assertEqual(payload["status"], "attention")


if __name__ == "__main__":
    unittest.main()
