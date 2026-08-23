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

def test_experience_replay():
    t = TestResult("Experience Replay Buffer")
    
    buffer = ExperienceReplayBuffer(capacity=100)
    t.check(len(buffer) == 0, "Initial buffer not empty")
    
    for i in range(50):
        state = np.random.randn(10)
        action = np.random.randint(5)
        reward = np.random.random()
        next_state = np.random.randn(10)
        done = np.random.random() > 0.9
        buffer.push(state, action, reward, next_state, done)
    
    t.check(len(buffer) == 50, f"Wrong buffer size: {len(buffer)}")
    
    states, actions, rewards, next_states, dones = buffer.sample(32)
    t.check(states.shape == (32, 10), f"Wrong states shape: {states.shape}")
    t.check(actions.shape == (32,), f"Wrong actions shape: {actions.shape}")
    t.check(rewards.shape == (32,), f"Wrong rewards shape: {rewards.shape}")
    
    for i in range(60):
        buffer.push(np.random.randn(10), 0, 0, np.random.randn(10), False)
    t.check(len(buffer) == 100, f"Buffer overflow: {len(buffer)}")
    
    empty = ExperienceReplayBuffer(capacity=10)
    try:
        empty.sample(5)
        t.check(False, "Should raise on empty buffer")
    except ValueError:
        t.check(True, "Raises ValueError on empty buffer")
    return t

def test_dueling_dqn():
    t = TestResult("Dueling DQN")
    
    dqn = DuelingDQN(state_size=10, action_size=5, hidden_size=32)
    state = np.random.randn(10)
    
    q_values = dqn.forward(state)
    t.check(q_values.shape == (1, 5), f"Wrong Q-values shape: {q_values.shape}")
    
    action = dqn.get_action(state, epsilon=0.1)
    t.check(0 <= action < 5, f"Action out of range: {action}")
    
    error = dqn.update(state, action, 1.0, np.random.randn(10), False)
    t.check(error >= 0, f"Negative error: {error}")
    
    for _ in range(20):
        s = np.random.randn(10)
        a = dqn.get_action(s)
        dqn.update(s, a, np.random.random(), np.random.randn(10), np.random.random() > 0.9)
    return t

def test_actor_critic():
    t = TestResult("Actor-Critic")
    
    ac = ActorCritic(state_size=10, action_size=5, hidden_size=32)
    state = np.random.randn(10)
    
    action = ac.get_action(state)
    t.check(0 <= action < 5, f"Action out of range: {action}")
    t.check(len(ac.log_probs) == 1, "Log probs not recorded")
    t.check(len(ac.values) == 1, "Values not recorded")
    
    rewards = [np.random.random() for _ in range(10)]
    loss = ac.update(rewards)
    t.check(loss >= 0, f"Negative loss: {loss}")
    t.check(len(ac.log_probs) == 0, "Log probs not cleared")
    return t

def test_lstm():
    t = TestResult("LSTM")
    
    lstm = LSTM(input_size=5, hidden_size=20, output_size=3)
    
    inputs = [np.random.randn(5) for _ in range(10)]
    output, h = lstm.forward(inputs)
    t.check(output.shape == (1, 3), f"Wrong output shape: {output.shape}")
    t.check(h.shape == (1, 20), f"Wrong hidden shape: {h.shape}")
    
    sequence = lstm.predict_sequence(inputs)
    t.check(sequence.shape == (10, 3), f"Wrong sequence shape: {sequence.shape}")
    return t

def test_attention():
    t = TestResult("Attention Mechanism")
    
    attn = AttentionMechanism(embed_size=16)
    
    query = np.random.randn(1, 16)
    keys = np.random.randn(5, 16)
    values = np.random.randn(5, 16)
    
    output, weights = attn.attention(query, keys, values)
    t.check(output.shape == (1, 16), f"Wrong output shape: {output.shape}")
    t.check(weights.shape == (1, 5), f"Wrong weights shape: {weights.shape}")
    t.check(abs(np.sum(weights) - 1.0) < 0.01, "Weights don't sum to 1")
    
    multi_out = attn.multi_head_attention(query, keys, values, n_heads=4)
    t.check(multi_out.shape == (1, 16), f"Wrong multi-head shape: {multi_out.shape}")
    return t

def test_curriculum():
    t = TestResult("Curriculum Learning")
    
    curr = CurriculumLearning()
    curr.add_task("task1", difficulty=1)
    curr.add_task("task2", difficulty=2, prerequisites=["task1"])
    curr.add_task("task3", difficulty=3, prerequisites=["task2"])
    
    progress = curr.get_progress()
    t.check(progress['total_tasks'] == 3, "Wrong total tasks")
    t.check(progress['completed'] == 0, "Wrong completed count")
    
    next_task = curr.get_next_task()
    t.check(next_task['id'] == "task1", f"Wrong next task: {next_task}")
    
    curr.complete_task("task1")
    next_task = curr.get_next_task()
    t.check(next_task['id'] == "task2", f"Wrong next task after completion: {next_task}")
    
    progress = curr.get_progress()
    t.check(progress['completed'] == 1, "Wrong completed count after completion")
    return t

def test_few_shot():
    t = TestResult("Few-Shot Learning")
    
    fsl = FewShotLearner(n_shot=3)
    
    fsl.add_support("class_a", [np.array([1, 0, 0]), np.array([1, 1, 0]), np.array([1, 0, 1])])
    fsl.add_support("class_b", [np.array([0, 1, 0]), np.array([0, 1, 1]), np.array([0, 0, 1])])
    
    t.check("class_a" in fsl.prototypes, "Prototype for class_a not created")
    t.check("class_b" in fsl.prototypes, "Prototype for class_b not created")
    
    query = np.array([1, 0.5, 0.5])
    prediction = fsl.predict(query)
    t.check(prediction == "class_a", f"Wrong prediction: {prediction}")
    
    queries = [np.array([1, 0, 0]), np.array([0, 1, 0])]
    labels = ["class_a", "class_b"]
    accuracy = fsl.compute_accuracy(queries, labels)
    t.check(0 <= accuracy <= 1, f"Accuracy out of range: {accuracy}")
    return t

def test_continual():
    t = TestResult("Continual Learning")
    
    nn = NeuralNetwork([5, 10, 3])
    cl = ContinualLearner(nn, lambda_ewc=100)
    
    X = np.random.randn(20, 5)
    y = np.random.randint(0, 3, (20, 1))
    
    cl.consolidate(X, y)
    t.check(cl.task_count == 1, "Task count not incremented")
    t.check(0 in cl.fisher_information, "Fisher information not stored")
    t.check(0 in cl.optimal_weights, "Optimal weights not stored")
    
    cl.consolidate(X, y)
    t.check(cl.task_count == 2, "Task count not incremented for second task")
    
    original_loss = 0.5
    penalized = cl.penalized_loss(original_loss)
    t.check(penalized >= original_loss, "Penalized loss should be >= original")
    return t

def test_ensemble():
    t = TestResult("Ensemble Learner")
    
    ensemble = EnsembleLearner()
    
    model1 = NeuralNetwork([5, 10, 1])
    model2 = NeuralNetwork([5, 10, 1])
    
    ensemble.add_model(model1, weight=1.0)
    ensemble.add_model(model2, weight=0.8)
    t.check(len(ensemble.models) == 2, "Wrong number of models")
    
    X = np.random.randn(10, 5)
    prediction = ensemble.predict(X)
    t.check(prediction.shape == (10, 1), f"Wrong prediction shape: {prediction.shape}")
    
    performances = [0.8, 0.9]
    ensemble.update_weights(performances)
    t.check(len(ensemble.performance_history) == 1, "Performance history not updated")
    
    diversity = ensemble.get_diversity()
    t.check(0 <= diversity <= 10, f"Diversity out of range: {diversity}")
    return t

def test_hp_optimizer():
    t = TestResult("HP Optimizer")
    
    hp = HPOptimizer()
    hp.add_param('lr', 'log_uniform', low=1e-5, high=1e-1)
    hp.add_param('hidden', 'int', low=16, high=128)
    hp.add_param('activation', 'categorical', values=['relu', 'tanh', 'sigmoid'])
    
    for _ in range(20):
        params = hp.sample_params()
        t.check('lr' in params, "Missing lr")
        t.check('hidden' in params, "Missing hidden")
        t.check('activation' in params, "Missing activation")
        t.check(1e-5 <= params['lr'] <= 1e-1, f"lr out of range: {params['lr']}")
        t.check(16 <= params['hidden'] < 128, f"hidden out of range: {params['hidden']}")
        t.check(params['activation'] in ['relu', 'tanh', 'sigmoid'], f"Invalid activation: {params['activation']}")
        
        score = np.random.random()
        hp.record_trial(params, score)
    
    best_params, best_score = hp.get_best()
    t.check(best_params is not None, "Best params not set")
    t.check(best_score > 0, f"Best score not positive: {best_score}")
    
    sorted_trials = hp.get_trials_sorted()
    t.check(len(sorted_trials) == 20, "Wrong number of trials")
    t.check(sorted_trials[0]['score'] >= sorted_trials[-1]['score'], "Trials not sorted")
    return t

def test_meta_controller():
    t = TestResult("Meta Controller")
    
    mc = MetaController()
    
    mc.register_strategy("strategy_a", lambda x: x * 2)
    mc.register_strategy("strategy_b", lambda x: x * 3)
    t.check(len(mc.strategies) == 2, "Wrong number of strategies")
    
    selected = mc.select_strategy()
    t.check(selected in mc.strategies, f"Invalid strategy selected: {selected}")
    
    mc.update_strategy("strategy_a", reward=0.9, context="context1")
    mc.update_strategy("strategy_b", reward=0.7, context="context1")
    
    selected = mc.select_strategy(context="context1")
    t.check(selected == "strategy_a", f"Best strategy not selected: {selected}")
    
    rankings = mc.get_rankings()
    t.check(len(rankings) == 2, "Wrong number of rankings")
    t.check(rankings[0]['name'] == "strategy_a", "Best strategy not first")
    return t

def test_emotional_intelligence():
    t = TestResult("Emotional Intelligence")
    
    ei = EmotionalIntelligence()
    
    result = ei.analyze_sentiment("This is great and amazing")
    t.check(result['sentiment'] == 'positive', f"Wrong sentiment: {result['sentiment']}")
    t.check(result['score'] > 0.5, f"Score should be > 0.5: {result['score']}")
    
    result = ei.analyze_sentiment("This is terrible and horrible")
    t.check(result['sentiment'] == 'negative', f"Wrong sentiment: {result['sentiment']}")
    
    emotion = ei.detect_emotion("I love this success", context="task")
    t.check(emotion == 'joy', f"Wrong emotion: {emotion}")
    t.check(len(ei.emotion_history) == 1, "Emotion not recorded")
    t.check("task" in ei.emotion_patterns, "Context not recorded")
    
    trend = ei.get_emotional_trend()
    t.check(trend is None, "Trend should be None with less than 10 entries")
    
    for _ in range(15):
        ei.detect_emotion("This is great")
    
    trend = ei.get_emotional_trend()
    t.check(trend is not None, "Trend should not be None")
    t.check('dominant_emotion' in trend, "Missing dominant_emotion")
    
    response = ei.suggest_response("joy")
    t.check("positive" in response.lower(), f"Response should be positive: {response}")
    return t

def run_all_tests():
    print("=" * 60)
    print("SELF-LEARNING ENGINE v4.0 - NEW COMPONENTS TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_experience_replay(),
        test_dueling_dqn(),
        test_actor_critic(),
        test_lstm(),
        test_attention(),
        test_curriculum(),
        test_few_shot(),
        test_continual(),
        test_ensemble(),
        test_hp_optimizer(),
        test_meta_controller(),
        test_emotional_intelligence(),
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
