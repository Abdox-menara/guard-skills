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

def test_transformer():
    t = TestResult("Transformer")
    
    transformer = Transformer(d_model=32, n_heads=4, n_layers=2, d_ff=64)
    
    x = np.random.randn(2, 10, 32)
    output = transformer.forward(x)
    t.check(output.shape == (2, 10, 32), f"Wrong output shape: {output.shape}")
    
    tokens = list(range(10))
    encoded = transformer.encode(tokens)
    t.check(encoded.shape == (1, 10, 32), f"Wrong encoded shape: {encoded.shape}")
    return t

def test_gnn():
    t = TestResult("Graph Neural Network")
    
    gnn = GraphNeuralNetwork(node_features=8, hidden_features=16, output_features=4)
    
    node_features = np.random.randn(10, 8)
    adjacency = np.eye(10)
    for i in range(10):
        for j in range(i+1, min(i+3, 10)):
            adjacency[i, j] = 1
            adjacency[j, i] = 1
    
    output = gnn.forward(node_features, adjacency)
    t.check(output.shape == (10, 4), f"Wrong output shape: {output.shape}")
    
    graph_embedding = gnn.embed_graph(node_features, adjacency)
    t.check(graph_embedding.shape == (4,), f"Wrong embedding shape: {graph_embedding.shape}")
    return t

def test_vae():
    t = TestResult("Variational Autoencoder")
    
    vae = VariationalAutoencoder(input_dim=20, latent_dim=8)
    
    x = np.random.randn(5, 20)
    recon, mu, logvar = vae.forward(x)
    t.check(recon.shape == (5, 20), f"Wrong recon shape: {recon.shape}")
    t.check(mu.shape == (5, 8), f"Wrong mu shape: {mu.shape}")
    t.check(logvar.shape == (5, 8), f"Wrong logvar shape: {logvar.shape}")
    
    loss = vae.loss(x, recon, mu, logvar)
    t.check(loss >= 0, f"Negative loss: {loss}")
    
    generated = vae.generate(3)
    t.check(generated.shape == (3, 20), f"Wrong generated shape: {generated.shape}")
    return t

def test_mcts():
    t = TestResult("Monte Carlo Tree Search")
    
    mcts = MonteCarloTreeSearch(rollout_limit=20)
    root = MCTSNode(state=0)
    
    best = mcts.search(root, n_iterations=50)
    t.check(best is not None, "Best node is None")
    t.check(best.visits > 0, "Best node not visited")
    return t

def test_thompson():
    t = TestResult("Thompson Sampling")
    
    ts = ThompsonSampling(n_arms=5)
    
    arm = ts.sample()
    t.check(0 <= arm < 5, f"Arm out of range: {arm}")
    
    ts.update(arm, 1.0)
    probs = ts.get_probabilities()
    t.check(len(probs) == 5, f"Wrong number of probabilities: {len(probs)}")
    t.check(all(0 <= p <= 1 for p in probs), "Probabilities out of range")
    
    confidence = ts.get_confidence()
    t.check(len(confidence) == 5, "Wrong confidence length")
    return t

def test_ucb():
    t = TestResult("Upper Confidence Bound")
    
    ucb = UpperConfidenceBound(n_arms=5, c=2.0)
    
    for _ in range(100):
        arm = ucb.select_arm()
        reward = np.random.random()
        ucb.update(arm, reward)
    
    t.check(sum(ucb.counts) == 100, "Wrong total counts")
    t.check(all(c > 0 for c in ucb.counts), "Some arms not explored")
    return t

def test_ppo():
    t = TestResult("PPO Agent")
    
    ppo = PPOAgent(state_size=10, action_size=5, hidden_size=32)
    
    state = np.random.randn(10)
    action, prob = ppo.get_action(state)
    t.check(0 <= action < 5, f"Action out of range: {action}")
    t.check(0 <= prob <= 1, f"Prob out of range: {prob}")
    
    value = ppo.get_value(state)
    t.check(value.shape == (1, 1), f"Wrong value shape: {value.shape}")
    
    rewards = [np.random.random() for _ in range(10)]
    values = [np.random.random() for _ in range(10)]
    dones = [False] * 9 + [True]
    advantages, returns = ppo.compute_gae(rewards, values, dones)
    t.check(len(advantages) == 10, "Wrong advantages length")
    t.check(len(returns) == 10, "Wrong returns length")
    
    states = np.random.randn(10, 10)
    actions = np.random.randint(0, 5, 10)
    old_probs = np.random.random(10)
    loss = ppo.update(states, actions, old_probs, advantages, returns, epochs=5)
    t.check(loss >= 0, f"Negative loss: {loss}")
    return t

def test_world_model():
    t = TestResult("World Model")
    
    wm = WorldModel(state_size=10, action_size=5, hidden_size=32)
    
    state = np.random.randn(10)
    action = 2
    next_state = wm.predict_next_state(state, action)
    t.check(next_state.shape == (1, 10), f"Wrong next_state shape: {next_state.shape}")
    
    reward = wm.predict_reward(state, action)
    t.check(np.isscalar(reward), "Reward not scalar")
    
    def policy(s):
        return np.random.randint(5)
    
    trajectory = wm.imagine_trajectory(state, policy, horizon=5)
    t.check(len(trajectory) == 5, f"Wrong trajectory length: {len(trajectory)}")
    
    wm.store_experience(state, action, 1.0, next_state)
    t.check(len(wm.memory) == 1, "Memory not updated")
    return t

def test_curiosity():
    t = TestResult("Intrinsic Motivation")
    
    im = IntrinsicMotivation(state_size=10, action_size=5, hidden_size=32)
    
    state = np.random.randn(10)
    action = 2
    next_state = np.random.randn(10)
    
    reward = im.compute_curiosity_reward(state, action, next_state)
    t.check(reward >= 0, f"Negative curiosity reward: {reward}")
    
    novelty = im.get_state_novelty(state)
    t.check(0 <= novelty <= 1, f"Novelty out of range: {novelty}")
    
    for _ in range(5):
        im.compute_curiosity_reward(state, action, np.random.randn(10))
    
    novelty2 = im.get_state_novelty(state)
    t.check(novelty2 <= novelty, "Novelty should decrease with visits")
    return t

def test_option_critic():
    t = TestResult("Option-Critic")
    
    oc = OptionCritic(state_size=10, n_options=4, action_size=5)
    
    state = np.random.randn(10)
    option = oc.select_option(state)
    t.check(0 <= option < 4, f"Option out of range: {option}")
    
    action = oc.select_action(state, option)
    t.check(0 <= action < 5, f"Action out of range: {action}")
    
    terminate = oc.should_terminate(state, option)
    t.check(isinstance(terminate, (bool, np.bool_)), "Termination not boolean")
    return t

def test_multi_agent():
    t = TestResult("Multi-Agent System")
    
    mas = MultiAgentSystem(n_agents=3, state_size=10, action_size=5)
    
    for i in range(3):
        state = np.random.randn(10)
        action = mas.select_action(i, state)
        t.check(0 <= action < 5, f"Agent {i} action out of range: {action}")
        
        next_state = np.random.randn(10)
        reward = np.random.random()
        mas.update_agent(i, state, action, reward, next_state, False)
    
    performance = mas.get_team_performance()
    t.check('total_score' in performance, "Missing total_score")
    t.check('best_agent' in performance, "Missing best_agent")
    t.check(performance['total_score'] > 0, "Total score not positive")
    
    mas.communicate(0, 1, "state_info")
    t.check(len(mas.agents[1]['communication']) == 1, "Communication not recorded")
    return t

def test_nas():
    t = TestResult("Neural Architecture Search")
    
    nas = NeuralArchitectureSearch(input_size=10, output_size=2)
    
    arch = nas.sample_architecture()
    t.check('layers' in arch, "Missing layers")
    t.check('activation' in arch, "Missing activation")
    t.check(arch['layers'][0] == 10, "Wrong input size")
    t.check(arch['layers'][-1] == 2, "Wrong output size")
    
    score = nas.evaluate_architecture(arch)
    t.check(0 <= score <= 1, f"Score out of range: {score}")
    
    best_arch, best_score = nas.get_best_architecture()
    t.check(best_arch is not None, "Best arch is None")
    
    offspring = nas.evolve_architectures(n_offspring=3)
    t.check(len(offspring) == 3, f"Wrong offspring count: {len(offspring)}")
    return t

def test_bayesian_optimization():
    t = TestResult("Bayesian Optimization")
    
    bo = BayesianOptimizer()
    
    for x in np.linspace(0, 10, 20):
        y = -((x - 5) ** 2) + 10
        bo.observe(x, y)
    
    mu, sigma = bo.gaussian_process_predict(np.array([3, 5, 7]))
    t.check(len(mu) == 3, f"Wrong mu length: {len(mu)}")
    t.check(len(sigma) == 3, f"Wrong sigma length: {len(sigma)}")
    
    next_x = bo.suggest_next(bounds=(0, 10))
    t.check(0 <= next_x <= 10, f"Next x out of bounds: {next_x}")
    return t

def run_all_tests():
    print("=" * 60)
    print("SELF-LEARNING ENGINE v5.0 - ULTRA-ADVANCED TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_transformer(),
        test_gnn(),
        test_vae(),
        test_mcts(),
        test_thompson(),
        test_ucb(),
        test_ppo(),
        test_world_model(),
        test_curiosity(),
        test_option_critic(),
        test_multi_agent(),
        test_nas(),
        test_bayesian_optimization(),
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
