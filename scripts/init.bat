@echo off
REM Init Script - Start Development Server (Windows)

echo === Starting Development Environment ===

REM Detect project type
if exist package.json (
    echo Detected Node.js project

    if not exist node_modules (
        echo Installing dependencies...
        call npm install
    )

    echo Starting dev server...
    start /b npm run dev

    timeout /t 5 /nobreak >nul
    echo Dev server started

) else if exist requirements.txt (
    echo Detected Python project

    if not exist venv (
        echo Creating virtual environment...
        python -m venv venv
    )

    call venv\Scripts\activate.bat
    pip install -r requirements.txt

    echo Starting dev server...
    start /b python manage.py runserver

    echo Dev server started at http://localhost:8000

) else if exist pyproject.toml (
    echo Detected Python project (Poetry)

    if not exist venv (
        echo Creating virtual environment...
        poetry env use python
    )

    poetry install
    echo Starting dev server...
    start /b poetry run python manage.py runserver

) else (
    echo Unknown project type. Please customize init.bat for your project.
    exit /b 1
)

echo === Environment Ready ===
