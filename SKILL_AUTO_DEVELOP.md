# Auto-Develop Harness Skill

This skill provides a complete automation framework for AI-driven software development, based on Anthropic's [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

## Concept

The harness enables AI agents (like Claude Code) to work effectively across multiple sessions on complex projects. It solves the problem of limited context windows by:
1. **Initializer Agent** - First session: sets up environment
2. **Coding Agent** - Subsequent sessions: make incremental progress

## Project Structure

```
project/
├── CLAUDE.md              # Main guidance file (this file)
├── prompts/
│   ├── initializer.md     # System prompt for first session
│   ├── coding.md          # System prompt for coding sessions
│   └── task-runner.md    # System prompt for task runner
├── data/
│   ├── tasks.json         # Task queue with pending/completed
│   ├── features.json      # Feature list with pass/fail
│   └── claude-progress.txt # Progress log
├── harness/
│   ├── loop.sh           # Unix loop script
│   ├── loop.ps1          # Windows PowerShell loop script
│   └── run.sh            # Single run script
├── scripts/
│   ├── init.sh           # Dev server startup (Unix)
│   ├── init.bat         # Dev server startup (Windows)
│   └── task-manager.sh  # Task queue management
└── logs/                 # Execution logs
```

## Quick Start

### Windows
```powershell
# Run loop
.\harness\loop.ps1 10

# Run specific task
.\harness\loop.ps1 -TaskId 1

# Dry run
.\harness\loop.ps1 1 -DryRun
```

### Unix/Linux/Git Bash
```bash
# Run loop
./harness/loop.sh 10

# Run specific task
./harness/loop.sh --task-id 1

# Dry run
./harness/loop.sh 1 --dry-run
```

## Workflow

### 1. Initialize Project
- Create project structure (backend/frontend)
- Set up tech stack (FastAPI, React, etc.)
- Initialize git repository
- Create initial commit

### 2. Create Task List
Add tasks to `data/tasks.json`:
```json
{
  "tasks": [
    {"id": 1, "description": "Task description", "status": "pending"}
  ],
  "metadata": {"total": 1, "completed": 0, "pending": 1}
}
```

### 3. Run Development Loop
Each iteration:
1. Read next pending task from `tasks.json`
2. Execute the task (implement feature/fix bug)
3. Test the implementation
4. Commit changes: `git add . && git commit -m "feat: description"`
5. Update task status in `tasks.json`
6. Update progress in `claude-progress.txt`

### 4. Testing Loop
Add Playwright E2E tests:
```bash
# Install Playwright
cd frontend && npm install -D @playwright/test

# Run tests
npx playwright test
```

## Key Scripts

### harness/loop.ps1 (Windows)
PowerShell script for running multiple iterations:
- `-Count N` : Number of iterations
- `-TaskId N`: Run specific task
- `-DryRun`: Preview without executing
- `-Timeout N`: Timeout per iteration (minutes, default: 30)

### harness/loop.sh (Unix)
Bash script with similar options.

### scripts/task-manager.sh
Task queue management:
- `list` - Show all tasks
- `get` - Get next pending task
- `add "description"` - Add new task
- `complete N` - Mark task as completed

## Progress Tracking

### tasks.json
```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Implement feature X",
      "status": "completed",
      "created_at": "2026-02-13T00:00:00Z",
      "completed_at": "2026-02-13T14:30:00Z"
    }
  ],
  "metadata": {"total": 10, "completed": 1, "pending": 9}
}
```

### claude-progress.txt
```
## Session 2026-02-13

### Completed
- Task 1: Implemented feature X

### Notes
- Important context for next session

### Next
- Task 2: Implement feature Y
```

## Best Practices

1. **One task per session** - Don't try to do everything at once
2. **Leave code working** - Always test before committing
3. **Update progress** - Keep tasks.json and progress file current
4. **Use descriptive commits** - Help future sessions understand history
5. **Never remove features** - Only toggle passes field in features.json

## Troubleshooting

### Port Already in Use (Windows)
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill //F //PID <PID>
```

### Playwright Issues
```bash
# Install browsers
npx playwright install chromium

# Run with headed mode
npx playwright test --headed
```

## Adapting to New Projects

1. Copy the harness/ directory
2. Update `prompts/task-runner.md` with project-specific instructions
3. Modify `scripts/init.sh`/`init.bat` for project startup
4. Create initial `data/tasks.json` with project tasks
5. Update `CLAUDE.md` with project details

## Credits

Based on [Anthropic's Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
