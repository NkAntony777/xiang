# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Auto-Develop Harness Structure

This project implements the long-running agent harness pattern from Anthropic's engineering guide for autonomous software development. The harness enables AI agents to work effectively across multiple context windows on complex, multi-session tasks.

### Architecture Overview

The harness uses a **two-agent pattern**:

1. **Initializer Agent** - First session only: Sets up the development environment
2. **Coding Agent** - All subsequent sessions: Makes incremental progress

### Key Files

| File | Purpose |
|------|---------|
| `prompts/initializer.md` | System prompt for the initializer agent |
| `prompts/coding.md` | System prompt for coding agents |
| `data/features.json` | Feature list with pass/fail status |
| `data/claude-progress.txt` | Progress log across sessions |
| `scripts/init.sh` | Development server startup script |
| `harness/run.sh` | Main harness execution script |

### Commands

```bash
# Start a new project (initializer agent)
./harness/run.sh --init "Build a todo app with React"

# Continue development (coding agent)
./harness/run.sh

# Run specific feature test
./scripts/test-feature.sh "feature-name"

# Check project status
cat data/claude-progress.txt
```

### Workflow

1. **Session Start**: Agent reads git logs, progress file, and feature list
2. **Environment Check**: Run init.sh and verify basic functionality works
3. **Feature Selection**: Choose highest-priority incomplete feature
4. **Implementation**: Make incremental change with tests
5. **Session End**: Commit to git, update progress file, mark feature status

### Progress Tracking

- `data/features.json` - JSON array of features with `passes: boolean`
- `data/claude-progress.txt` - Human-readable session summaries
- Git history - Atomic changes with descriptive commit messages

### Testing Strategy

- Use browser automation (Puppeteer/Playwright MCP) for end-to-end testing
- Run basic sanity check before implementing new features
- Only mark features as "passing" after verified testing

### Best Practices

- One feature per session maximum
- Never remove features from the list - only toggle `passes` field
- Commit after each feature completion
- Always leave code in a clean, working state
