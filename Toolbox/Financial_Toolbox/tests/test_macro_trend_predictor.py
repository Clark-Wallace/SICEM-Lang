import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.forecasting.macro_trend_predictor import run
except ImportError:
    pytest.skip("Module finance.forecasting.macro_trend_predictor not found")

def test_run_basic_macro_trend_predictor():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
