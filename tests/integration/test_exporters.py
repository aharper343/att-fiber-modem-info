"""
Integration tests for exporters.

These tests verify that exporters work correctly with gatherers
and produce expected output formats.
"""
import pytest
from unittest.mock import Mock, MagicMock

from exporters import DataGathererExporter
from modem_exporters import ModemDataGathererExporter
from gatherers import DataGatherer, CachingDataGatherer


class MockGatherer(DataGatherer):
    """Mock gatherer for integration testing."""
    
    def __init__(self, name="MockGatherer", data=None):
        self._name = name
        self._data = data or {"test": "data"}
    
    def gather(self):
        return self._data
    
    def get_name(self):
        return self._name


@pytest.mark.integration
class TestDataGathererExporter:
    """Integration tests for DataGathererExporter."""
    
    def test_export_returns_gatherer_data(self):
        """export() should return data from the gatherer."""
        gatherer = MockGatherer(data={"key": "value"})
        exporter = DataGathererExporter(gatherer)
        
        result = exporter.export()
        
        assert result == {"key": "value"}
    
    def test_export_returns_dict_from_typed_dict(self):
        """export() should convert TypedDict to dict."""
        from typing import TypedDict
        
        class TestData(TypedDict):
            field: str
        
        data = TestData(field="value")
        gatherer = MockGatherer(data=data)
        exporter = DataGathererExporter(gatherer)
        
        result = exporter.export()
        
        assert isinstance(result, dict)
        assert result["field"] == "value"
    
    def test_get_name_includes_gatherer_name(self):
        """get_name() should include the gatherer's name."""
        gatherer = MockGatherer(name="TestGatherer")
        exporter = DataGathererExporter(gatherer)
        
        name = exporter.get_name()
        
        assert "TestGatherer" in name
        assert exporter.__class__.__name__ in name


@pytest.mark.integration
class TestModemDataGathererExporter:
    """Integration tests for ModemDataGathererExporter."""
    
    def test_works_with_caching_gatherer(self, modem_config):
        """Should work correctly with CachingDataGatherer wrapper."""
        from modem_client import ModemClient
        from modem_gatherers import ModemClientDataGatherer
        
        # Create a mock gatherer that acts like ModemClientDataGatherer
        mock_gatherer = Mock(spec=ModemClientDataGatherer)
        mock_gatherer.get_name.return_value = "TestGatherer"
        mock_gatherer.gather.return_value = {"test": "data"}
        
        # Mock get_client_config
        mock_gatherer.get_client_config.return_value = modem_config
        
        # Wrap in cache
        cached = CachingDataGatherer(mock_gatherer)
        
        # Create exporter
        exporter = ModemDataGathererExporter(cached)
        
        # Should not raise
        assert exporter is not None
        assert exporter._modem_id == modem_config.id

