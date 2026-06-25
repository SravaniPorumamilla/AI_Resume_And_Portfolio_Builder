#!/bin/bash
echo "Installing dependencies..."
pip install streamlit requests

echo ""
echo "Starting app..."
echo "Open browser at: http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""
python3 -m streamlit run app.py
