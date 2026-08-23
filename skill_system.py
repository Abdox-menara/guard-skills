import json, time
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

class SkillStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class SkillResult:
    status: SkillStatus
    output: Any = None
    error: Optional[str] = None
    tests_passed: int = 0
    tests_failed: int = 0
    duration_ms: float = 0

@dataclass
class Skill:
    name: str
    description: str
    handler: Optional[Callable] = None
    tests: List[Callable] = field(default_factory=list)

    def execute(self, ctx):
        start = time.time()
        try:
            if not self.handler:
                return SkillResult(SkillStatus.FAILED, error="No handler")
            out = self.handler(ctx)
            p, f2 = self._run_tests(out)
            st = SkillStatus.SUCCESS if f2 == 0 else SkillStatus.FAILED
            return SkillResult(st, out, tests_passed=p, tests_failed=f2, duration_ms=round((time.time()-start)*1000,2))
        except Exception as e:
            return SkillResult(SkillStatus.FAILED, error=str(e))

    def _run_tests(self, out):
        p, f2 = 0, 0
        for t in self.tests:
            try:
                if t(out): p += 1
                else: f2 += 1
            except: f2 += 1
        return p, f2

class SkillRegistry:
    def __init__(self):
        self.skills = {}
    def register(self, skill):
        self.skills[skill.name] = skill
    def execute(self, name, ctx):
        if name not in self.skills:
            return SkillResult(SkillStatus.FAILED, error=f"Skill {name} not found")
        return self.skills[name].execute(ctx)

if __name__ == "__main__":
    print("Skill System Ready!")
