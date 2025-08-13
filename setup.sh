#!/bin/bash

# Auto-detect architecture and set DOCKER_ARCH environment variable
ARCH=$(uname -m)
case $ARCH in
  x86_64)
    export DOCKER_ARCH=amd64
    echo "Detected x86_64 architecture - using Dockerfile.amd64"
    ;;
  aarch64|arm64)
    export DOCKER_ARCH=arm64
    echo "Detected ARM64 architecture - using Dockerfile.arm64"
    ;;
  *)
    echo "Unknown architecture: $ARCH, defaulting to amd64"
    export DOCKER_ARCH=amd64
    ;;
esac

# Build with docker compose
docker compose build