"""Find near-duplicate / overlapping skill clusters.
Similarity: name token overlap + description trigram Jaccard.
Output: console report + tools/dedupe_report.json
"""

import os
import re
import json
from difflib import SequenceMatcher

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")


def load_skills():
    out = []
    for cat in ("guards", "tools", "workflow"):
        base = os.path.join(SKILLS, cat)
        for d in sorted(os.listdir(base)):
            sm = os.path.join(base, d, "SKILL.md")
            if os.path.isfile(sm):
                t = open(sm, encoding="utf-8", errors="replace").read()
                dm = re.search(r"^description:\s*\|?\s*\n?(.*?)(?=^\w+:|\Z)", t, re.S | re.M)
                desc = " ".join((dm.group(1) if dm else "").split())[:400]
                out.append({"cat": cat, "dir": d, "desc": desc})
    for name in ("desktop-control-mcp", "force-delete", "self-learning"):
        sm = os.path.join(SKILLS, name, "SKILL.md")
        if os.path.isfile(sm):
            t = open(sm, encoding="utf-8", errors="replace").read()
            dm = re.search(r"^description:\s*\|?\s*\n?(.*?)(?=^\w+:|\Z)", t, re.S | re.M)
            out.append({"cat": "special", "dir": name, "desc": " ".join((dm.group(1) if dm else "").split())[:400]})
    return out


def trigrams(s):
    s = re.sub(r"[^a-z0-9 ]", "", s.lower())
    return set(s[i : i + 3] for i in range(max(0, len(s) - 2)))


def jac(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    skills = load_skills()
    print(f"analyzing {len(skills)} skills...")
    pairs = []
    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            a, b = skills[i], skills[j]
            # quick prefix filter: same family names share long common prefix
            name_sim = SequenceMatcher(None, a["dir"], b["dir"]).ratio()
            if name_sim < 0.72:
                continue
            tg = jac(trigrams(a["desc"]), trigrams(b["desc"]))
            if tg > 0.45 or (name_sim > 0.85 and tg > 0.30):
                pairs.append(
                    {
                        "a": f"{a['cat']}/{a['dir']}",
                        "b": f"{b['cat']}/{b['dir']}",
                        "name_sim": round(name_sim, 2),
                        "desc_sim": round(tg, 2),
                    }
                )
    pairs.sort(key=lambda p: -p["desc_sim"])
    print(f"overlap clusters found: {len(pairs)}")
    for p in pairs[:20]:
        print(f"  {p['a']}  <->  {p['b']}   name:{p['name_sim']} desc:{p['desc_sim']}")
    json.dump(pairs, open(os.path.join(ROOT, "tools", "dedupe_report.json"), "w"), indent=1)
    print("report -> tools/dedupe_report.json")


if __name__ == "__main__":
    main()
