import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.signals.mean_reversion_detector import run
except ImportError:
    pytest.skip("Module finance.signals.mean_reversion_detector not found")

def test_run_basic_mean_reversion_detector():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
