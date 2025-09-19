@echo off
REM Setup virtual environment and install dependencies

echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Virtual environment and dependencies set up!
echo To activate later, run:
echo     .venv\Scripts\activate
echo ========================================
pause
