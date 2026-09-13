"""Append-only skill-usage analytics hook. Usage: python tools/skill_usage_hook.py <skill> <event>."""
import csv
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "skills", "skills_usage.csv")


def main():
    if len(sys.argv) < 3:
        print("usage: python tools/skill_usage_hook.py <skill-name> <event>")
        sys.exit(2)
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["ts", "skill", "event"])
        w.writerow([datetime.now(timezone.utc).isoformat(), sys.argv[1], sys.argv[2]])
    print(f"logged {sys.argv[1]}:{sys.argv[2]}")


if __name__ == "__main__":
    main()
