#!/bin/bash

# Get Python executable path in conda environment
PYTHON_BIN=$(which python3)

echo "🔍 Current Python path: $PYTHON_BIN"

# Copy path to clipboard
echo "$PYTHON_BIN" | pbcopy
echo "✅ Path copied to clipboard"

# Open accessibility settings interface
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"

# Show prompt
osascript <<EOF
tell application "System Events"
	display dialog "Please manually add the following Python path to 'Accessibility':\n\n$PYTHON_BIN\n\nPath has been copied to clipboard." buttons {"OK"} default button "OK"
end tell
EOF
