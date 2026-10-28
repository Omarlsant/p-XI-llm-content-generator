#!/usr/bin/env python3
"""
Portable Backend Test Runner

Executes test suite with pytest if installed; falls back to standard Python
introspection and execution if running in a minimal environment.
"""
import os
import sys
import inspect
import importlib

# Ensure server root is in sys.path
SERVER_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVER_ROOT not in sys.path:
    sys.path.insert(0, SERVER_ROOT)

def main():
    # If pytest is available, prefer running through pytest
    try:
        import pytest
        print("--- Running tests via pytest ---")
        exit_code = pytest.main(["-v", os.path.dirname(__file__)])
        sys.exit(exit_code)
    except ImportError:
        pass

    # Fallback to direct test function runner
    print("--- Running backend tests via standard python runner ---")
    test_dir = os.path.dirname(__file__)
    test_files = [
        f[:-3] for f in sorted(os.listdir(test_dir))
        if f.startswith("test_") and f.endswith(".py")
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    for mod_name in test_files:
        try:
            mod = importlib.import_module(f"tests.{mod_name}")
        except Exception as e:
            print(f"❌ Failed to import tests.{mod_name}: {e}")
            failed_tests += 1
            continue

        for attr_name in dir(mod):
            if attr_name.startswith("test_"):
                func = getattr(mod, attr_name)
                if inspect.isfunction(func):
                    total_tests += 1
                    try:
                        func()
                        print(f"  ✔ {mod_name}.{attr_name}")
                        passed_tests += 1
                    except Exception as exc:
                        print(f"  ❌ {mod_name}.{attr_name}: {exc}")
                        failed_tests += 1

    print("\n------------------------------------------------------------")
    print(f"Test Summary: {passed_tests} passed, {failed_tests} failed, {total_tests} total.")
    print("------------------------------------------------------------")

    if failed_tests > 0:
        sys.exit(1)
    else:
        print("✅ All discovered backend tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
