import time
from datetime import timedelta
from unittest.mock import Mock, call
from app.gatherers import DataGatherer, CachingDataGatherer


class MockGatherer(DataGatherer):
    """Mock gatherer that tracks how many times gather() was called."""
    def __init__(self):
        self.call_count = 0

    def gather(self):
        self.call_count += 1
        return f"result_{self.call_count}"


def test_first_call_fetches_data():
    """First call should fetch data from the underlying gatherer."""
    mock = MockGatherer()
    caching = CachingDataGatherer(mock, cache_duration=timedelta(seconds=5))
    
    result = caching.gather()
    assert result == "result_1"
    assert mock.call_count == 1
    print("✓ First call fetches data")


def test_second_call_within_cache_returns_cached():
    """Second call within cache duration should return cached data."""
    mock = MockGatherer()
    caching = CachingDataGatherer(mock, cache_duration=timedelta(seconds=5))
    
    result1 = caching.gather()
    result2 = caching.gather()
    
    assert result1 == "result_1"
    assert result2 == "result_1"  # Should be the same cached result
    assert mock.call_count == 1   # Should only be called once
    print("✓ Second call returns cached data")


def test_call_after_cache_expires():
    """Call after cache expires should fetch fresh data."""
    mock = MockGatherer()
    caching = CachingDataGatherer(mock, cache_duration=timedelta(milliseconds=100))
    
    result1 = caching.gather()
    time.sleep(0.15)  # Wait for cache to expire
    result2 = caching.gather()
    
    assert result1 == "result_1"
    assert result2 == "result_2"  # Should be fresh data
    assert mock.call_count == 2   # Should be called twice
    print("✓ Call after cache expires fetches fresh data")


def test_multiple_calls_within_cache():
    """Multiple calls within cache duration should all return cached data."""
    mock = MockGatherer()
    caching = CachingDataGatherer(mock, cache_duration=timedelta(seconds=5))
    
    result1 = caching.gather()
    result2 = caching.gather()
    result3 = caching.gather()
    
    assert result1 == result2 == result3 == "result_1"
    assert mock.call_count == 1  # Should only be called once
    print("✓ Multiple calls within cache return same result")


if __name__ == "__main__":
    test_first_call_fetches_data()
    test_second_call_within_cache_returns_cached()
    test_call_after_cache_expires()
    test_multiple_calls_within_cache()
    print("\n✓ All tests passed!")
