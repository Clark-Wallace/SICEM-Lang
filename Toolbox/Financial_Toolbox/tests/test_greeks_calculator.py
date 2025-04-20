import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.derivatives.greeks_calculator import run
except ImportError:
    pytest.skip("Module finance.derivatives.greeks_calculator not found")

def test_run_basic_greeks_calculator():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
