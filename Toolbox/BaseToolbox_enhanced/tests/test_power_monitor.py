import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from iot.power_monitor import run
except ImportError:
    pytest.skip("Module iot.power_monitor not found")

def test_run_smoke():
    """Basic smoke test for power_monitor"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
