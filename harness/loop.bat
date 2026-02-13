@echo off
REM Auto-Develop Loop Script for Windows
REM Runs Claude Code multiple times to execute development tasks
REM Usage: loop.bat [count] [options]

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."
set "LOG_DIR=%PROJECT_DIR%\logs"
set "TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

set "COUNT="
set "TASK_ID="
set "CUSTOM_PROMPT="
set "VERBOSE="
set "DRY_RUN="

:parse_args
if "%~1"=="" goto run_loop
if "%~1"=="--task-id" (
    set "TASK_ID=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--prompt" (
    set "CUSTOM_PROMPT=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--verbose" (
    set "VERBOSE=1"
    shift
    goto parse_args
)
if "%~1"=="--dry-run" (
    set "DRY_RUN=1"
    shift
    goto parse_args
)
if "%~1"=="-h" goto usage
if "%~1"=="--help" goto usage
set "COUNT=%~1"
shift
goto parse_args

:usage
echo Usage: %~nx0 [count] [options]
echo.
echo Arguments:
echo   count          Number of iterations to run Claude
echo.
echo Options:
echo   --task-id N    Run specific task ID
echo   --prompt P    Custom initial prompt
echo   --verbose     Enable verbose logging
echo   --dry-run     Show what would run without executing
exit /b 1

:run_loop
if "%COUNT%"=="" (
    echo Error: Count argument is required
    goto usage
)

echo [INFO] ==========================================
echo [INFO]   Auto-Develop Loop Started
echo [INFO]   Iterations: %COUNT%
echo [INFO]   Project: %PROJECT_DIR%
echo [INFO]   Log: %LOG_DIR%\loop_%TIMESTAMP%.log
echo [INFO] ==========================================

REM Get task from tasks.json using Python
set "TASK_JSON_FILE=%PROJECT_DIR%\data\tasks.json"
set "TASK_JSON_FILE=%TASK_JSON_FILE:\=\\%"

set "TASK_DESC="
for /f "delims=" %%i in ('python -c "import json; f=open(r'%TASK_JSON_FILE%','r',encoding='utf-8'); d=json.load(f); print([t['description'] for t in d['tasks'] if t['status']=='pending'][0] if [t for t in d['tasks'] if t['status']=='pending'] else '')"') do set "TASK_DESC=%%i"

if "%TASK_DESC%"=="" (
    echo [WARN] No pending tasks found in data/tasks.json
    if defined CUSTOM_PROMPT (
        set "TASK_DESC=%CUSTOM_PROMPT%"
    ) else (
        set "TASK_DESC=Continue developing the project. Check data/features.json for remaining work."
    )
)

echo [INFO] Task: %TASK_DESC%

REM Count pending tasks
set "PENDING_COUNT=0"
for /f %%i in ('python -c "import json; f=open(r'%TASK_JSON_FILE%','r',encoding='utf-8'); d=json.load(f); print(len([t for t in d['tasks'] if t['status']=='pending']))"') do set "PENDING_COUNT=%%i"

if "%PENDING_COUNT%"=="0" (
    echo [WARN] No more pending tasks!
    goto end_loop
)

REM Run the loop
set "CURRENT_ITER=1"

:loop_start
if %CURRENT_ITER% GTR %COUNT% goto end_loop

echo [PROGRESS] [%CURRENT_ITER%/%COUNT%] ==========================================
echo [PROGRESS] [%CURRENT_ITER%/%COUNT%] Starting iteration...

REM Build prompt content
set "PROMPT_FILE=%PROJECT_DIR%\prompts\task-runner.md"

REM Read prompt file into a variable
set "PROMPT_CONTENT="
for /f "usebackq delims=" %%a in ("%PROMPT_FILE%") do (
    set "PROMPT_CONTENT=!PROMPT_CONTENT!%%a^n"
)

REM Add task description to prompt
set "FULL_PROMPT=%PROMPT_CONTENT%^n^n---^n^n## Current Task^n^n%TASK_DESC%"

if defined DRY_RUN (
    echo [INFO] [DRY-RUN] Would execute Claude with task: %TASK_DESC%
    goto after_claude
)

REM Run Claude - use --dangerously-skip-permissions to avoid prompts
echo [INFO] Calling Claude...
echo.
echo %FULL_PROMPT% | claude --dangerously-skip-permissions >> "%LOG_DIR%\iteration_%CURRENT_ITER%_%TIMESTAMP%.log" 2>&1
set "CLAUDE_EXIT_CODE=!ERRORLEVEL!"

if !CLAUDE_EXIT_CODE! EQU 0 (
    Claude completed echo [SUCCESS] successfully
) else (
    echo [ERROR] Claude exited with code !CLAUDE_EXIT_CODE!
)

:after_claude
REM Auto-commit if not dry-run
if not defined DRY_RUN (
    cd /d "%PROJECT_DIR%"
    git add -A >nul 2>&1
    git commit -m "Auto-commit: iteration %CURRENT_ITER%" >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [SUCCESS] Changes committed
    ) else (
        echo [INFO] No changes to commit
    )
)

set /a CURRENT_ITER+=1
goto loop_start

:end_loop
echo [INFO] ==========================================
echo [INFO]   Loop Completed
echo [INFO]   Total iterations: %COUNT%
echo [INFO]   Log file: %LOG_DIR%\loop_%TIMESTAMP%.log
echo [INFO] ==========================================

REM Show recent commits
cd /d "%PROJECT_DIR%"
echo [INFO] Recent commits:
git log --oneline -5 2>nul

endlocal
