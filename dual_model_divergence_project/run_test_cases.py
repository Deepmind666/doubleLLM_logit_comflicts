import subprocess
import sys


CASES = [
    ["python", "-m", "unittest", "tests.test_basic_flow", "-v"],
    ["python", "-m", "unittest", "tests.test_stage2_cases_unittest", "-v"],
    ["python", "-m", "unittest", "tests.test_stage3_realworld_benchmark_unittest", "-v"],
    ["python", "experiments/run_benchmark.py"],
    ["python", "experiments/run_realworld_benchmark.py"],
]


def run_case(cmd):
    print(f"\n[RUN] {' '.join(cmd)}", flush=True)
    p = subprocess.run(cmd)
    if p.returncode != 0:
        print(f"[FAIL] return code = {p.returncode}", flush=True)
        return False
    print("[PASS]", flush=True)
    return True


def main():
    ok = True
    for cmd in CASES:
        ok = run_case(cmd) and ok
    if not ok:
        sys.exit(1)
    print("\nAll test cases passed.", flush=True)


if __name__ == "__main__":
    main()
