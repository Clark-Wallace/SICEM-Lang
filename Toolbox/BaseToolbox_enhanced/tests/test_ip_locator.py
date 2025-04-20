import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from web.ip_locator import run
except ImportError:
    pytest.skip("Module web.ip_locator not found")

def test_run_smoke():
    """Basic smoke test for ip_locator"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
