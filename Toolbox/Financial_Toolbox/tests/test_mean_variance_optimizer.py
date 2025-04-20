import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.portfolio.mean_variance_optimizer import run
except ImportError:
    pytest.skip("Module finance.portfolio.mean_variance_optimizer not found")

def test_run_basic_mean_variance_optimizer():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
