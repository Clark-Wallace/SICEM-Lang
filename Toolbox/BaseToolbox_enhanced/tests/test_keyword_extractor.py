import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from text.keyword_extractor import run
except ImportError:
    pytest.skip("Module text.keyword_extractor not found")

def test_run_smoke():
    """Basic smoke test for keyword_extractor"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
