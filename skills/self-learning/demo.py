from self_learning_engine import (
    init_learning_db, log_action, detect_pattern, get_best_strategy,
    learn_from_mistake, amplify_success, predict_next_action,
    predict_success_probability, get_performance_stats, get_improvement_recommendations,
    improve, get_learning_curve
)
import json

def demo():
    print("=" * 60)
    print("SELF-LEARNING ENGINE - DEMONSTRATION")
    print("=" * 60)
    
    db = init_learning_db()
    print(f"\n[INIT] Knowledge base initialized: {len(db)} fields")
    
    print("\n--- Logging Actions ---")
    log_action("click_button", {"target": "submit"}, True, context="form_submission")
    log_action("type_text", {"field": "email", "length": 25}, True, context="form_input")
    log_action("navigate", {"url": "/dashboard"}, True, context="page_load")
    log_action("click_button", {"target": "submit"}, False, context="form_submission")
    log_action("click_button", {"target": "submit"}, True, context="form_submission")
    print("[OK] 5 actions logged")
    
    print("\n--- Pattern Detection ---")
    pattern = detect_pattern("click_button", "form_submission")
    print(f"[OK] Pattern detected: {pattern['count']} occurrences, success rate: {pattern['success_rate']:.2f}")
    
    print("\n--- Best Strategy ---")
    strategy = get_best_strategy("click_button")
    if strategy:
        print(f"[OK] Best strategy for 'click_button': {strategy[0]} (success: {strategy[1]['success_rate']:.2f})")
    
    print("\n--- Learning from Mistakes ---")
    lesson = learn_from_mistake("click_button", "element_not_found", "wait_and_retry", context="form_submission")
    print(f"[OK] Learned from mistake: {lesson['error']} -> {lesson['correction']}")
    
    print("\n--- Amplifying Success ---")
    success = amplify_success("click_button", "form_submission", True, performance_metrics={"accuracy": 0.95, "speed": 0.8})
    print(f"[OK] Success amplified: score {success['success_score']:.2f}")
    
    print("\n--- Predictions ---")
    next_action = predict_next_action("click_button")
    if next_action:
        print(f"[OK] Predicted next action after 'click_button': {next_action[0]} (confidence: {next_action[1]})")
    
    prob = predict_success_probability("click_button", "form_submission")
    print(f"[OK] Success probability for 'click_button' in 'form_submission': {prob:.2f}")
    
    print("\n--- Performance Stats ---")
    stats = get_performance_stats()
    print(f"[OK] Total actions: {stats['total_actions']}")
    print(f"     Success rate: {stats['success_rate']:.2%}")
    print(f"     Patterns learned: {stats['patterns_learned']}")
    print(f"     Knowledge graph nodes: {stats['knowledge_graph_nodes']}")
    
    print("\n--- Improvement Recommendations ---")
    recs = get_improvement_recommendations()
    print(f"[OK] Found {len(recs)} recommendations")
    for r in recs[:3]:
        print(f"     - [{r['priority']}] {r['suggestion']}")
    
    print("\n--- Learning Curve ---")
    curve = get_learning_curve()
    if curve:
        print(f"[OK] Learning curve data points: {len(curve)}")
    else:
        print("[--] Not enough data for learning curve (need 10+ actions)")
    
    print("\n--- Full Improvement Cycle ---")
    improvement = improve()
    print(f"[OK] Improvement cycle complete")
    print(f"     Weak areas: {len(improvement['weak_areas'])}")
    print(f"     Strong areas: {len(improvement['strong_areas'])}")
    print(f"     Improvements suggested: {len(improvement['improvements'])}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Knowledge base saved")
    print("=" * 60)

if __name__ == "__main__":
    demo()
