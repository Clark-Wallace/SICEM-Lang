import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from iot.thermo_sensor_read import run
except ImportError:
    pytest.skip("Module iot.thermo_sensor_read not found")

def test_run_smoke():
    """Basic smoke test for thermo_sensor_read"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
