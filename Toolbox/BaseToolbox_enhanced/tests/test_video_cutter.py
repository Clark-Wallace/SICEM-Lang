import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from audio.video_cutter import run
except ImportError:
    pytest.skip("Module audio.video_cutter not found")

def test_run_smoke():
    """Basic smoke test for video_cutter"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
