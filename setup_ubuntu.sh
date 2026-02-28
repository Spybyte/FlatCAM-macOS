#!/bin/sh -e

# Ubuntu system packages (C libraries and dev headers)

sudo apt-get install -y \
	libfreetype6 \
	libfreetype6-dev \
	libgeos-dev \
	libgdal-dev \
	libpng-dev \
	libspatialindex-dev \
	qt5-style-plugins \
	python3-dev \
	python3-pyqt5 \
	python3-pyqt5.qtopengl \
	python3-tk


# Install uv if not present
if ! command -v uv > /dev/null 2>&1; then
	echo "Installing uv package manager..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Sync Python dependencies via uv
uv sync --extra optimization
