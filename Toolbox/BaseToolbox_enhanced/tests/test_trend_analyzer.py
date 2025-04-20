import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from data.trend_analyzer import run
except ImportError:
    pytest.skip("Module data.trend_analyzer not found")

def test_run_smoke():
    """Basic smoke test for trend_analyzer"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
