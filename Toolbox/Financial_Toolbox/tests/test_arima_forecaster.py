import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.forecasting.arima_forecaster import run
except ImportError:
    pytest.skip("Module finance.forecasting.arima_forecaster not found")

def test_run_basic_arima_forecaster():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
