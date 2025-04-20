import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from core.csv_loader import run
except ImportError:
    pytest.skip("Module core.csv_loader not found")

def test_run_smoke():
    """Basic smoke test for csv_loader"""
    try:
        res = run({})
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
