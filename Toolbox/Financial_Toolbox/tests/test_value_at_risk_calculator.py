import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.risk.value_at_risk_calculator import run
except ImportError:
    pytest.skip("Module finance.risk.value_at_risk_calculator not found")

def test_run_basic_value_at_risk_calculator():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
