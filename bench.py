# Fixed benchmark
import time
from performance_optimization import TwoTierCache

print("Running benchmarks...")

cache = TwoTierCache(db=":memory:")

start = time.time()
for i in range(1000):
    cache.put(f"key_{i}", f"value_{i}")
for i in range(1000):
    cache.get(f"key_{i}")
elapsed = (time.time() - start) * 1000
print(f"Cache 1000 put+get: {elapsed:.1f}ms")

print("Benchmark complete!")

