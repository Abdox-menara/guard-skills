"""Fuzzy-find skills by name/description/trigger. Usage: python tools/skill_search.py <query>."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "skills_index.json")


def main():
    if len(sys.argv) < 2:
        print("usage: python tools/skill_search.py <query>")
        sys.exit(2)
    q = " ".join(sys.argv[1:]).lower()
    idx = json.load(open(IDX, encoding="utf-8"))["index"]
    hits = []
    for cat, items in idx.items():
        for it in items:
            score = 0
            if q in it["name"].lower():
                score += 3
            if q in (it.get("desc") or "").lower():
                score += 1
            if score:
                hits.append((score, cat, it["name"], it.get("desc", "")))
    hits.sort(reverse=True)
    for score, cat, name, desc in hits[:15]:
        print(f"[{score}] {cat}/{name} — {desc}")
    if not hits:
        print("no matches")


if __name__ == "__main__":
    main()
