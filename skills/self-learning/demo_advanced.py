from self_learning_engine import (
    NeuralNetwork, RLAgent, BayesianInference, GeneticAlgorithm,
    MetaLearner, PatternClusterer, AnomalyDetector, KnowledgeGraph,
    init_learning_db, log_action, detect_pattern, get_best_strategy,
    learn_from_mistake, amplify_success, predict_next_action,
    predict_success_probability, get_performance_stats, get_improvement_recommendations,
    improve, get_learning_curve
)
import numpy as np

def demo():
    print("=" * 60)
    print("SELF-LEARNING ENGINE v3.0 - ADVANCED DEMONSTRATION")
    print("=" * 60)
    
    # Initialize
    db = init_learning_db()
    print(f"\n[INIT] Knowledge base initialized")
    
    # Neural Network
    print("\n--- Neural Network ---")
    nn = NeuralNetwork([4, 8, 4, 1])
    X = np.random.randn(20, 4)
    y = np.random.randint(0, 2, (20, 1))
    history = nn.train(X, y, epochs=50, learning_rate=0.1)
    print(f"[OK] Trained neural network: loss {history[0]:.4f} -> {history[-1]:.4f}")
    
    # Reinforcement Learning
    print("\n--- Reinforcement Learning ---")
    agent = RLAgent(state_size=5, action_size=3, algorithm='q_learning')
    for _ in range(100):
        state = np.random.randint(0, 2, 5).tolist()
        action = agent.get_action(state)
        next_state = np.random.randint(0, 2, 5).tolist()
        reward = np.random.random()
        done = np.random.random() > 0.9
        agent.update(state, action, reward, next_state, done)
    episode_reward = agent.end_episode()
    print(f"[OK] RL agent: {len(agent.q_table)} states explored, episode reward: {episode_reward:.2f}")
    
    # Bayesian Inference
    print("\n--- Bayesian Inference ---")
    bayes = BayesianInference()
    bayes.set_prior("rain", 0.3)
    bayes.set_prior("no_rain", 0.7)
    posterior = bayes.update("rain", "wet_ground", 0.8)
    print(f"[OK] Bayesian: P(rain|wet_ground) = {posterior:.3f}")
    
    # Genetic Algorithm
    print("\n--- Genetic Algorithm ---")
    ga = GeneticAlgorithm(population_size=30, mutation_rate=0.1)
    ga.initialize_population(gene_length=15)
    def fitness(individual):
        return sum(individual)
    best_fitness = ga.evolve(fitness)
    print(f"[OK] Genetic algorithm: generation {ga.generation}, best fitness: {best_fitness}")
    
    # Meta-Learning
    print("\n--- Meta-Learning ---")
    meta = MetaLearner()
    embedding = meta.encode_task("optimize form submission")
    strategies = ["retry", "wait", "alternative"]
    meta.record_performance(embedding, "retry", 0.8)
    meta.record_performance(embedding, "wait", 0.6)
    suggested = meta.suggest_strategy(embedding, strategies)
    print(f"[OK] Meta-learner suggested strategy: {suggested}")
    
    # Pattern Clustering
    print("\n--- Pattern Clustering ---")
    clusterer = PatternClusterer(n_clusters=3)
    data = np.random.randn(50, 4).tolist()
    clusterer.fit(data)
    prediction = clusterer.predict(data[0])
    print(f"[OK] Clusterer: {len(clusterer.centroids)} clusters, prediction: {prediction}")
    
    # Anomaly Detection
    print("\n--- Anomaly Detection ---")
    detector = AnomalyDetector(threshold=2.0)
    normal_data = np.random.randn(100, 4).tolist()
    detector.fit(normal_data)
    normal = detector.detect([0, 0, 0, 0])
    anomaly = detector.detect([100, 100, 100, 100])
    print(f"[OK] Anomaly detector: normal={normal}, anomaly={anomaly}")
    
    # Knowledge Graph
    print("\n--- Knowledge Graph ---")
    kg = KnowledgeGraph()
    kg.add_node("form", "concept", {"name": "Form"})
    kg.add_node("submit", "action", {"name": "Submit"})
    kg.add_node("success", "outcome", {"name": "Success"})
    kg.add_edge("form", "submit", "requires")
    kg.add_edge("submit", "success", "leads_to")
    path = kg.find_path("form", "success")
    print(f"[OK] Knowledge graph: path from form to success: {path}")
    
    # Basic Functions
    print("\n--- Basic Learning Functions ---")
    for i in range(5):
        log_action("click_button", {"target": "submit"}, i % 3 != 0, context="form")
        log_action("type_text", {"field": "email"}, True, context="input")
    
    pattern = detect_pattern("click_button", "form")
    print(f"[OK] Pattern detected: {pattern['count']} occurrences")
    
    lesson = learn_from_mistake("click_button", "timeout", "increase_wait")
    print(f"[OK] Learned from mistake: {lesson['error']} -> {lesson['correction']}")
    
    success = amplify_success("click_button", "form", True, {"accuracy": 0.95})
    print(f"[OK] Success amplified: score {success['success_score']:.2f}")
    
    prediction = predict_next_action("click_button")
    prob = predict_success_probability("click_button", "form")
    print(f"[OK] Predictions: next={prediction}, probability={prob:.2f}")
    
    # Performance Stats
    print("\n--- Performance Statistics ---")
    stats = get_performance_stats()
    print(f"[OK] Total actions: {stats['total_actions']}")
    print(f"     Success rate: {stats['success_rate']:.2%}")
    print(f"     Patterns: {stats['patterns_learned']}")
    
    # Improvement Cycle
    print("\n--- Improvement Cycle ---")
    result = improve()
    print(f"[OK] Recommendations: {len(result['recommendations'])}")
    for rec in result['recommendations'][:3]:
        print(f"     - [{rec['priority']}] {rec['suggestion']}")
    
    print("\n" + "=" * 60)
    print("ADVANCED DEMO COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    demo()
