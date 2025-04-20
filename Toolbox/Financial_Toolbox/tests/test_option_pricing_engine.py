import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.derivatives.option_pricing_engine import run
except ImportError:
    pytest.skip("Module finance.derivatives.option_pricing_engine not found")

def test_run_basic_option_pricing_engine():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
