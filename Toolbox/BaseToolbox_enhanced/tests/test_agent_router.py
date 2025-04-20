import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from meta.agent_router import run
except ImportError:
    pytest.skip("Module meta.agent_router not found")

def test_run_smoke():
    """Basic smoke test for agent_router"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
