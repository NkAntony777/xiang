@echo off
REM ========================================
REM 六十甲子象意百科查询系统 - 停止服务
REM ========================================

echo.
echo ========================================
echo   停止所有服务
echo ========================================
echo.

REM 杀死 Python 进程 (uvicorn)
echo 正在停止后端服务...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq uvicorn.exe" >nul 2>&1

REM 杀死 Node.js 进程 (vite)
echo 正在停止前端服务...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq Frontend*" >nul 2>&1

echo.
echo ========================================
echo   所有服务已停止
echo ========================================
echo.

pause
