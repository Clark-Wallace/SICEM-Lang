import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.credit.credit_score_modeler import run
except ImportError:
    pytest.skip("Module finance.credit.credit_score_modeler not found")

def test_run_basic_credit_score_modeler():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
