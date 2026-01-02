# AT&T Fiber Modem Info Exporter

A Prometheus exporter and REST API for AT&T Fiber modem information, providing real-time metrics and statistics from your modem's web interface.

## Limitations

Tested only with an ARRIS BGW210-700 modem

## Features

- 🔌 **Prometheus Metrics**: Exposes modem statistics in Prometheus format at `/metrics`
- 🌐 **REST API**: JSON endpoints for system information, network status, and broadband statistics
- ⚡ **Caching**: Built-in caching to reduce load on modem interface
- 🐳 **Docker Support**: Containerized for easy deployment
- 📊 **Multiple Data Sources**:
  - System Information (uptime, firmware, hardware details)
  - Home Network Status (LAN port statistics)
  - Broadband Status (WAN connection, IPv4/IPv6 statistics)

## Quick Start

### Using Docker (Recommended)

```bash
# Pull and run
docker run -d \
  --name att-modem-exporter \
  -p 8666:8666 \
  -e MODEM_URL=http://192.168.1.254 \
  -e MODEM_ACCESS_CODE=your-access-code \
  andrew/att-modem-exporter:latest
```

### Using Docker Compose

```bash
# Create .env file
cat > .env << EOF
MODEM_URL=http://192.168.1.254
MODEM_ACCESS_CODE=your-access-code
MODEM_ID=att
EOF

# Start the service
docker-compose up -d
```

### Using Make

```bash
# Build and run
make build
make run
```

### From Source

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MODEM_URL=http://192.168.1.254
export MODEM_ACCESS_CODE=your-access-code

# Run
python app/main.py
```

## Configuration

The application can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEM_URL` | Base URL of the modem web interface | `http://192.168.1.254` |
| `MODEM_ACCESS_CODE` | Access code for the modem (if required) | None |
| `MODEM_ID` | Identifier for the modem | `att` |
| `SERVER_HOSTNAME` | Hostname to bind the server to | `0.0.0.0` |
| `SERVER_PORT` | Port to run the server on | `8666` |

## API Endpoints

### Prometheus Metrics
- **GET** `/metrics` - Prometheus format metrics

### Health & Info
- **GET** `/health` - Health check endpoint
- **GET** `/endpoints` - List all available endpoints

### Data Endpoints
- **GET** `/modems/{modem_id}/system-information` - System information (JSON)
- **GET** `/modems/{modem_id}/home-network-status` - LAN port statistics (JSON)
- **GET** `/modems/{modem_id}/broadband-status` - WAN connection statistics (JSON)

## Prometheus Configuration

Add this to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'att-modem-exporter'
    static_configs:
      - targets: ['localhost:8666']
    scrape_interval: 30s
```

## Project Structure

```
att-fiber-modem-info/
├── app/                      # Application source code
│   ├── gatherers/           # Data gathering framework
│   ├── modem_gatherers/     # Modem-specific data gatherers
│   ├── exporters/           # Data export framework
│   ├── modem_exporters/     # Modem-specific exporters
│   ├── prometheus_exporters/# Prometheus exporters
│   ├── modem_prometheus_mappers/ # Prometheus metric mappers
│   ├── modem_client/        # HTTP client for modem
│   └── server/              # FastAPI server
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── Makefile                # Build automation
└── requirements.txt        # Production dependencies
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

### Quick Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
make test
# or
pytest

# Run with coverage
make test-cov
```

## Building

### Using Make

```bash
make build              # Build Docker image
make build NO_CACHE=--no-cache  # Build without cache
make push               # Push to registry
```

### Using Build Script

```bash
./build.sh              # Build with cache
./build.sh --no-cache   # Build without cache
```

See [BUILD_AUTOMATION.md](BUILD_AUTOMATION.md) for more details.

## Testing

The project includes comprehensive test coverage:

- **Unit Tests**: Fast, isolated component tests
- **Integration Tests**: Component interaction tests
- **E2E Tests**: Full system tests

Run tests:
```bash
pytest                  # Run all tests
pytest tests/unit       # Run unit tests only
pytest --cov=app        # Run with coverage
```

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Code of Conduct

Be kind

## Troubleshooting

### Connection Issues

- Verify `MODEM_URL` is correct and accessible
- Check if modem requires access code
- Ensure network connectivity to modem

### Metrics Not Appearing

- Check `/health` endpoint to verify service is running
- Verify Prometheus can reach the exporter
- Check logs for error messages

### High Resource Usage

- Adjust cache duration if needed
- Reduce scrape interval in Prometheus
- Monitor modem web interface responsiveness

## Support

- Open an issue on GitHub for bug reports or feature requests
- Check existing issues before creating new ones
- Provide logs and configuration details when reporting issues

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Uses [prometheus-client](https://github.com/prometheus/client_python) for metrics
- Parsing done with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

