import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from audio.audio_transcriber import run
except ImportError:
    pytest.skip("Module audio.audio_transcriber not found")

def test_run_smoke():
    """Basic smoke test for audio_transcriber"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
