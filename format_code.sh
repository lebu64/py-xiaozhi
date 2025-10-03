#!/bin/bash

echo "🧹 Starting code formatting..."

# Define target folders and files to format
TARGETS="src/ scripts/ main.py"

echo "📁 Formatting targets: $TARGETS"
echo ""

# Remove unused imports and variables (non-intrusive but effective)
echo "1️⃣ Removing unused imports and variables..."
autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports $TARGETS

# Fix docstring punctuation, capitalization, etc.
echo "2️⃣ Formatting docstrings..."
docformatter -r -i --wrap-summaries=88 --wrap-descriptions=88 --make-summary-multi-line $TARGETS

# Auto-sort imports
echo "3️⃣ Sorting import statements..."
isort $TARGETS

# Auto-format (handles long lines, function parameters, f-strings, etc.)
echo "4️⃣ Formatting code..."
black $TARGETS

# Final static checking (non-fixing)
echo "5️⃣ Static code checking..."
flake8 $TARGETS

echo ""
echo "✅ Code formatting completed!"
echo "📊 Processed targets: $TARGETS"
