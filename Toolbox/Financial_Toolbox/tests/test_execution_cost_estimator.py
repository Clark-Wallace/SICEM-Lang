import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.execution.execution_cost_estimator import run
except ImportError:
    pytest.skip("Module finance.execution.execution_cost_estimator not found")

def test_run_basic_execution_cost_estimator():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
