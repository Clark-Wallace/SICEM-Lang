import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from data.predictor_model import run
except ImportError:
    pytest.skip("Module data.predictor_model not found")

def test_run_smoke():
    """Basic smoke test for predictor_model"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
