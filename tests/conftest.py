"""
Pytest configuration and shared fixtures.

This file is automatically discovered by pytest and provides:
- Shared fixtures for all tests
- Test configuration
- Common test utilities
"""
import sys
from pathlib import Path

# Add app directory to Python path for imports
APP_DIR = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(APP_DIR))

import pytest
from unittest.mock import Mock, MagicMock
from datetime import timedelta

from modem_client import ModemClient, ModemConfig
from gatherers import DataGatherer


@pytest.fixture
def modem_config():
    """Create a test ModemConfig."""
    return ModemConfig(
        id="test-modem",
        url="http://192.168.1.254",
        access_code="test-code"
    )


@pytest.fixture
def mock_modem_client(modem_config):
    """Create a mock ModemClient."""
    client = Mock(spec=ModemClient)
    client.config = modem_config
    return client


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    response = Mock()
    response.text = "<html><body>Test HTML</body></html>"
    response.status_code = 200
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def mock_gatherer():
    """Create a mock DataGatherer."""
    gatherer = Mock(spec=DataGatherer)
    gatherer.get_name.return_value = "MockGatherer"
    gatherer.gather.return_value = {"test": "data"}
    return gatherer


@pytest.fixture
def short_cache_duration():
    """Short cache duration for testing."""
    return timedelta(milliseconds=100)


@pytest.fixture
def default_cache_duration():
    """Default cache duration for testing."""
    return timedelta(seconds=5)

