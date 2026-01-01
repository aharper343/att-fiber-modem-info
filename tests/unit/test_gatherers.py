"""
Unit tests for gatherers module.

These tests are fast and isolated, testing individual components
without external dependencies.
"""
import time
import pytest
from datetime import timedelta
from unittest.mock import Mock, patch

from gatherers import DataGatherer, CachingDataGatherer


class MockGatherer(DataGatherer):
    """Mock gatherer for testing."""
    
    def __init__(self):
        self.call_count = 0
        self.return_value = "default_result"
    
    def gather(self):
        self.call_count += 1
        return f"result_{self.call_count}"


@pytest.mark.unit
class TestCachingDataGatherer:
    """Test suite for CachingDataGatherer."""
    
    def test_first_call_fetches_data(self, default_cache_duration):
        """First call should fetch data from the underlying gatherer."""
        mock_gatherer = MockGatherer()
        caching = CachingDataGatherer(mock_gatherer, cache_duration=default_cache_duration)
        
        result = caching.gather()
        
        assert result == "result_1"
        assert mock_gatherer.call_count == 1
    
    def test_second_call_within_cache_returns_cached(self, default_cache_duration):
        """Second call within cache duration should return cached data."""
        mock_gatherer = MockGatherer()
        caching = CachingDataGatherer(mock_gatherer, cache_duration=default_cache_duration)
        
        result1 = caching.gather()
        result2 = caching.gather()
        
        assert result1 == "result_1"
        assert result2 == "result_1"  # Should be the same cached result
        assert mock_gatherer.call_count == 1  # Should only be called once
    
    def test_call_after_cache_expires_fetches_fresh_data(self, short_cache_duration):
        """Call after cache expires should fetch fresh data."""
        mock_gatherer = MockGatherer()
        caching = CachingDataGatherer(mock_gatherer, cache_duration=short_cache_duration)
        
        result1 = caching.gather()
        time.sleep(0.15)  # Wait for cache to expire
        result2 = caching.gather()
        
        assert result1 == "result_1"
        assert result2 == "result_2"  # Should be fresh data
        assert mock_gatherer.call_count == 2  # Should be called twice
    
    def test_multiple_calls_within_cache_return_same_result(self, default_cache_duration):
        """Multiple calls within cache duration should all return cached data."""
        mock_gatherer = MockGatherer()
        caching = CachingDataGatherer(mock_gatherer, cache_duration=default_cache_duration)
        
        result1 = caching.gather()
        result2 = caching.gather()
        result3 = caching.gather()
        
        assert result1 == result2 == result3 == "result_1"
        assert mock_gatherer.call_count == 1  # Should only be called once
    
    def test_get_name_returns_wrapped_gatherer_name(self, default_cache_duration):
        """get_name() should return the wrapped gatherer's name."""
        mock_gatherer = MockGatherer()
        caching = CachingDataGatherer(mock_gatherer, cache_duration=default_cache_duration)
        
        assert caching.get_name() == "MockGatherer"
    
    def test_get_gatherer_returns_wrapped_gatherer(self, default_cache_duration):
        """get_gatherer() should return the wrapped gatherer instance."""
        mock_gatherer = MockGatherer()
        caching = CachingDataGatherer(mock_gatherer, cache_duration=default_cache_duration)
        
        assert caching.get_gatherer() is mock_gatherer


@pytest.mark.unit
class TestDataGatherer:
    """Test suite for DataGatherer base class."""
    
    def test_get_name_returns_class_name(self):
        """get_name() should return the class name."""
        gatherer = MockGatherer()
        assert gatherer.get_name() == "MockGatherer"

