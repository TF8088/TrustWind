@echo off
echo off

set Directory_PythonEnv=.env

setlocal enableextensions enabledelayedexpansion

echo ReCreating Python environment...
python -m venv %Directory_PythonEnv%

echo Activating the Python environment
%Directory_PythonEnv%\Scripts\pip install Flask

pause
