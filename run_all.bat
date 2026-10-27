@echo off
setlocal enabledelayedexpansion

REM Change to the directory of this script (project root)
cd /d "%~dp0"

REM Ensure virtual environment exists
if not exist "venv\Scripts\activate.bat" (
  echo [Setup] Creating virtual environment in venv\ ...
  py -3 -m venv venv
)

REM Activate virtual environment
call "venv\Scripts\activate.bat"

REM Ensure required packages are installed (basic check)
if not exist "venv\Lib\site-packages\fastapi\__init__.py" (
  echo [Setup] Installing backend dependencies...
  python -m pip install --upgrade pip
  python -m pip install -r Backend\requirements.txt
)
if not exist "venv\Scripts\streamlit.exe" (
  echo [Setup] Installing frontend dependencies...
  python -m pip install streamlit reportlab requests
)

REM Start Backend (FastAPI) in new window
start "CareerRecommender-Backend" cmd /k python -m Backend.main

REM Start Frontend (Streamlit) in new window
start "CareerRecommender-Frontend" cmd /k streamlit run Frontend\app.py

echo Started Backend and Frontend in separate windows.
exit /b 0


