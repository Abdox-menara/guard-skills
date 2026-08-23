# Unified Optimization Script
# Combines all optimization modules for opencode

import time
import os

def check_dependencies():
    """Check which optimization modules are available"""
    modules = {
        "memory_system": False,
        "performance_optimization": False,
        "skill_system": False,
        "streaming_context": False,
        "openvino_integration": False,
        "mcp_integration": False,
    }
    
    for module in modules:
        try:
            __import__(module)
            modules[module] = True
        except:
            pass
    
    return modules


def print_status(modules):
    """Print module status"""
    print("=" * 60)
    print("OPENCODE OPTIMIZATION STATUS")
    print("=" * 60)
    
    for name, available in modules.items():
        status = "[OK]" if available else "[MISSING]"
        print(f"  {status} {name}")
    
    print("=" * 60)
    
    total = len(modules)
    available = sum(modules.values())
    print(f"Modules: {available}/{total} available")
    print()


def run_benchmarks():
    """Run quick benchmarks"""
    print("Running benchmarks...")
    
    # SQLite benchmark
    try:
        from performance_optimization import OptimizedSQLiteMemory
        db = OptimizedSQLiteMemory(":memory:")
        
        start = time.time()
        for i in range(100):
            db.set_pref(f"key_{i}", f"value_{i}")
        elapsed = (time.time() - start) * 1000
        print(f"  SQLite write 100 records: {elapsed:.1f}ms")
    except Exception as e:
        print(f"  SQLite benchmark error: {e}")
    
    # Cache benchmark
    try:
        from performance_optimization import TwoTierCache
        cache = TwoTierCache(max_memory=1000)
        
        start = time.time()
        for i in range(1000):
            cache.set(f"key_{i}", f"value_{i}")
        for i in range(1000):
            cache.get(f"key_{i}")
        elapsed = (time.time() - start) * 1000
        print(f"  Cache 1000 set+get: {elapsed:.1f}ms")
    except Exception as e:
        print(f"  Cache benchmark error: {e}")
    
    print()


def main():
    """Main optimization runner"""
    print()
    modules = check_dependencies()
    print_status(modules)
    
    if modules.get("performance_optimization"):
        run_benchmarks()
    
    print("Optimization check complete!")
    print()
    print("Next steps:")
    print("  1. Install OpenVINO: pip install openvino")
    print("  2. Convert RapidOCR models to OpenVINO IR format")
    print("  3. Run: python openvino_integration.py")


if __name__ == "__main__":
    main()

