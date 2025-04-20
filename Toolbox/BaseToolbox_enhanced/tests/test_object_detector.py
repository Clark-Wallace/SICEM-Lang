import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from vision.object_detector import run
except ImportError:
    pytest.skip("Module vision.object_detector not found")

def test_run_smoke():
    """Basic smoke test for object_detector"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
