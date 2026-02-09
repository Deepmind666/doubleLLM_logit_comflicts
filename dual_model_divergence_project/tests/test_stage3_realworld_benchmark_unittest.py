import subprocess
import unittest
from pathlib import Path


class Stage3RealworldBenchmarkTests(unittest.TestCase):
    def test_realworld_benchmark_runs_and_generates_report(self):
        project_root = Path(__file__).resolve().parents[1]
        cmd = ["python", "experiments/run_realworld_benchmark.py"]
        proc = subprocess.run(cmd, cwd=str(project_root), capture_output=True, text=True)
        self.assertEqual(
            proc.returncode,
            0,
            msg=f"realworld benchmark failed.\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
        )

        report_file = project_root / "experiments" / "realworld_benchmark_report.md"
        self.assertTrue(report_file.exists(), "Expected realworld benchmark report to be generated.")
        text = report_file.read_text(encoding="utf-8")
        self.assertIn("Realworld Benchmark Report", text)
        self.assertIn("Layer Metrics", text)
        self.assertIn("Conflict Detection Error Analysis", text)


if __name__ == "__main__":
    unittest.main()
