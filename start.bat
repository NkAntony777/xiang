@echo off
REM ========================================
REM 60 Jiazi Encyclopedia - One Click Start
REM ========================================

echo.
echo ========================================
echo   60 Jiazi Image Encyclopedia
echo   One Click Start
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo [1/4] Installing backend dependencies...
cd /d "%~dp0backend"
pip install -r requirements.txt -q

echo [2/4] Installing frontend dependencies...
cd /d "%~dp0frontend"
call npm install

echo.
echo [3/4] Starting backend server (port 8000)...
start "Backend" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [4/4] Starting frontend server (port 5173)...
start "Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo   Started successfully!
echo.
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo ========================================
echo.

pause
