#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Setup complete! Activate venv with: source venv/bin/activate"