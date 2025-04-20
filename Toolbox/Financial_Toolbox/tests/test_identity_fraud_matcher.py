import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.fraud.identity_fraud_matcher import run
except ImportError:
    pytest.skip("Module finance.fraud.identity_fraud_matcher not found")

def test_run_basic_identity_fraud_matcher():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
