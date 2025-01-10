@echo off
echo off

set Directory_PythonEnv=.venv

setlocal enableextensions enabledelayedexpansion

echo ReCreating Python environment...
python -m venv %Directory_PythonEnv%

echo Activating the Python environment
%Directory_PythonEnv%\Scripts\pip install Flask

echo installing .environment
%Directory_PythonEnv%\Scripts\pip install python-dotenv
%Directory_PythonEnv%\Scripts\pip install requests
%Directory_PythonEnv%\Scripts\pip install flask_mail


pause
