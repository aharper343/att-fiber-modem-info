"""
Unit tests for ModemClient and ModemConfig.

These tests mock external dependencies (HTTP requests) to test
the client logic in isolation.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from requests.exceptions import Timeout, ConnectionError, RequestException

from modem_client import ModemClient, ModemConfig


@pytest.mark.unit
class TestModemConfig:
    """Test suite for ModemConfig."""
    
    def test_init_creates_config_with_valid_values(self):
        """Config should be created with provided values."""
        config = ModemConfig(id="test-id", url="http://test.com", access_code="code")
        
        assert config.id == "test-id"
        assert config.url == "http://test.com"
        assert config.access_code == "code"
    
    def test_init_raises_error_when_id_missing(self):
        """Config should raise ValueError when id is empty."""
        with pytest.raises(ValueError, match="id is required"):
            ModemConfig(id="", url="http://test.com", access_code="code")
        
        with pytest.raises(ValueError, match="id is required"):
            ModemConfig(id=None, url="http://test.com", access_code="code")
    
    def test_init_raises_error_when_url_missing(self):
        """Config should raise ValueError when url is empty."""
        with pytest.raises(ValueError, match="url is required"):
            ModemConfig(id="test", url="", access_code="code")
        
        with pytest.raises(ValueError, match="url is required"):
            ModemConfig(id="test", url=None, access_code="code")
    
    @patch.dict('os.environ', {
        'MODEM_ID': 'env-id',
        'MODEM_URL': 'http://env-url.com',
        'MODEM_ACCESS_CODE': 'env-code'
    })
    def test_from_env_reads_environment_variables(self):
        """from_env() should read values from environment variables."""
        config = ModemConfig.from_env()
        
        assert config.id == "env-id"
        assert config.url == "http://env-url.com"
        assert config.access_code == "env-code"
    
    @patch.dict('os.environ', {}, clear=True)
    def test_from_env_uses_defaults_when_env_not_set(self):
        """from_env() should use defaults when environment variables are not set."""
        config = ModemConfig.from_env()
        
        assert config.id == "att"
        assert config.url == "http://192.168.1.254"
        assert config.access_code is None


@pytest.mark.unit
class TestModemClient:
    """Test suite for ModemClient."""
    
    def test_init_creates_client_with_config(self, modem_config):
        """Client should be initialized with provided config."""
        client = ModemClient(modem_config)
        
        assert client.config is modem_config
        assert client.nonce is None
        assert client.logged_in is False
        assert client.session is not None
    
    @patch('modem_client.requests.Session')
    def test_fetch_makes_http_request(self, mock_session_class, modem_config, mock_response):
        """_fetch() should make an HTTP GET request to the correct URL."""
        mock_session = Mock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = ModemClient(modem_config)
        response = client._fetch("/test/path")
        
        mock_session.get.assert_called_once_with(
            "http://192.168.1.254/test/path",
            timeout=10
        )
        assert response is mock_response
    
    @patch('modem_client.BeautifulSoup')
    @patch('modem_client.requests.Session')
    def test_fetch_extracts_nonce_from_response(self, mock_session_class, mock_bs, modem_config, mock_response):
        """_fetch() should extract nonce from HTML response."""
        mock_session = Mock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # Mock BeautifulSoup to return a nonce input
        mock_soup = Mock()
        mock_nonce_tag = Mock()
        mock_nonce_tag.get.return_value = "nonce-value"
        mock_nonce_tag.__getitem__ = Mock(return_value="nonce-value")
        mock_soup.find.return_value = mock_nonce_tag
        mock_bs.return_value = mock_soup
        
        client = ModemClient(modem_config)
        client._fetch("/test/path")
        
        assert client.nonce == "nonce-value"
    
    @patch('modem_client.requests.Session')
    def test_fetch_handles_timeout(self, mock_session_class, modem_config):
        """_fetch() should handle timeout errors."""
        mock_session = Mock()
        mock_session.get.side_effect = Timeout("Connection timeout")
        mock_session_class.return_value = mock_session
        
        client = ModemClient(modem_config)
        
        with pytest.raises(Timeout):
            client._fetch("/test/path")
    
    @patch('modem_client.requests.Session')
    def test_fetch_handles_connection_error(self, mock_session_class, modem_config):
        """_fetch() should handle connection errors."""
        mock_session = Mock()
        mock_session.get.side_effect = ConnectionError("Connection failed")
        mock_session_class.return_value = mock_session
        
        client = ModemClient(modem_config)
        
        with pytest.raises(ConnectionError):
            client._fetch("/test/path")
    
    @patch('modem_client.requests.Session')
    def test_fetch_handles_request_exception(self, mock_session_class, modem_config):
        """_fetch() should handle general request exceptions."""
        mock_session = Mock()
        mock_session.get.side_effect = RequestException("Request failed")
        mock_session_class.return_value = mock_session
        
        client = ModemClient(modem_config)
        
        with pytest.raises(RequestException):
            client._fetch("/test/path")

