import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from self_learning_engine import *
import json
import time

class TestResult:
    def __init__(self, name):
        self.name = name
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def check(self, condition, msg=""):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(msg)
    
    def report(self):
        status = "PASS" if self.failed == 0 else "FAIL"
        print(f"  [{status}] {self.name}: {self.passed} passed, {self.failed} failed")
        for err in self.errors:
            print(f"         - {err}")

def test_init():
    t = TestResult("Initialization")
    db = init_learning_db()
    t.check(db is not None, "DB is None")
    t.check("version" in db, "Missing version")
    t.check("action_history" in db, "Missing action_history")
    t.check("patterns" in db, "Missing patterns")
    t.check("knowledge_graph" in db, "Missing knowledge_graph")
    t.check(db["version"] == "3.0", f"Wrong version: {db['version']}")
    return t

def test_log_action():
    t = TestResult("Log Action")
    db = init_learning_db()
    initial_count = db["total_actions"]
    
    entry = log_action("test_action", {"key": "value"}, True, context="test")
    t.check(entry is not None, "Entry is None")
    t.check(entry["type"] == "test_action", "Wrong type")
    t.check(entry["success"] == True, "Wrong success")
    t.check(entry["context"] == "test", "Wrong context")
    
    db = load_db()
    t.check(db["total_actions"] == initial_count + 1, "Count not incremented")
    t.check(db["successful_actions"] > 0, "Success not tracked")
    
    log_action("fail_action", {}, False)
    db = load_db()
    t.check(db["failed_actions"] > 0, "Failure not tracked")
    return t

def test_pattern_detection():
    t = TestResult("Pattern Detection")
    
    for _ in range(5):
        detect_pattern("multi_click", "context_a")
    
    pattern = detect_pattern("multi_click", "context_a")
    t.check(pattern["count"] >= 5, f"Count too low: {pattern['count']}")
    t.check(pattern["success_rate"] > 0, "Success rate is 0")
    t.check("embedding" in pattern, "Missing embedding")
    
    unique_key = f"unique_{int(time.time())}"
    pattern2 = detect_pattern(unique_key, "unique_context")
    t.check(pattern2["count"] >= 1, "New pattern count wrong")
    return t

def test_strategy():
    t = TestResult("Best Strategy")
    
    for _ in range(3):
        detect_pattern("strat_test", "ctx1")
    
    strategy = get_best_strategy("strat_test")
    t.check(strategy is not None, "Strategy is None")
    if strategy:
        t.check("strat_test" in strategy[0], "Wrong pattern key")
    return t

def test_error_learning():
    t = TestResult("Error Learning")
    
    lesson = learn_from_mistake("action_x", "timeout_error", "retry_with_delay")
    t.check(lesson is not None, "Lesson is None")
    t.check(lesson["error"] == "timeout_error", "Wrong error")
    t.check(lesson["correction"] == "retry_with_delay", "Wrong correction")
    t.check("analysis" in lesson, "Missing analysis")
    t.check(lesson["analysis"]["error_type"] == "timing", f"Wrong error type: {lesson['analysis']['error_type']}")
    
    db = load_db()
    t.check(len(db["mistakes"]) > 0, "Mistake not stored")
    t.check(len(db["learned_shortcuts"]) > 0, "Shortcut not created")
    return t

def test_success_amplification():
    t = TestResult("Success Amplification")
    
    success = amplify_success("test_action", "test_ctx", True, {"accuracy": 0.9, "speed": 0.8})
    t.check(success is not None, "Success is None")
    t.check(success["success_score"] > 0, "Score is 0")
    t.check(success["success_score"] <= 1.0, f"Score too high: {success['success_score']}")
    t.check(success["performance_metrics"]["accuracy"] == 0.9, "Metrics wrong")
    
    db = load_db()
    t.check(len(db["successes"]) > 0, "Success not stored")
    return t

def test_predictions():
    t = TestResult("Predictions")
    
    for i in range(10):
        log_action("predict_src", {"i": i}, i % 2 == 0)
        log_action("predict_dst", {"i": i}, True)
    
    prediction = predict_next_action("predict_src")
    t.check(prediction is not None, "Prediction is None")
    
    prob = predict_success_probability("predict_src", None)
    t.check(0 <= prob <= 1, f"Probability out of range: {prob}")
    return t

def test_knowledge_graph():
    t = TestResult("Knowledge Graph")
    
    update_knowledge_graph_with_error("err1", "fix1", None)
    update_knowledge_graph_with_success("act1", "ctx1", True)
    
    db = load_db()
    kg = db["knowledge_graph"]
    t.check(len(kg["nodes"]) > 0, "No nodes created")
    
    error_nodes = [n for n in kg["nodes"] if kg["nodes"][n]["type"] == "error"]
    t.check(len(error_nodes) > 0, "No error nodes")
    
    success_nodes = [n for n in kg["nodes"] if kg["nodes"][n]["type"] == "success"]
    t.check(len(success_nodes) > 0, "No success nodes")
    return t

def test_performance_stats():
    t = TestResult("Performance Stats")
    
    stats = get_performance_stats()
    t.check(stats is not None, "Stats is None")
    t.check("total_actions" in stats, "Missing total_actions")
    t.check("success_rate" in stats, "Missing success_rate")
    t.check("patterns_learned" in stats, "Missing patterns_learned")
    t.check("learning_velocity" in stats, "Missing learning_velocity")
    t.check(0 <= stats["success_rate"] <= 1, "Success rate out of range")
    return t

def test_improvement():
    t = TestResult("Improvement Cycle")
    
    result = improve()
    t.check(result is not None, "Result is None")
    t.check("stats" in result, "Missing stats")
    t.check("weak_areas" in result, "Missing weak_areas")
    t.check("strong_areas" in result, "Missing strong_areas")
    t.check("recommendations" in result, "Missing recommendations")
    return t

def test_learning_curve():
    t = TestResult("Learning Curve")
    
    for i in range(15):
        log_action("curve_action", {"i": i}, i % 3 != 0)
    
    curve = get_learning_curve()
    t.check(curve is not None, "Curve is None")
    t.check(len(curve) > 0, "Curve is empty")
    t.check("success_rate" in curve[0], "Missing success_rate in curve")
    return t

def test_recommendations():
    t = TestResult("Recommendations")
    
    recs = get_improvement_recommendations()
    t.check(recs is not None, "Recommendations is None")
    t.check(isinstance(recs, list), "Not a list")
    return t

def test_data_persistence():
    t = TestResult("Data Persistence")
    
    log_action("persist_test", {"data": 123}, True)
    db1 = load_db()
    count1 = db1["total_actions"]
    
    db2 = load_db()
    t.check(db2["total_actions"] == count1, "Data not persisted")
    return t

def test_history_limit():
    t = TestResult("History Limit")
    
    db = load_db()
    original_count = len(db["action_history"])
    
    for i in range(100):
        log_action("limit_test", {"i": i}, True)
    
    db = load_db()
    t.check(len(db["action_history"]) <= 10000, "History exceeds limit")
    return t

def run_all_tests():
    print("=" * 60)
    print("SELF-LEARNING ENGINE - TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_init(),
        test_log_action(),
        test_pattern_detection(),
        test_strategy(),
        test_error_learning(),
        test_success_amplification(),
        test_predictions(),
        test_knowledge_graph(),
        test_performance_stats(),
        test_improvement(),
        test_learning_curve(),
        test_recommendations(),
        test_data_persistence(),
        test_history_limit(),
    ]
    
    total_passed = 0
    total_failed = 0
    
    for test in tests:
        test.report()
        total_passed += test.passed
        total_failed += test.failed
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {total_passed} passed, {total_failed} failed")
    print("=" * 60)
    
    return total_failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
