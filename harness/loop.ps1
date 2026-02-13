# Auto-Develop Loop Script for Windows (PowerShell)
# Runs Claude Code multiple times to execute development tasks

param(
    [int]$Count = 0,
    [int]$TaskId = 0,
    [string]$CustomPrompt = "",
    [switch]$Verbose = $false,
    [switch]$DryRun = $false,
    [int]$Timeout = 30
)

$ErrorActionPreference = "Continue"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$LogDir = "$ProjectDir\logs"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO"    { "Cyan" }
        "WARN"    { "Yellow" }
        "SUCCESS" { "Green" }
        "ERROR"   { "Red" }
        default   { "White" }
    }
    Write-Host "[$Level] $Message" -ForegroundColor $color
}

function Get-NextTask {
    $tasksFile = "$ProjectDir\data\tasks.json"
    if (-not (Test-Path $tasksFile)) {
        return $null
    }
    $data = Get-Content $tasksFile -Raw | ConvertFrom-Json
    $pendingTask = $data.tasks | Where-Object { $_.status -eq "pending" } | Select-Object -First 1
    if ($pendingTask) {
        return $pendingTask.description
    }
    return $null
}

function Get-PendingCount {
    $tasksFile = "$ProjectDir\data\tasks.json"
    $data = Get-Content $tasksFile -Raw | ConvertFrom-Json
    return ($data.tasks | Where-Object { $_.status -eq "pending" }).Count
}

function Get-PromptContent {
    $promptFile = "$ProjectDir\prompts\task-runner.md"
    if (Test-Path $promptFile) {
        return Get-Content $promptFile -Raw
    }
    return ""
}

# Validate count
if ($Count -le 0) {
    Write-Host "Usage: .\loop.ps1 <count> [-TaskId N] [-Prompt 'text'] [-Verbose] [-DryRun] [-Timeout N]"
    Write-Host ""
    Write-Host "Arguments:"
    Write-Host "  count          Number of iterations to run Claude"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -TaskId N      Run specific task ID"
    Write-Host "  -Prompt P      Custom initial prompt"
    Write-Host "  -Verbose       Enable verbose logging"
    Write-Host "  -DryRun        Show what would run without executing"
    Write-Host "  -Timeout N     Timeout per iteration in minutes (default: 30)"
    exit 1
}

Write-Log "==========================================" "INFO"
Write-Log "  Auto-Develop Loop Started" "INFO"
Write-Log "  Iterations: $Count" "INFO"
Write-Log "  Project: $ProjectDir" "INFO"
Write-Log "  Log: $LogDir\loop_$Timestamp.log" "INFO"
Write-Log "==========================================" "INFO"

# Get task
$taskDesc = Get-NextTask

if (-not $taskDesc) {
    Write-Log "No pending tasks found in data/tasks.json" "WARN"
    if ($CustomPrompt) {
        $taskDesc = $CustomPrompt
    } else {
        $taskDesc = "Continue developing the project. Check data/features.json for remaining work."
    }
}

Write-Log "Task: $taskDesc" "INFO"

$pendingCount = Get-PendingCount
if ($pendingCount -eq 0) {
    Write-Log "No more pending tasks!" "WARN"
    exit 0
}

# Build full prompt
$promptContent = Get-PromptContent
$fullPrompt = @"

$promptContent

---

## Current Task

$taskDesc

---

## Instructions

1. First, check the current state of the project
2. Read the specification documents if needed
3. Initialize the project or implement the feature
4. Test thoroughly
5. Commit your changes
6. Update the progress file

Remember to complete the task fully before ending the session.
"@

# Main loop
for ($i = 1; $i -le $Count; $i++) {
    Write-Log "[$i/$Count] ==========================================" "INFO"
    Write-Log "[$i/$Count] Starting iteration..." "INFO"

    if ($DryRun) {
        Write-Log "[DRY-RUN] Would execute Claude with task: $taskDesc" "INFO"
    } else {
        Write-Log "Calling Claude (this may take a while)..." "INFO"

        # Run Claude with the prompt
        $logFile = "$LogDir\iteration_${i}_${Timestamp}.log"

        # Write prompt to temp file
        $tempPromptFile = "$env:TEMP\claude_prompt_$PID.txt"
        $fullPrompt | Out-File -FilePath $tempPromptFile -Encoding UTF8

        # Save current location
        $origLocation = Get-Location

        try {
            Set-Location $ProjectDir

            # Call claude directly with input from file
            # Using --print to get structured output
            $processInfo = New-Object System.Diagnostics.ProcessStartInfo
            $processInfo.FileName = "claude"
            $processInfo.Arguments = "--dangerously-skip-permissions --print"
            $processInfo.RedirectStandardInput = $true
            $processInfo.RedirectStandardOutput = $true
            $processInfo.RedirectStandardError = $true
            $processInfo.UseShellExecute = $false
            $processInfo.CreateNoWindow = $true

            $process = New-Object System.Diagnostics.Process
            $process.StartInfo = $processInfo

            $process.Start() | Out-Null

            # Send the prompt
            $fullPrompt | ForEach-Object { $process.StandardInput.WriteLine($_) }
            $process.StandardInput.Close()

            # Read output with timeout (configurable, default 30 minutes)
            $output = ""
            $timeoutSeconds = [int]$Timeout * 60  # Convert minutes to seconds
            $elapsed = 0

            while (-not $process.HasExited -and $elapsed -lt $timeoutSeconds) {
                Start-Sleep -Seconds 5
                $elapsed += 5
                Write-Host "." -NoNewline
            }

            if (-not $process.HasExited) {
                Write-Log "Timeout reached, killing process..." "WARN"
                $process.Kill()
            }

            $stdout = $process.StandardOutput.ReadToEnd()
            $stderr = $process.StandardError.ReadToEnd()

            $stdout | Out-File -FilePath $logFile -Encoding UTF8
            if ($stderr) {
                $stderr | Out-File -FilePath $logFile -Append -Encoding UTF8
            }

            Write-Log "Claude execution completed" "SUCCESS"

        } catch {
            Write-Log "Error: $_" "ERROR"
        } finally {
            Set-Location $origLocation
            # Clean up
            Remove-Item $tempPromptFile -Force -ErrorAction SilentlyContinue
        }

        # Auto-commit
        Set-Location $ProjectDir
        git add -A 2>$null
        $null = git commit -m "Auto-commit: iteration $i" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Changes committed" "SUCCESS"
        } else {
            Write-Log "No changes to commit" "INFO"
        }
    }

    # Check if there are still pending tasks
    $pendingCount = Get-PendingCount
    if ($pendingCount -eq 0) {
        Write-Log "All tasks completed!" "SUCCESS"
        break
    }
}

Write-Log "==========================================" "INFO"
Write-Log "  Loop Completed" "INFO"
Write-Log "  Total iterations: $($i - 1)" "INFO"
Write-Log "  Log file: $LogDir\loop_$Timestamp.log" "INFO"
Write-Log "==========================================" "INFO"

# Show recent commits
Set-Location $ProjectDir
Write-Log "Recent commits:" "INFO"
git log --oneline -5 2>$null | ForEach-Object { Write-Log "  $_" "INFO" }
