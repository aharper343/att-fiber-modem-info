.PHONY: help build build-dev test test-cov clean run push tag-latest docker-build

# Variables
IMAGE_NAME ?= andrew/att-modem-exporter
VERSION ?= $(shell date '+%Y%m%d')
REGISTRY ?= 
NO_CACHE ?= 

# Default target
help:
	@echo "Available targets:"
	@echo "  make build          - Build Docker image (production)"
	@echo "  make build-dev      - Build Docker image with dev dependencies (for testing)"
	@echo "  make test           - Run tests"
	@echo "  make test-cov       - Run tests with coverage report"
	@echo "  make run            - Run the container locally"
	@echo "  make push           - Push image to registry"
	@echo "  make tag-latest     - Tag current version as latest"
	@echo "  make clean          - Clean up Docker images and containers"
	@echo "  make install        - Install development dependencies"
	@echo ""
	@echo "Variables:"
	@echo "  IMAGE_NAME=name     - Override image name (default: $(IMAGE_NAME))"
	@echo "  VERSION=version     - Override version (default: $(VERSION))"
	@echo "  NO_CACHE=--no-cache - Build without cache"

# Build production Docker image
build:
	@echo "Building production image: $(IMAGE_NAME):$(VERSION)"
	docker build $(NO_CACHE) \
		--tag $(IMAGE_NAME):$(VERSION) \
		--tag $(IMAGE_NAME):latest \
		--progress plain \
		.

# Build development Docker image (with test dependencies)
# Note: Requires Dockerfile.dev or modify Dockerfile to use requirements-dev.txt
build-dev:
	@echo "Building development image: $(IMAGE_NAME):$(VERSION)-dev"
	@echo "WARNING: build-dev requires Dockerfile.dev (not included by default)"
	@echo "Use 'make install && make test' for local development instead"

# Run tests locally
test:
	@echo "Running tests..."
	pytest

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	pytest --cov=app --cov-report=html --cov-report=term-missing

# Install development dependencies
install:
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt

# Run the container locally
run:
	@echo "Running container $(IMAGE_NAME):latest"
	docker run --rm -p 8666:8666 \
		-e MODEM_URL=$${MODEM_URL:-http://192.168.1.254} \
		-e MODEM_ACCESS_CODE=$${MODEM_ACCESS_CODE} \
		$(IMAGE_NAME):latest

# Tag version as latest
tag-latest:
	@echo "Tagging $(IMAGE_NAME):$(VERSION) as latest"
	docker tag $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):latest

# Push image to registry
push: tag-latest
	@echo "Pushing $(IMAGE_NAME):$(VERSION) and $(IMAGE_NAME):latest"
	docker push $(IMAGE_NAME):$(VERSION)
	docker push $(IMAGE_NAME):latest

# Clean up Docker resources
clean:
	@echo "Cleaning up Docker resources..."
	docker images $(IMAGE_NAME) -q | xargs -r docker rmi -f
	@echo "Clean complete"

# Lint code (if you add linting tools)
lint:
	@echo "Running linters..."
	@echo "TODO: Add linting tools (flake8, black, mypy, etc.)"

# Format code
format:
	@echo "Formatting code..."
	@echo "TODO: Add formatting tools (black, isort, etc.)"

