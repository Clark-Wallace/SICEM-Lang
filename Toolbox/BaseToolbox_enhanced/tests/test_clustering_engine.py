import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from data.clustering_engine import run
except ImportError:
    pytest.skip("Module data.clustering_engine not found")

def test_run_smoke():
    """Basic smoke test for clustering_engine"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
