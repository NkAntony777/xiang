#!/bin/bash

# Auto-Develop Loop Script
# Runs Claude Code multiple times to execute development tasks
#
# Usage: ./loop.sh <count>
#   count: number of iterations (how many times to call Claude)

set -e

# Colors for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

cd "$PROJECT_DIR"

# Create log directory
mkdir -p "$LOG_DIR"

# Usage function
usage() {
    echo "Usage: $0 <count> [options]"
    echo ""
    echo "Arguments:"
    echo "  count          Number of iterations to run Claude"
    echo ""
    echo "Options:"
    echo "  --task-id N   Run specific task ID (default: next pending task)"
    echo "  --prompt P    Custom initial prompt"
    echo "  --verbose     Enable verbose logging"
    echo "  --dry-run     Show what would run without executing"
    exit 1
}

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" >> "$LOG_DIR/loop_${TIMESTAMP}.log"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SUCCESS] $1" >> "$LOG_DIR/loop_${TIMESTAMP}.log"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1" >> "$LOG_DIR/loop_${TIMESTAMP}.log"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >> "$LOG_DIR/loop_${TIMESTAMP}.log"
}

log_progress() {
    echo -e "${BLUE}[PROGRESS]${NC} [$1/$2] $3"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [PROGRESS] [$1/$2] $3" >> "$LOG_DIR/loop_${TIMESTAMP}.log"
}

# Parse arguments
COUNT=""
TASK_ID=""
CUSTOM_PROMPT=""
VERBOSE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        --task-id)
            TASK_ID="$2"
            shift 2
            ;;
        --prompt)
            CUSTOM_PROMPT="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            if [[ -z "$COUNT" ]]; then
                COUNT="$1"
            else
                log_error "Unknown argument: $1"
                usage
            fi
            shift
            ;;
    esac
done

# Validate count
if [[ -z "$COUNT" ]]; then
    log_error "Count argument is required"
    usage
fi

if ! [[ "$COUNT" =~ ^[0-9]+$ ]] || [ "$COUNT" -lt 1 ]; then
    log_error "Count must be a positive number"
    usage
fi

log_info "=========================================="
log_info "  Auto-Develop Loop Started"
log_info "  Iterations: $COUNT"
log_info "  Project: $PROJECT_DIR"
log_info "  Log: $LOG_DIR/loop_${TIMESTAMP}.log"
log_info "=========================================="

# Get task to work on
get_task() {
    if [ -n "$TASK_ID" ]; then
        # Get specific task
        node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/tasks.json', 'utf8'));
const task = data.tasks.find(t => t.id == $TASK_ID);
if (task) {
    console.log(task.description);
} else {
    console.log('');
}
" 2>/dev/null || echo ""
    else
        # Get next pending task
        node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/tasks.json', 'utf8'));
const task = data.tasks.find(t => t.status === 'pending');
if (task) {
    console.log(task.description);
} else {
    console.log('');
}
" 2>/dev/null || echo ""
    fi
}

# Check if there are pending tasks
check_pending_tasks() {
    node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/tasks.json', 'utf8'));
const pending = data.tasks.filter(t => t.status === 'pending').length;
console.log(pending);
" 2>/dev/null || echo "0"
}

# Mark task as completed
mark_task_completed() {
    local task_id="$1"
    node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/tasks.json', 'utf8'));
const task = data.tasks.find(t => t.id == $task_id);
if (task) {
    task.status = 'completed';
    task.completed_at = new Date().toISOString();
    data.metadata.completed++;
    data.metadata.pending--;
    fs.writeFileSync('data/tasks.json', JSON.stringify(data, null, 2));
    console.log('Task $task_id marked as completed');
} else {
    console.log('Task $task_id not found');
}
" 2>/dev/null || true
}

# Check if all features are done
check_all_features_done() {
    node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/features.json', 'utf8'));
const allFeatures = data.features || data;
const allDone = allFeatures.every(f => f.passes === true);
console.log(allDone ? 'true' : 'false');
" 2>/dev/null || echo "false"
}

# Auto-commit function
auto_commit() {
    # Check if there are changes to commit
    if git diff --quiet && git diff --cached --quiet; then
        log_info "No changes to commit"
        return 0
    fi

    # Get git status for commit message
    local changed_files=$(git diff --name-only | head -5)
    local commit_msg="Auto-commit: $(date '+%Y-%m-%d %H:%M:%S') - Updated files"

    # Stage all changes
    git add -A

    # Create commit
    if git commit -m "$commit_msg" 2>/dev/null; then
        log_success "Changes committed"
        return 1
    else
        log_warn "Commit failed or nothing to commit"
        return 0
    fi
}

# Run Claude with the task
run_claude() {
    local iteration=$1
    local task_desc="$2"

    log_progress "$iteration" "$COUNT" "Starting iteration..."

    # Build the prompt
    local PROMPT_FILE="$PROJECT_DIR/prompts/task-runner.md"
    local FULL_PROMPT=""

    if [ -f "$PROMPT_FILE" ]; then
        FULL_PROMPT=$(cat "$PROMPT_FILE")
    else
        FULL_PROMPT=$(cat "$PROJECT_DIR/prompts/coding.md")
    fi

    # Add task description
    FULL_PROMPT="$FULL_PROMPT

---

## Current Task

$task_desc

---

## Instructions

1. First, check the current state of the project
2. If this is first run, initialize the project
3. Otherwise, read the progress file and feature list
4. Implement ONE feature
5. Test thoroughly
6. Commit your changes
7. Update the progress file"

    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY-RUN] Would execute Claude with task: $task_desc"
        return 0
    fi

    # Run Claude with --dangerously-skip-permissions to avoid prompts
    # Using timeout to prevent infinite loops
    local Claude_OUTPUT
    if [ "$VERBOSE" = true ]; then
        echo "$FULL_PROMPT" | claude --dangerously-skip-permissions 2>&1 | tee "$LOG_DIR/iteration_${iteration}_${TIMESTAMP}.log"
    else
        echo "$FULL_PROMPT" | claude --dangerously-skip-permissions >> "$LOG_DIR/iteration_${iteration}_${TIMESTAMP}.log" 2>&1
    fi

    local Claude_EXIT_CODE=${PIPESTATUS[0]}

    if [ $Claude_EXIT_CODE -eq 0 ]; then
        log_success "Iteration $iteration completed"
    else
        log_error "Iteration $iteration failed with exit code $Claude_EXIT_CODE"
    fi

    # Auto-commit after each iteration
    auto_commit

    return $Claude_EXIT_CODE
}

# Main loop
main() {
    local current_iteration=1
    local max_iterations=$COUNT
    local task_completed=false

    # Get initial task
    local current_task=$(get_task)

    if [ -z "$current_task" ]; then
        log_warn "No pending tasks found in data/tasks.json"
        log_info "Using custom prompt or default task"

        if [ -n "$CUSTOM_PROMPT" ]; then
            current_task="$CUSTOM_PROMPT"
        else
            current_task="Continue developing the project. Check data/features.json for remaining work."
        fi
    else
        log_info "Task: $current_task"
    fi

    # Check if all features are already done
    if [ "$DRY_RUN" = false ]; then
        if check_all_features_done | grep -q "true"; then
            log_success "All features are already complete!"
            log_info "Use --task-id to start a new task or add tasks to data/tasks.json"
            exit 0
        fi
    fi

    while [ $current_iteration -le $max_iterations ]; do
        log_progress $current_iteration $max_iterations "=========================================="

        # Get current task status
        local pending_count=$(check_pending_tasks)
        if [ "$pending_count" -eq 0 ] && [ "$task_completed" = false ]; then
            log_warn "No more pending tasks!"
            break
        fi

        # Run Claude for this iteration
        if run_claude "$current_iteration" "$current_task"; then
            log_success "Iteration $current_iteration completed successfully"
        else
            log_error "Iteration $current_iteration had issues"
        fi

        # Check if all features are done after each iteration
        if [ "$DRY_RUN" = false ]; then
            if check_all_features_done | grep -q "true"; then
                log_success "All features completed!"
                task_completed=true
                break
            fi
        fi

        ((current_iteration++))

        # Small delay between iterations to prevent rate limiting
        if [ $current_iteration -le $max_iterations ]; then
            log_info "Waiting 2 seconds before next iteration..."
            sleep 2
        fi
    done

    log_info "=========================================="
    log_info "  Loop Completed"
    log_info "  Total iterations: $((current_iteration - 1))"
    log_info "  Log file: $LOG_DIR/loop_${TIMESTAMP}.log"
    log_info "=========================================="

    # Final summary
    if [ "$DRY_RUN" = false ]; then
        local pending=$(check_pending_tasks)
        log_info "Pending tasks remaining: $pending"

        # Show recent commits
        echo ""
        log_info "Recent commits:"
        git log --oneline -5 2>/dev/null || true
    fi
}

# Run main function
main
