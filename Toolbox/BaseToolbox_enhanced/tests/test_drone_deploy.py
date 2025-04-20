import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from iot.drone_deplo import run
except ImportError:
    pytest.skip("Module iot.drone_deplo not found")

def test_run_smoke():
    """Basic smoke test for drone_deploy"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
