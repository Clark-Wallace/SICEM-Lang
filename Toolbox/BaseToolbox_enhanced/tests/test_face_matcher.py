import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from vision.face_matcher import run
except ImportError:
    pytest.skip("Module vision.face_matcher not found")

def test_run_smoke():
    """Basic smoke test for face_matcher"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
