@echo off
echo ========================================
echo  AI Budget ^& Expense Advisor - Startup
echo ========================================

cd /d "%~dp0"

REM Check for virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    REM Check if Python is available
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python not found. Install Python 3.10+ first.
        pause
        exit /b 1
    )
    REM Install dependencies if not already installed
    echo [1/2] Checking Python dependencies...
    python -m pip install -r backend/requirements.txt --quiet
)

REM Start FastAPI Backend
echo.
echo [1/2] Starting FastAPI Backend on http://localhost:8000 ...
start "AI Advisor Backend" cmd /k "cd /d ""%~dp0"" && if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat && cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak >nul

REM Start Frontend HTTP Server
echo [2/2] Starting Frontend Server on http://localhost:5500 ...
start "AI Advisor Frontend" cmd /k "cd /d ""%~dp0"" && if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat && python -m http.server 5500 --directory frontend"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo  Application Started!
echo ========================================
echo  Frontend:  http://localhost:5500
echo  Backend:   http://localhost:8000
echo  API Docs:  http://localhost:8000/docs
echo  Health:    http://localhost:8000/api/v1/health
echo ========================================
echo.
echo Opening browser...
start http://localhost:5500

echo Press any key to exit launcher.
pause >nul
