@echo off
REM Auto-Develop Harness - Run Claude Agent (Windows)

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

cd /d "%PROJECT_DIR%"

set INIT_FLAG=
set USER_PROMPT=

REM Parse arguments
:parse_args
if "%~1"=="" goto run_agent
if "%~1"=="--init" (
    set INIT_FLAG=true
    shift
    set USER_PROMPT=%~1
    shift
    goto parse_args
)
if "%~1"=="--prompt" (
    shift
    set USER_PROMPT=%~1
    shift
    goto parse_args
)
set USER_PROMPT=%~1
shift
goto parse_args

:run_agent
if defined INIT_FLAG (
    echo === Running Initializer Agent ===
    set PROMPT_FILE=%SCRIPT_DIR%..\prompts\initializer.md
) else (
    echo === Running Coding Agent ===
    set PROMPT_FILE=%SCRIPT_DIR%..\prompts\coding.md
)

if not exist "%PROMPT_FILE%" (
    echo Error: Prompt file not found: %PROMPT_FILE%
    exit /b 1
)

REM Check if first run (no git)
if not exist ".git" (
    echo First run detected - running initializer
    set INIT_FLAG=true
    set PROMPT_FILE=%SCRIPT_DIR%..\prompts\initializer.md
)

REM Run Claude with the prompt
REM Note: Adjust claude command based on your installation
type "%PROMPT_FILE%" | claude --dangerously-skip-permissions

echo === Session Complete ===
echo Remember to:
echo   1. Commit your changes: git add . && git commit -m "Description"
echo   2. Update progress: Edit data\claude-progress.txt
echo   3. Update features: Edit data\features.json
