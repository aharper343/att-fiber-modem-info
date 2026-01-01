#!/bin/bash
# Build script for att-fiber-modem-exporter Docker image
#
# Usage:
#   ./build.sh              - Build with cache
#   ./build.sh --no-cache   - Build without cache
#   ./build.sh --help       - Show help

set -e  # Exit on error

IMAGE_NAME="andrew/att-modem-exporter"
VERSION=$(date '+%Y%m%d')
BUILD_ARGS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-cache)
            BUILD_ARGS="--no-cache"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --no-cache    Build without using cache"
            echo "  --help, -h    Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  IMAGE_NAME    Override image name (default: $IMAGE_NAME)"
            echo "  VERSION       Override version (default: $VERSION)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Allow override via environment variables
IMAGE_NAME=${IMAGE_NAME:-$IMAGE_NAME}
VERSION=${VERSION:-$(date '+%Y%m%d')}

echo "========================================="
echo "Building Docker Image"
echo "========================================="
echo "Image: $IMAGE_NAME"
echo "Version: $VERSION"
echo "Build args: $BUILD_ARGS"
echo "========================================="

# Show existing images
echo ""
echo "Existing images:"
docker images "$IMAGE_NAME" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" || true

# Build image
echo ""
echo "Building image..."
docker build $BUILD_ARGS \
    --tag "$IMAGE_NAME:$VERSION" \
    --tag "$IMAGE_NAME:latest" \
    --progress plain \
    .

# Show results
echo ""
echo "========================================="
echo "Build complete!"
echo "========================================="
echo ""
echo "New images:"
docker images "$IMAGE_NAME" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo ""
echo "To run the container:"
echo "  docker run --rm -p 8666:8666 $IMAGE_NAME:latest"
echo ""
echo "To push to registry:"
echo "  docker push $IMAGE_NAME:$VERSION"
echo "  docker push $IMAGE_NAME:latest"
