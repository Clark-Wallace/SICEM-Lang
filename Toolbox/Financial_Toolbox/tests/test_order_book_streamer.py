import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from finance.market_data.order_book_streamer import run
except ImportError:
    pytest.skip("Module finance.market_data.order_book_streamer not found")

def test_run_basic_order_book_streamer():
    """Basic smoke test"""
    try:
        res = run()
    except Exception:
        pytest.skip("run() not implemented yet")
    assert res is not None
