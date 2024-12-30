@echo off
echo off

set FLASK_APP=main.py

set FLASK_BIN=.venv\Scripts\flask

start %FLASK_BIN% run --port 80 --host="0.0.0.0" --debug

start http://localhost