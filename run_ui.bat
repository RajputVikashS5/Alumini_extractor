@echo off
REM Batch script to launch Streamlit UI on Windows

echo.
echo ======================================================
echo   Alumni Data Extractor - Web UI Launcher
echo ======================================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
    echo.
) else (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Streamlit not installed!
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Launch Streamlit
echo Starting Streamlit application...
echo The web interface will open at: http://localhost:8501
echo.
python -m streamlit run ui/app.py --logger.level=info --client.showErrorDetails=true

pause
