import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from self_learning_engine import *
import numpy as np

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

def test_neural_network():
    t = TestResult("Neural Network")
    
    nn = NeuralNetwork([4, 8, 4, 1])
    t.check(len(nn.weights) == 3, "Wrong number of weight layers")
    t.check(len(nn.biases) == 3, "Wrong number of bias layers")
    t.check(nn.weights[0].shape == (4, 8), "Wrong first layer shape")
    
    X = np.random.randn(10, 4)
    output = nn.forward(X)
    t.check(output.shape == (10, 1), "Wrong output shape")
    t.check(np.all(output >= 0) and np.all(output <= 1), "Output not in [0,1]")
    
    y = np.random.randint(0, 2, (10, 1))
    history = nn.train(X, y, epochs=100, learning_rate=0.1)
    t.check(len(history) == 100, "Wrong history length")
    t.check(history[-1] <= history[0] + 0.1, "Loss not stabilizing")
    
    test_path = os.path.join(os.path.dirname(__file__), "test_weights.json")
    nn.save_weights(test_path)
    nn2 = NeuralNetwork([4, 8, 4, 1])
    nn2.load_weights(test_path)
    t.check(np.allclose(nn.weights[0], nn2.weights[0]), "Weights not saved correctly")
    try:
        os.remove(test_path)
    except:
        pass
    return t

def test_rl_agent():
    t = TestResult("RL Agent")
    
    agent = RLAgent(state_size=5, action_size=3, algorithm='q_learning')
    t.check(agent.epsilon == 1.0, "Initial epsilon wrong")
    
    state = [1, 0, 1, 0, 1]
    action = agent.get_action(state)
    t.check(0 <= action < 3, "Action out of range")
    
    for _ in range(100):
        state = np.random.randint(0, 2, 5).tolist()
        action = agent.get_action(state)
        next_state = np.random.randint(0, 2, 5).tolist()
        reward = np.random.random()
        done = np.random.random() > 0.9
        agent.update(state, action, reward, next_state, done)
    
    t.check(len(agent.q_table) > 0, "Q-table empty")
    t.check(agent.epsilon < 1.0, "Epsilon not decaying")
    
    episode_reward = agent.end_episode()
    t.check(len(agent.episode_rewards) == 1, "Episode rewards not tracked")
    
    policy = agent.get_policy()
    t.check(len(policy) > 0, "Policy empty")
    
    sarsa_agent = RLAgent(state_size=5, action_size=3, algorithm='sarsa')
    state = [1, 0, 1, 0, 1]
    action = sarsa_agent.get_action(state)
    sarsa_agent.update(state, action, 1.0, [0, 1, 0, 1, 0], False)
    t.check(len(sarsa_agent.q_table) > 0, "SARSA Q-table empty")
    return t

def test_bayesian():
    t = TestResult("Bayesian Inference")
    
    bayes = BayesianInference()
    bayes.set_prior("rain", 0.3)
    bayes.set_prior("no_rain", 0.7)
    
    posterior = bayes.update("rain", "wet_ground", 0.8)
    t.check(0 <= posterior <= 1, "Posterior out of range")
    t.check("rain" in bayes.posteriors, "Posterior not stored")
    
    prediction = bayes.predict("cloudy")
    t.check(prediction is not None, "Prediction is None")
    
    confidence = bayes.get_confidence()
    t.check(0 <= confidence <= 1, "Confidence out of range")
    return t

def test_genetic_algorithm():
    t = TestResult("Genetic Algorithm")
    
    ga = GeneticAlgorithm(population_size=20, mutation_rate=0.1)
    population = ga.initialize_population(10)
    t.check(len(population) == 20, "Wrong population size")
    t.check(len(population[0]) == 10, "Wrong gene length")
    
    def fitness(individual):
        return sum(individual)
    
    best_fitness = ga.evaluate_fitness(fitness)
    t.check(best_fitness >= 0, "Fitness negative")
    t.check(ga.best_individual is not None, "Best individual not set")
    
    new_fitness = ga.evolve(fitness)
    t.check(ga.generation == 1, "Generation not incremented")
    t.check(new_fitness >= 0, "New fitness negative")
    
    for _ in range(10):
        ga.evolve(fitness)
    t.check(ga.generation == 11, "Wrong generation count after evolution")
    return t

def test_meta_learner():
    t = TestResult("Meta Learner")
    
    meta = MetaLearner()
    embedding = meta.encode_task("test task description")
    t.check(len(embedding) == 16, "Wrong embedding length")
    t.check(embedding in meta.task_embeddings, "Task not stored")
    
    strategies = ["strategy_a", "strategy_b", "strategy_c"]
    suggested = meta.suggest_strategy(embedding, strategies)
    t.check(suggested in strategies, "Suggested strategy not in list")
    
    meta.record_performance(embedding, "strategy_a", 0.8)
    meta.record_performance(embedding, "strategy_b", 0.6)
    
    suggested2 = meta.suggest_strategy(embedding, strategies)
    t.check(suggested2 == "strategy_a", "Best strategy not suggested")
    
    rankings = meta.get_strategy_rankings()
    t.check(len(rankings) == 2, "Wrong number of rankings")
    t.check(rankings[0][0] == "strategy_a", "Best strategy not first")
    return t

def test_pattern_clusterer():
    t = TestResult("Pattern Clusterer")
    
    clusterer = PatternClusterer(n_clusters=3)
    data = np.random.randn(100, 5).tolist()
    clusterer.fit(data)
    t.check(clusterer.centroids is not None, "Centroids not set")
    t.check(len(clusterer.centroids) == 3, "Wrong number of centroids")
    t.check(len(clusterer.assignments) == 100, "Wrong number of assignments")
    
    prediction = clusterer.predict(data[0])
    t.check(0 <= prediction < 3, "Prediction out of range")
    return t

def test_anomaly_detector():
    t = TestResult("Anomaly Detector")
    
    detector = AnomalyDetector(threshold=2.0)
    data = np.random.randn(100, 5).tolist()
    detector.fit(data)
    t.check(detector.mean is not None, "Mean not set")
    t.check(detector.std is not None, "Std not set")
    
    normal_point = np.mean(data, axis=0).tolist()
    t.check(not detector.detect(normal_point), "Normal point detected as anomaly")
    
    anomalous_point = [100, 100, 100, 100, 100]
    t.check(detector.detect(anomalous_point), "Anomalous point not detected")
    
    score = detector.get_anomaly_score(anomalous_point)
    t.check(score > 0, "Anomaly score is 0")
    return t

def test_knowledge_graph():
    t = TestResult("Knowledge Graph")
    
    kg = KnowledgeGraph()
    kg.add_node("n1", "concept", {"name": "A"})
    kg.add_node("n2", "concept", {"name": "B"})
    kg.add_node("n3", "concept", {"name": "C"})
    
    kg.add_edge("n1", "n2", "related_to", 0.8)
    kg.add_edge("n2", "n3", "related_to", 0.9)
    
    neighbors = kg.get_neighbors("n1")
    t.check(len(neighbors) == 1, "Wrong number of neighbors")
    t.check(neighbors[0][0] == "n2", "Wrong neighbor")
    
    path = kg.find_path("n1", "n3")
    t.check(path is not None, "Path not found")
    t.check(len(path) == 3, "Wrong path length")
    
    inference = kg.infer_relationships("n1", "n3")
    t.check(inference['connected'] == True, "Not connected")
    t.check(inference['distance'] == 2, "Wrong distance")
    
    scores = kg.get_importance_scores()
    t.check(len(scores) == 3, "Wrong number of scores")
    return t

def test_basic_functions():
    t = TestResult("Basic Functions")
    
    db = init_learning_db()
    t.check(db is not None, "DB is None")
    t.check(db["version"] in ["2.0", "3.0"], f"Wrong version: {db['version']}")
    
    entry = log_action("test_action", {"key": "value"}, True, context="test")
    t.check(entry is not None, "Entry is None")
    t.check(entry["type"] == "test_action", "Wrong type")
    
    pattern = detect_pattern("test_pattern", "test_ctx")
    t.check(pattern["count"] >= 1, "Pattern count wrong")
    
    strategy = get_best_strategy("test_pattern")
    t.check(strategy is not None, "Strategy is None")
    
    lesson = learn_from_mistake("test_action", "test_error", "test_fix")
    t.check(lesson is not None, "Lesson is None")
    
    success = amplify_success("test_action", "test_ctx", True)
    t.check(success is not None, "Success is None")
    
    prediction = predict_next_action("test_action")
    prob = predict_success_probability("test_action", "test_ctx")
    t.check(0 <= prob <= 1, "Probability out of range")
    
    stats = get_performance_stats()
    t.check("total_actions" in stats, "Missing total_actions")
    
    result = improve()
    t.check("stats" in result, "Missing stats")
    
    curve = get_learning_curve()
    return t

def run_all_tests():
    print("=" * 60)
    print("SELF-LEARNING ENGINE v3.0 - ADVANCED TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_basic_functions(),
        test_neural_network(),
        test_rl_agent(),
        test_bayesian(),
        test_genetic_algorithm(),
        test_meta_learner(),
        test_pattern_clusterer(),
        test_anomaly_detector(),
        test_knowledge_graph(),
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
