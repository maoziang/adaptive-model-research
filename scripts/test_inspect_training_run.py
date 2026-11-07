from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
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
        (self.run_dir / "results" / "candidate.json").write_text('{"metric":1.0}', encoding="utf-8")
        (self.run_dir / "final-summary.json").write_text('{"complete":true}', encoding="utf-8")
        code, payload = self.inspect()
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "complete")
        self.assertIn("main_chat", str(payload["recommended_action"]))

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


if __name__ == "__main__":
    unittest.main()
