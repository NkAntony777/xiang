#!/bin/bash

# Task Queue Manager
# Manages the task queue for the auto-develop harness

TASKS_FILE="data/tasks.json"

# Get next pending task
get_next_task() {
    if [ ! -f "$TASKS_FILE" ]; then
        echo "Error: Tasks file not found: $TASKS_FILE"
        return 1
    fi

    # Use node to parse JSON
    if command -v node &> /dev/null; then
        node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$TASKS_FILE', 'utf8'));
const task = data.tasks.find(t => t.status === 'pending');
if (task) {
    console.log(JSON.stringify(task));
} else {
    console.log('');
}
"
    else
        echo "Error: Node.js is required for task management"
        return 1
    fi
}

# Mark task as completed
complete_task() {
    TASK_ID="$1"
    if [ -z "$TASK_ID" ]; then
        echo "Error: Task ID required"
        return 1
    fi

    node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$TASKS_FILE', 'utf8'));
const task = data.tasks.find(t => t.id == $TASK_ID);
if (task) {
    task.status = 'completed';
    task.completed_at = new Date().toISOString();
    data.metadata.completed++;
    data.metadata.pending--;
    fs.writeFileSync('$TASKS_FILE', JSON.stringify(data, null, 2));
    console.log('Task $TASK_ID marked as completed');
} else {
    console.log('Task $TASK_ID not found');
}
"
}

# List all tasks
list_tasks() {
    if [ ! -f "$TASKS_FILE" ]; then
        echo "No tasks file found"
        return
    fi

    node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$TASKS_FILE', 'utf8'));
console.log('=== Task Queue ===');
console.log('Total:', data.metadata.total, '| Completed:', data.metadata.completed, '| Pending:', data.metadata.pending);
console.log('---');
data.tasks.forEach(t => {
    console.log('[' + t.id + '] ' + t.status.toUpperCase() + ': ' + t.description);
});
"
}

# Add a new task
add_task() {
    DESCRIPTION="$1"
    if [ -z "$DESCRIPTION" ]; then
        echo "Error: Task description required"
        return 1
    fi

    node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$TASKS_FILE', 'utf8'));
const maxId = data.tasks.length > 0 ? Math.max(...data.tasks.map(t => t.id)) : 0;
const newTask = {
    id: maxId + 1,
    description: process.argv[2],
    status: 'pending',
    created_at: new Date().toISOString(),
    completed_at: null
};
data.tasks.push(newTask);
data.metadata.total++;
data.metadata.pending++;
fs.writeFileSync('$TASKS_FILE', JSON.stringify(data, null, 2));
console.log('Task added: [' + newTask.id + '] ' + newTask.description);
" "$DESCRIPTION"
}

# Show usage
show_usage() {
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  get              Get next pending task"
    echo "  complete <id>   Mark task as completed"
    echo "  list            List all tasks"
    echo "  add <desc>      Add a new task"
}

# Main
case "$1" in
    get)
        get_next_task
        ;;
    complete)
        complete_task "$2"
        ;;
    list)
        list_tasks
        ;;
    add)
        add_task "$2"
        ;;
    *)
        show_usage
        ;;
esac
