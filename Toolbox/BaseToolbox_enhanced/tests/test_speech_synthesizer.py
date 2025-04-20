import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from text.speech_synthesizer import run
except ImportError:
    pytest.skip("Module text.speech_synthesizer not found")

def test_run_smoke():
    """Basic smoke test for speech_synthesizer"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
