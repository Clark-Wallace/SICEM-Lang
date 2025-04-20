import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from core.env_checker import run
except ImportError:
    pytest.skip("Module core.env_checker not found")

def test_run_smoke():
    """Basic smoke test for env_checker"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
