"""
Self-Improvement Loop v1.0
Integrates with the self-learning engine for continuous learning.
Usage: python self_improve.py [mode]
  mode=interactive  - Full interactive Q&A learning loop
  mode=quick        - Quick test of all components
"""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(__file__))
from self_learning_engine import *
from datetime import datetime

LEARNING_DB = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')

class SelfImprovementLoop:
    def __init__(self):
        self.db = load_db()
        self.rl_agent = RLAgent(state_size=10, action_size=5)
        self.meta_learner = MetaLearner()
        self.knowledge_graph = KnowledgeGraph()
        self.emotional_intel = EmotionalIntelligence()
        self.bayesian = BayesianInference()
        self.nn = NeuralNetwork([10, 16, 8, 2])
        self.stats_history = []
        self.user_preferences = {}
        self.cycle_count = 0

    def log(self, action_type, details, success, context=None):
        entry = log_action(action_type, details, success, context)
        detect_pattern(action_type, context or "default")
        return entry

    def learn_from_result(self, action, error, correction, context=None, success=True):
        if not success:
            lesson = learn_from_mistake(action, error, correction, context)
            self.knowledge_graph.add_node(f"error_{action}", "error", {"action": action, "error": error})
            return lesson
        else:
            pattern = amplify_success(action, context, True)
            self.knowledge_graph.add_node(f"success_{action}", "success", {"action": action, "context": context})
            return pattern

    def ask_and_learn(self, question_text, category="general"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question_text,
            "category": category,
            "answer": None,
            "sentiment": None
        }
        self.db["action_history"].append({
            "type": f"ask_{category}",
            "details": {"question": question_text},
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "context": category
        })
        save_db(self.db)
        return entry

    def record_answer(self, category, answer, user_sentiment="neutral"):
        sentiment = self.emotional_intel.analyze_sentiment(answer)
        self.user_preferences[category] = {
            "answer": answer,
            "sentiment": sentiment["sentiment"],
            "score": sentiment["score"],
            "timestamp": datetime.now().isoformat()
        }
        self.db["user_preferences"] = self.user_preferences
        save_db(self.db)
        pattern_key = f"preference_{category}_{answer[:20]}"
        if pattern_key not in self.db["patterns"]:
            self.db["patterns"][pattern_key] = {
                "count": 1,
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "success_rate": 0.8,
                "embedding": hashlib.md5(pattern_key.encode()).hexdigest()[:16]
            }
        save_db(self.db)
        return sentiment

    def run_improvement_cycle(self):
        self.cycle_count += 1
        result = improve()
        self.stats_history.append(result["stats"])
        curve = get_learning_curve()
        recommendations = get_improvement_recommendations()

        if self.cycle_count % 3 == 0 and len(self.db["patterns"]) > 5:
            try:
                X = np.random.randn(max(10, len(self.db["patterns"])), 10)
                y = np.random.randint(0, 2, (max(10, len(self.db["patterns"])), 1))
                self.nn.train(X, y, epochs=5, learning_rate=0.01)
                self.db["neural_weights"] = {
                    "trained_at": datetime.now().isoformat(),
                    "patterns_count": len(self.db["patterns"]),
                    "cycle": self.cycle_count
                }
                save_db(self.db)
            except Exception as e:
                print(f"  [NN train skipped: {e}]")

        for key, pattern in result.get("strong_areas", {}).items():
            self.knowledge_graph.add_node(
                f"strength_{key[:16]}",
                "strength",
                {"pattern": key, "rate": pattern["success_rate"]}
            )

        return {"stats": result["stats"], "recommendations": recommendations, "curve": curve}

    def get_summary(self):
        stats = get_performance_stats()
        return f"""=== Self-Learning Status ===
Actions: {stats['total_actions']} | Success: {stats['success_rate']*100:.1f}% | Recent: {stats['recent_success_rate']*100:.1f}%
Patterns: {stats['patterns_learned']} | Mistakes Learned: {stats['mistakes_learned']}
Learning Velocity: {stats['learning_velocity']:.2f} patterns/hr
Knowledge Graph: {stats['knowledge_graph_nodes']} nodes, {stats['knowledge_graph_edges']} edges
Preferences Known: {len(self.user_preferences)} categories
Cycle: {self.cycle_count}
========================="""


if __name__ == "__main__":
    loop = SelfImprovementLoop()
    mode = sys.argv[1] if len(sys.argv) > 1 else "interactive"

    if mode == "quick":
        print("Quick test: Learning components")
        loop.log("test_component", {"component": "all"}, True, "init")
        result = loop.run_improvement_cycle()
        print(loop.get_summary())
        print(f"Recommendations: {len(result['recommendations'])}")
        print("Knowledge base saved to knowledge_base.json")

    elif mode == "interactive":
        print("\n" + "="*60)
        print("  SELF-IMPROVEMENT LOOP - Interactive Learning Mode")
        print("="*60)
        print("I will ask you questions and learn from your answers.")
        print("Type 'status' to see learning stats, 'cycle' to run improvement,")
        print("'quit' to exit, or just answer the questions.\n")

        topics = [
            ("communication", "How do you prefer I communicate with you? (concise/detailed/balanced)"),
            ("code_style", "What code style do you prefer? (pythonic/typed/functional)"),
            ("formatting", "Preferred output format? (markdown/plain/structured)"),
            ("depth", "How detailed should my explanations be? (brief/moderate/deep)"),
            ("proactivity", "Should I proactively suggest improvements or wait for instructions? (proactive/cautious)"),
            ("error_handling", "How should I handle errors? (verbose/silent/retry)"),
            ("creativity", "How creative should my solutions be? (conservative/balanced/creative)"),
            ("learning_focus", "What should I focus on learning most? (code/testing/docs/architecture)"),
            ("feedback_style", "How do you want feedback? (direct/diplomatic/praise-first)"),
            ("priority", "What's your top priority? (speed/quality/security/completeness)")
        ]

        topic_idx = 0
        while True:
            if topic_idx < len(topics):
                category, question_text = topics[topic_idx]
                print(f"\n[Q{topic_idx+1}] {question_text}")
                print("> ", end="")
                answer = input().strip()
                if answer.lower() == 'quit':
                    break
                elif answer.lower() == 'status':
                    print(loop.get_summary())
                    continue
                elif answer.lower() == 'cycle':
                    result = loop.run_improvement_cycle()
                    print("\n--- Improvement Cycle ---")
                    print(f"Weak patterns: {len(result['stats']['patterns_learned'])}")
                    print(f"Recommendations: {len(result['recommendations'])}")
                    for rec in result['recommendations']:
                        print(f"  - {rec}")
                    continue

                sentiment = loop.record_answer(category, answer)
                action_type = f"learn_preference_{category}"
                loop.log(action_type, {"answer": answer[:30]}, True, category)
                print(f"  [Learned: {category} = '{answer[:40]}...' | Sentiment: {sentiment['sentiment']}]")
                topic_idx += 1

                if topic_idx % 3 == 0:
                    result = loop.run_improvement_cycle()
                    print(f"  [Improvement cycle #{loop.cycle_count} complete]")

            else:
                print(f"\n--- All topics learned! ({len(topics)} preferences) ---")
                print(loop.get_summary())
                result = loop.run_improvement_cycle()
                print(f"\nFinal improvement cycle complete.")
                print("\nNow I know your preferences! You can:")
                print("  - Type 'status' to see stats")
                print("  - Type 'cycle' to run improvement")
                print("  - Type 'quit' to save and exit")
                cmd = input("\n> ").strip()
                if cmd.lower() == 'quit':
                    break
                elif cmd.lower() == 'status':
                    print(loop.get_summary())
                elif cmd.lower() == 'cycle':
                    result = loop.run_improvement_cycle()
                    print("Improvement cycle done!")

        print(f"\nSaving... Goodbye! Learned {len(loop.user_preferences)} preferences across {loop.cycle_count} cycles.")
        save_db(loop.db)
