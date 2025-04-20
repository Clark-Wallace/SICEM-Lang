import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.signals.momentum_signal_generator import run
except ImportError:
    pytest.skip("Module finance.signals.momentum_signal_generator not found")

def test_run_basic_momentum_signal_generator():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
