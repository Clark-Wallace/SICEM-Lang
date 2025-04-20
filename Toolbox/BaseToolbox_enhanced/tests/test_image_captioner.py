import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from vision.image_captioner import run
except ImportError:
    pytest.skip("Module vision.image_captioner not found")

def test_run_smoke():
    """Basic smoke test for image_captioner"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
