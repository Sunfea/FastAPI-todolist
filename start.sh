#!/bin/bash
# Simple startup script for the Todo API

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting the Todo API server..."
python main.py