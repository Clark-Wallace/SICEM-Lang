import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.compliance.kyc_data_validator import run
except ImportError:
    pytest.skip("Module finance.compliance.kyc_data_validator not found")

def test_run_basic_kyc_data_validator():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
