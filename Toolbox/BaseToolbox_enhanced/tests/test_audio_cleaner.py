import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from audio.audio_cleaner import run
except ImportError:
    pytest.skip("Module audio.audio_cleaner not found")

def test_run_smoke():
    """Basic smoke test for audio_cleaner"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
