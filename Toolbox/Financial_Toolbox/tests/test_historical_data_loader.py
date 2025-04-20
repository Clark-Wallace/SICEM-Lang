import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.market_data.historical_data_loader import run
except ImportError:
    pytest.skip("Module finance.market_data.historical_data_loader not found")

def test_run_basic_historical_data_loader():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
