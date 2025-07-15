#!/bin/bash
set -e

echo "Building run_sql_query function..."

# Remove any existing virtual environment
rm -rf virtualenv

# Create virtual environment
virtualenv --without-pip virtualenv

# Install dependencies with --upgrade to force replacement
pip install -r requirements.txt --target virtualenv/lib/python3.11/site-packages --upgrade

echo "Build complete"