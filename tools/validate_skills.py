"""Validate all SKILL.md files: frontmatter, description, relative links.
Usage: python tools/validate_skills.py   (exit 1 on hard failures)
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")

FENCE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
FRONT = re.compile(r"^---\s*\n(.*?)\n---", re.S)
LINK = re.compile(r"\]\(([^)#]+?)\)")


def check():
    no_front, no_desc, broken = [], [], []
    total = 0
    for r, d, fs in os.walk(SKILLS):
        if "__pycache__" in r:
            continue
        for f in fs:
            if f != "SKILL.md":
                continue
            total += 1
            p = os.path.join(r, f)
            try:
                raw = open(p, encoding="utf-8", errors="replace").read()
            except OSError as e:
                no_front.append((p, str(e)))
                continue
            m = FRONT.match(raw)
            if not m:
                no_front.append((p, "missing --- block"))
                continue
            fm = m.group(1)
            body_no_fence = FENCE.sub("", raw)
            dm = re.search(r"^description:\s*\|?\s*\n?(.*?)(?=^\w+:|\Z)", fm, re.S | re.M)
            desc_text = ""
            if dm:
                desc_text = " ".join(dm.group(1).split())
            if len(desc_text) < 10:
                no_desc.append(p)
            rel = os.path.relpath(p, SKILLS).replace("\\", "/")
            for ref in LINK.findall(FENCE.sub("", body_no_fence)):
                target = ref.strip().replace("%20", " ")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if "*" in target or "<" in target or " " in target and not target.endswith(".md"):
                    continue
                full = os.path.normpath(os.path.join(os.path.dirname(p), target))
                if target.endswith(".md") and not os.path.exists(full):
                    broken.append((rel, target))
    return total, no_front, no_desc, broken


def main():
    total, no_front, no_desc, broken = check()
    print(f"validated: {total} SKILL.md")
    print(f"no_frontmatter: {len(no_front)}")
    for p, why in no_front[:5]:
        print(f"   {p} -> {why}")
    print(f"weak_description: {len(no_desc)}")
    for p in no_desc[:5]:
        print(f"   {p}")
    print(f"broken_md_links: {len(broken)}")
    for p, t in broken[:8]:
        print(f"   {p} -> {t}")
    hard = len(no_front) + len(broken)
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
