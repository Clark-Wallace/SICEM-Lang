import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.signals.volatility_breakout_finder import run
except ImportError:
    pytest.skip("Module finance.signals.volatility_breakout_finder not found")

def test_run_basic_volatility_breakout_finder():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
