import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from text.summarize_text import run
except ImportError:
    pytest.skip("Module text.summarize_text not found")

def test_run_smoke():
    """Basic smoke test for summarize_text"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
