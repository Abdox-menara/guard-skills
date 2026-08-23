# Skill Examples

from skill_system import Skill, SkillRegistry


def sql_gen(ctx):
    table = ctx.get("table", "users")
    cols = ", ".join(ctx.get("columns", ["id", "name"]))
    conds = ctx.get("conditions", {})
    sql = f"SELECT {cols} FROM {table}"
    if conds:
        sql += " WHERE " + " AND ".join(f"{k} = ?" for k in conds)
    return {"sql": sql, "params": list(conds.values())}


def test_gen(ctx):
    func = ctx.get("function_name", "func")
    tests = f"def test_{func}():\n    assert {func}() is not None\n"
    return {"tests": tests, "coverage": 75.0}


def code_review(ctx):
    code = ctx.get("code", "")
    issues = []
    if "eval(" in code: issues.append("Security: eval()")
    if "exec(" in code: issues.append("Security: exec()")
    score = max(0, 100 - len(issues) * 20)
    return {"issues": issues, "score": score}


sql_skill = Skill(name="sql_generator", description="Generate SQL", handler=sql_gen, tests=[lambda o: "sql" in o])
test_skill = Skill(name="test_generator", description="Generate tests", handler=test_gen, tests=[lambda o: "tests" in o])
review_skill = Skill(name="code_reviewer", description="Review code", handler=code_review, tests=[lambda o: "score" in o])


def register_all(reg):
    reg.register(sql_skill)
    reg.register(test_skill)
    reg.register(review_skill)


if __name__ == "__main__":
    print("Skill Examples Ready!")
    reg = SkillRegistry()
    register_all(reg)
    r1 = reg.execute("sql_generator", {"table": "orders", "columns": ["id", "total"]})
    print("SQL:", r1.output["sql"])
    r2 = reg.execute("code_reviewer", {"code": "eval(\"bad\")"})
    print("Review score:", r2.output["score"])

