@echo off
echo off

set Directory_PythonEnv=.venv

setlocal enableextensions enabledelayedexpansion

echo ReCreating Python environment...
python -m venv %Directory_PythonEnv%

echo Activating the Python environment
%Directory_PythonEnv%\Scripts\pip install Flask

echo installing .environment
%Directory_PythonEnv%\Scripts\pip install -r requirements.txt

pause
