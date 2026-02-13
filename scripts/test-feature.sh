#!/bin/bash

# Test Feature Script
# Runs tests for a specific feature

FEATURE_NAME="$1"

if [ -z "$FEATURE_NAME" ]; then
    echo "Usage: ./test-feature.sh <feature-name>"
    exit 1
fi

echo "=== Testing Feature: $FEATURE_NAME ==="

# Check if feature exists in features.json
if ! grep -q "$FEATURE_NAME" data/features.json; then
    echo "Warning: Feature '$FEATURE_NAME' not found in features.json"
fi

# Run any feature-specific tests
if [ -f "tests/$FEATURE_NAME.test.js" ]; then
    echo "Running feature test..."
    npm test -- tests/$FEATURE_NAME.test.js
elif [ -f "tests/test_$FEATURE_NAME.py" ]; then
    echo "Running feature test..."
    pytest tests/test_$FEATURE_NAME.py
else
    echo "No specific test found for $FEATURE_NAME"
    echo "Running general test suite..."
    npm test 2>/dev/null || pytest 2>/dev/null || echo "No test framework detected"
fi

echo "=== Test Complete ==="
