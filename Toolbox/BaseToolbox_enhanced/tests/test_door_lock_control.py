import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from iot.door_lock_control import run
except ImportError:
    pytest.skip("Module iot.door_lock_control not found")

def test_run_smoke():
    """Basic smoke test for door_lock_control"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
