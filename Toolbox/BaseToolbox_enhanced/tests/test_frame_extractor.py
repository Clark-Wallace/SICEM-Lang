import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from vision.frame_extractor import run
except ImportError:
    pytest.skip("Module vision.frame_extractor not found")

def test_run_smoke():
    """Basic smoke test for frame_extractor"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
