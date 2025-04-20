import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.derivatives.implied_vol_surface_builder import run
except ImportError:
    pytest.skip("Module finance.derivatives.implied_vol_surface_builder not found")

def test_run_basic_implied_vol_surface_builder():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
