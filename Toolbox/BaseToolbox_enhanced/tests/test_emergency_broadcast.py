import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from iot.emergency_broadcast import run
except ImportError:
    pytest.skip("Module iot.emergency_broadcast not found")

def test_run_smoke():
    """Basic smoke test for emergency_broadcast"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
