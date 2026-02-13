#!/bin/bash

# Auto-Develop Harness
# Runs Claude Agent for long-running development tasks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Parse arguments
INIT_FLAG=""
USER_PROMPT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --init)
            INIT_FLAG="true"
            USER_PROMPT="$2"
            shift 2
            ;;
        --prompt)
            USER_PROMPT="$2"
            shift 2
            ;;
        *)
            USER_PROMPT="$1"
            shift
            ;;
    esac
done

# Determine which prompt to use
if [ "$INIT_FLAG" = "true" ]; then
    echo "=== Running Initializer Agent ==="
    PROMPT_FILE="$SCRIPT_DIR/../prompts/initializer.md"
else
    echo "=== Running Coding Agent ==="
    PROMPT_FILE="$SCRIPT_DIR/../prompts/coding.md"
fi

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Prompt file not found: $PROMPT_FILE"
    exit 1
fi

# Read the system prompt
SYSTEM_PROMPT=$(cat "$PROMPT_FILE")

# Build the full prompt
FULL_PROMPT="$SYSTEM_PROMPT"

if [ -n "$USER_PROMPT" ]; then
    FULL_PROMPT="$FULL_PROMPT

---

## User Request

$USER_PROMPT"
fi

# Check if this is first run (no git initialized)
if [ ! -d ".git" ]; then
    echo "First run detected - running initializer"
    INIT_FLAG="true"
    FULL_PROMPT=$(cat "$SCRIPT_DIR/../prompts/initializer.md")
    if [ -n "$USER_PROMPT" ]; then
        FULL_PROMPT="$FULL_PROMPT

---

## User Request

$USER_PROMPT"
    fi
fi

# Run Claude with the prompt
# Note: Adjust the claude command based on your installation
echo "$FULL_PROMPT" | claude --dangerously-skip-permissions 2>&1 || true

echo "=== Session Complete ==="
echo "Remember to:"
echo "  1. Commit your changes: git add . && git commit -m 'Description'"
echo "  2. Update progress: Edit data/claude-progress.txt"
echo "  3. Update features: Edit data/features.json"
