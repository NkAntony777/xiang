@echo off
REM ========================================
REM 60 Jiazi Encyclopedia - Stop Services
REM ========================================

echo.
echo ========================================
echo   Stopping all services
echo ========================================
echo.

echo Stopping backend...
taskkill /F /FI "IMAGENAME eq python.exe" >nul 2>&1

echo Stopping frontend...
taskkill /F /FI "IMAGENAME eq node.exe" >nul 2>&1

echo.
echo ========================================
echo   All services stopped
echo ========================================
echo.

pause
