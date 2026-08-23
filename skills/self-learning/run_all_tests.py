import subprocess, sys, os, re

base = os.path.dirname(__file__)
test_files = ["test_engine.py", "test_v4.py", "test_v5.py", "test_advanced.py"]
total_passed = 0
total_failed = 0

for tf in test_files:
    print(f"\n{'='*60}")
    print(f"  RUNNING: {tf}")
    print(f"{'='*60}")
    r = subprocess.run([sys.executable, os.path.join(base, tf)], capture_output=True, text=True)
    passed = failed = 0
    for line in r.stdout.split("\n"):
        if "TOTAL:" in line:
            nums = re.findall(r"(\d+)\s+passed", line)
            if nums:
                passed = int(nums[0])
            nums = re.findall(r"(\d+)\s+failed", line)
            if nums:
                failed = int(nums[0])
            print(f"  -> {passed} passed, {failed} failed")
        elif "[PASS]" in line or "[FAIL]" in line:
            pass
        else:
            stripped = line.strip()
            if stripped:
                print(line)
    total_passed += passed
    total_failed += failed

print(f"\n{'='*60}")
print(f"  GRAND TOTAL: {total_passed} passed, {total_failed} failed")
print(f"{'='*60}")
sys.exit(1 if total_failed > 0 else 0)
