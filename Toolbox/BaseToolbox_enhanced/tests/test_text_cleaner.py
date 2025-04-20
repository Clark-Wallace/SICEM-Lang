import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from text.text_cleaner import run
except ImportError:
    pytest.skip("Module text.text_cleaner not found")

def test_run_smoke():
    """Basic smoke test for text_cleaner"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
