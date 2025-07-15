#!/bin/bash
set -e

echo "Building web_search function..."

# Create virtual environment
virtualenv --without-pip virtualenv

# Install dependencies
pip install -r requirements.txt --target virtualenv/lib/python3.11/site-packages

echo "Build complete"
