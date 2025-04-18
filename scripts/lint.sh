#!/bin/bash
set -e

# Display help information
function show_help {
    echo "Usage: $0 [options]"
    echo
    echo "Run various code quality checks on the project."
    echo
    echo "Options:"
    echo "  -h, --help        Show this help message and exit"
    echo "  --fix             Automatically fix issues where possible"
    echo "  --format          Run only formatting tools (black, isort)"
    echo "  --lint            Run only linting tools (flake8, pylint)"
    echo "  --strict          Run with stricter settings"
    echo "  --all             Run all checks (default)"
    echo "  --summary         Show only summary of issues"
    echo
    echo "Examples:"
    echo "  $0 --fix          Run all checks and fix issues automatically where possible"
    echo "  $0 --format --fix Run only formatting and fix issues"
}

# Initialize options
FIX=false
FORMAT_ONLY=false
LINT_ONLY=false
STRICT=false
SUMMARY=false

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) show_help; exit 0 ;;
        --fix) FIX=true ;;
        --format) FORMAT_ONLY=true ;;
        --lint) LINT_ONLY=true ;;
        --strict) STRICT=true ;;
        --summary) SUMMARY=true ;;
        --all) FORMAT_ONLY=false; LINT_ONLY=false ;;
        *) echo "Unknown option: $1"; show_help; exit 1 ;;
    esac
    shift
done

# Create a directory for reports if it doesn't exist
mkdir -p reports

echo "Running code quality checks..."
echo "-----------------------------"

# Count files for percentage calculations
PYTHON_FILES=$(find . -name "*.py" -not -path "*/venv/*" -not -path "*/.venv/*" -not -path "*/migrations/*" | wc -l)
echo "Found $PYTHON_FILES Python files to check"

# Run isort if not lint-only
if [ "$LINT_ONLY" = false ]; then
    echo
    echo "Running isort..."
    if [ "$FIX" = true ]; then
        isort .
        echo "isort: Files sorted"
    else
        isort --check --diff . > reports/isort-report.txt
        if [ $? -eq 0 ]; then
            echo "isort: All imports are correctly sorted ✓"
        else
            if [ "$SUMMARY" = false ]; then
                cat reports/isort-report.txt
            fi
            echo "isort: Issues found ✗"
        fi
    fi
fi

# Run black if not lint-only
if [ "$LINT_ONLY" = false ]; then
    echo
    echo "Running black..."
    if [ "$FIX" = true ]; then
        black .
        echo "black: Files formatted"
    else
        black --check . > reports/black-report.txt 2>&1
        if [ $? -eq 0 ]; then
            echo "black: All files are properly formatted ✓"
        else
            if [ "$SUMMARY" = false ]; then
                cat reports/black-report.txt
            fi
            echo "black: Formatting issues found ✗"
        fi
    fi
fi

# Run flake8 if not format-only
if [ "$FORMAT_ONLY" = false ]; then
    echo
    echo "Running flake8..."
    flake8 . > reports/flake8-report.txt
    FLAKE8_ISSUES=$(cat reports/flake8-report.txt | wc -l)
    if [ $FLAKE8_ISSUES -eq 0 ]; then
        echo "flake8: No issues found ✓"
    else
        if [ "$SUMMARY" = false ]; then
            cat reports/flake8-report.txt
        fi
        echo "flake8: Found $FLAKE8_ISSUES issues ✗"
    fi
fi

# Run pylint if not format-only
if [ "$FORMAT_ONLY" = false ]; then
    echo
    echo "Running pylint..."
    pylint --output-format=parseable app > reports/pylint-report.txt || true
    PYLINT_ISSUES=$(grep -c ":" reports/pylint-report.txt || echo 0)
    if [ $PYLINT_ISSUES -eq 0 ]; then
        echo "pylint: No issues found ✓"
    else
        if [ "$SUMMARY" = false ]; then
            cat reports/pylint-report.txt
        fi
        echo "pylint: Found $PYLINT_ISSUES issues ✗"
    fi
fi

# Run mypy if not format-only
if [ "$FORMAT_ONLY" = false ]; then
    echo
    echo "Running mypy..."
    mypy app > reports/mypy-report.txt || true
    MYPY_ISSUES=$(grep -c "error:" reports/mypy-report.txt || echo 0)
    if [ $MYPY_ISSUES -eq 0 ]; then
        echo "mypy: No type issues found ✓"
    else
        if [ "$SUMMARY" = false ]; then
            cat reports/mypy-report.txt
        fi
        echo "mypy: Found $MYPY_ISSUES type issues ✗"
    fi
fi

# Run bandit if not format-only
if [ "$FORMAT_ONLY" = false ]; then
    echo
    echo "Running bandit..."
    bandit -r app -f txt > reports/bandit-report.txt || true
    BANDIT_ISSUES=$(grep -c "Issue:" reports/bandit-report.txt || echo 0)
    if [ $BANDIT_ISSUES -eq 0 ]; then
        echo "bandit: No security issues found ✓"
    else
        if [ "$SUMMARY" = false ]; then
            cat reports/bandit-report.txt
        fi
        echo "bandit: Found $BANDIT_ISSUES security issues ✗"
    fi
fi

# Calculate total and show summary
echo
echo "SUMMARY:"
echo "--------"
TOTAL_ISSUES=$((FLAKE8_ISSUES + PYLINT_ISSUES + MYPY_ISSUES + BANDIT_ISSUES))
if [ $TOTAL_ISSUES -eq 0 ]; then
    echo "All checks passed successfully! ✓"
else
    echo "Total issues found: $TOTAL_ISSUES"
    echo " - Flake8: $FLAKE8_ISSUES issues"
    echo " - Pylint: $PYLINT_ISSUES issues"
    echo " - MyPy: $MYPY_ISSUES issues"
    echo " - Bandit: $BANDIT_ISSUES issues"
    echo
    echo "Reports are saved in the 'reports' directory."
fi

if [ "$FIX" = true ] && [ $TOTAL_ISSUES -gt 0 ]; then
    echo
    echo "Some issues were fixed automatically, but manual fixes are still required."
    echo "Run '$0' again to see remaining issues."
fi
