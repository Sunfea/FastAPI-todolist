@echo off
REM Simple startup script for the Todo API on Windows

echo Installing dependencies...
pip install -r requirements.txt

echo Starting the Todo API server...
python main.py