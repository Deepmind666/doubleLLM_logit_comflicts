import subprocess
import sys


CASES = [
    ["python", "-m", "unittest", "tests.test_stage2_cases_unittest", "-v"],
]


def run_case(cmd):
    print(f"\n[RUN] {' '.join(cmd)}")
    p = subprocess.run(cmd)
    if p.returncode != 0:
        print(f"[FAIL] return code = {p.returncode}")
        return False
    print("[PASS]")
    return True


def main():
    ok = True
    for cmd in CASES:
        ok = run_case(cmd) and ok
    if not ok:
        sys.exit(1)
    print("\nAll test cases passed.")


if __name__ == "__main__":
    main()

