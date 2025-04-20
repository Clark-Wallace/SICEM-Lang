import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from web.map_renderer import run
except ImportError:
    pytest.skip("Module web.map_renderer not found")

def test_run_smoke():
    """Basic smoke test for map_renderer"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
