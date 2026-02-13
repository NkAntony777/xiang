@echo off
REM ========================================
REM 六十甲子象意百科查询系统 - 一键启动
REM ========================================

echo.
echo ========================================
echo   六十甲子象意百科查询系统
echo   一键启动脚本
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

echo [1/4] 安装后端依赖...
cd /d "%~dp0backend"
pip install -r requirements.txt -q

echo [2/4] 安装前端依赖...
cd /d "%~dp0frontend"
call npm install

echo.
echo [3/4] 启动后端服务器 (端口 8000)...
start "Backend - FastAPI" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [4/4] 启动前端服务器 (端口 5173)...
start "Frontend - Vite" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo   启动完成！
echo.
echo   后端: http://localhost:8000
echo   前端: http://localhost:5173
echo   API文档: http://localhost:8000/docs
echo ========================================
echo.
echo   按任意键打开浏览器访问...
echo.

pause >nul

start http://localhost:5173
