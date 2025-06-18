#!/bin/bash

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e .

echo "Development installation complete!"
echo "Run your command with: summarize-youtube" 