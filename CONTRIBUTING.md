# Contributing to AT&T Fiber Modem Info Exporter

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Be kind

## How to Contribute

### Reporting Bugs

Before creating a bug report, please:
1. Check if the issue already exists
2. Verify you're using the latest version
3. Collect relevant information (logs, configuration, steps to reproduce)

When reporting bugs, include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Docker version if applicable)
- Relevant logs or error messages
- Configuration (with sensitive data redacted)

### Suggesting Enhancements

Enhancement suggestions should include:
- Clear description of the proposed feature
- Use case or problem it solves
- Potential implementation approach (if you have ideas)
- Examples or mockups (if applicable)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the coding style (see below)
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure all tests pass

4. **Commit your changes**
   - Use clear, descriptive commit messages
   - Follow conventional commit format when possible:
     ```
     feat: add new data gatherer for signal strength
     fix: correct port label mapping in metrics
     docs: update README with new configuration options
     test: add integration tests for exporter
     ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure CI tests pass

## Development Setup

### Prerequisites

- Python 3.11 or 3.12
- pip
- Docker (optional, for containerized development)
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd att-fiber-modem-info
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run tests to verify setup**
   ```bash
   pytest
   ```

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Maximum line length: 100 characters (soft limit)
- Use meaningful variable and function names

### Code Organization

- Keep functions small and focused
- Use abstract base classes for extensibility
- Separate concerns (gathering, exporting, mapping)
- Add docstrings to classes and functions

### Example

```python
from typing import Optional
from datetime import timedelta

class MyGatherer(DataGatherer):
    """Brief description of what this gatherer does.
    
    Longer description if needed, explaining behavior,
    parameters, return values, etc.
    """
    
    def gather(self) -> Optional[dict]:
        """Gather data from source.
        
        Returns:
            Dictionary containing gathered data, or None if unavailable.
        """
        # Implementation
        pass
```

## Testing Guidelines

### Test Requirements

- All new features must include tests
- Bug fixes should include regression tests
- Maintain or improve code coverage
- Tests should be fast, isolated, and repeatable

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_gatherers.py

# Run specific test
pytest tests/unit/test_gatherers.py::TestCachingDataGatherer::test_first_call_fetches_data

# Run with verbose output
pytest -v
```

### Writing Tests

- Use descriptive test names: `test_<what>_<condition>_<expected_result>`
- Arrange-Act-Assert pattern
- Mock external dependencies (network, filesystem)
- Use fixtures from `conftest.py` for common setup

### Test Structure

```python
@pytest.mark.unit
class TestMyComponent:
    """Test suite for MyComponent."""
    
    def test_behavior_under_normal_conditions(self, fixture):
        """Test description."""
        # Arrange
        obj = MyComponent()
        
        # Act
        result = obj.method()
        
        # Assert
        assert result == expected_value
```

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing information.

## Documentation

### Code Documentation

- Add docstrings to all public classes and functions
- Use type hints for function signatures
- Include examples in docstrings for complex functions

### User Documentation

- Update README.md for user-facing changes
- Add/update docstrings for API changes
- Update examples if behavior changes

## Git Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions/updates

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- First line should be concise (< 50 characters)
- Add body for detailed explanation if needed
- Reference issues with `#issue-number`

Example:
```
feat: add signal strength metric to system information

Adds signal strength measurement to the system information
gatherer and exposes it as a Prometheus gauge metric.

Fixes #42
```

## Review Process

1. **Automated Checks**
   - All tests must pass
   - Code must pass linting (if configured)
   - Coverage must not decrease significantly

2. **Code Review**
   - At least one maintainer will review
   - Address review feedback promptly
   - Be open to suggestions and discussion

3. **Merge**
   - Maintainer will merge after approval
   - PR will be squashed if needed
   - Your contribution will be attributed in git history

## Project Structure

Understanding the project structure helps with contributions:

- `app/gatherers/` - Data gathering framework (abstract base classes)
- `app/modem_gatherers/` - Modem-specific data gatherers
- `app/exporters/` - Data export framework
- `app/prometheus_exporters/` - Prometheus export logic
- `app/modem_prometheus_mappers/` - Maps gathered data to Prometheus metrics
- `app/server/` - FastAPI server and routing
- `tests/` - Test suite mirroring source structure

## Adding New Features

### Adding a New Data Gatherer

1. Create gatherer class in `app/modem_gatherers/`
2. Implement `ModemClientDataGatherer`
3. Create TypedDict for return type
4. Add tests in `tests/unit/test_modem_gatherers.py`
5. Register in `app/main.py` if needed

### Adding a New Exporter

1. Create exporter class in `app/exporters/` or `app/modem_exporters/`
2. Implement `DataExporter` interface
3. Add tests
4. Register in server initialization

### Adding Prometheus Metrics

1. Create mapper in `app/modem_prometheus_mappers/`
2. Extend `PrometheusModemMapper`
3. Implement `_map()` method
4. Add tests for metric creation and values
5. Register mapper in `app/main.py`

## Questions?

- Open an issue for questions
- Check existing issues and discussions
- Review existing code for patterns and examples

Thank you for contributing! 🎉

