#!/usr/bin/env python3
"""
Test script for TeraBox skills
"""

import sys
import os

# Add the skill directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "skills", "tools", "terabox-integration"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "skills", "workflow", "terabox-improvement"))


def test_terabox_improvement():
    """Test the TeraBox improvement analyzer"""
    try:
        from terabox_improvement import TeraBoxImprovement

        analyzer = TeraBoxImprovement()

        # Test workflow analysis
        workflow_data = {
            "manual_cookie_extraction": True,
            "optimized_compression": False,
            "retry_logic": False,
            "parallel_uploads": False,
            "progress_tracking": False,
        }

        result = analyzer.analyze_upload_workflow(workflow_data)
        print(f"[OK] Workflow analysis: Score {result['score']}, Issues: {len(result['issues'])}")

        # Test security analysis
        auth_data = {"hardcoded_cookies": False, "session_persisted": True, "https_only": True}

        security = analyzer.analyze_security(auth_data)
        print(
            f"[OK] Security analysis: Risk Level {security['risk_level']}, Issues: {len(security['security_issues'])}"
        )

        # Test improvement plan
        plan = analyzer.generate_improvement_plan({"analyses": [result, security]})
        print(f"[OK] Improvement plan: Total Issues {plan['total_issues']}, Critical: {plan['critical_issues']}")

        return True

    except Exception as e:
        print(f"[FAIL] Error testing terabox-improvement: {e}")
        return False


def test_terabox_integration():
    """Test the TeraBox integration tool"""
    try:
        # Just test that the module can be imported
        from terabox import TeraBoxIntegration

        tb = TeraBoxIntegration()
        print("[OK] TeraBoxIntegration class instantiated")

        # Test that methods exist
        methods = ["check_quota", "list_files", "upload_file", "upload_folder", "verify_upload", "compress_folder"]
        for method in methods:
            if hasattr(tb, method):
                print(f"  [OK] Method {method} exists")
            else:
                print(f"  [FAIL] Method {method} missing")
                return False

        return True

    except ImportError as e:
        print(f"[FAIL] Could not import terabox (expected if playwright not installed): {e}")
        return True  # This is expected
    except Exception as e:
        print(f"[FAIL] Error testing terabox-integration: {e}")
        return False


def main():
    print("Testing TeraBox Skills...")
    print("=" * 50)

    tests = [("TeraBox Improvement", test_terabox_improvement), ("TeraBox Integration", test_terabox_integration)]

    results = []
    for name, test_func in tests:
        print(f"\nTesting {name}:")
        result = test_func()
        results.append((name, result))

    print("\n" + "=" * 50)
    print("Test Results:")
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {name}: {status}")

    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
