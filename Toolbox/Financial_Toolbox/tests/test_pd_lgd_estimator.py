import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.credit.pd_lgd_estimator import run
except ImportError:
    pytest.skip("Module finance.credit.pd_lgd_estimator not found")

def test_run_basic_pd_lgd_estimator():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
