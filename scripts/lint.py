#!/usr/bin/env python
"""
Cross-platform linting script for the Todo API project.
This script runs various code quality checks and generates reports.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Define colors for terminal output (works on Windows with newer versions of Python)
COLORS = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "end": "\033[0m",
    "bold": "\033[1m",
}


def color_text(text: str, color: str) -> str:
    """Add color to terminal text."""
    return f"{COLORS.get(color, '')}{text}{COLORS['end']}"


def run_command(command: List[str], capture_output: bool = True) -> Tuple[int, str]:
    """Run a shell command and return the exit code and output."""
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout or ""
    except Exception as e:
        return 1, str(e)


def ensure_directory_exists(directory: str) -> None:
    """Ensure the specified directory exists."""
    Path(directory).mkdir(exist_ok=True)


def count_issues_in_file(file_path: str, search_pattern: str) -> int:
    """Count occurrences of a pattern in a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return content.count(search_pattern)
    except FileNotFoundError:
        return 0


def run_isort(fix: bool) -> bool:
    """Run isort to check or fix import ordering."""
    print("\nRunning isort...")
    command = ["isort", "."]
    if not fix:
        command.append("--check-only")
        command.append("--diff")

    exit_code, output = run_command(command)

    if exit_code == 0:
        print(color_text("isort: All imports are correctly sorted ✓", "green"))
        return True
    else:
        if fix:
            print(color_text("isort: Imports have been sorted", "blue"))
            return True
        else:
            ensure_directory_exists("reports")
            with open("reports/isort-report.txt", "w") as f:
                f.write(output)
            print(color_text("isort: Issues found ✗", "red"))
            return False


def run_black(fix: bool) -> bool:
    """Run black to check or fix code formatting."""
    print("\nRunning black...")
    command = ["black", "."]
    if not fix:
        command.append("--check")

    exit_code, output = run_command(command)

    if exit_code == 0:
        print(color_text("black: All files are properly formatted ✓", "green"))
        return True
    else:
        if fix:
            print(color_text("black: Files have been reformatted", "blue"))
            return True
        else:
            ensure_directory_exists("reports")
            with open("reports/black-report.txt", "w") as f:
                f.write(output)
            print(color_text("black: Formatting issues found ✗", "red"))
            return False


def run_flake8() -> Tuple[bool, int]:
    """Run flake8 to check for code style issues."""
    print("\nRunning flake8...")
    ensure_directory_exists("reports")
    report_path = "reports/flake8-report.txt"

    command = ["flake8", "."]
    exit_code, output = run_command(command)

    with open(report_path, "w") as f:
        f.write(output)

    issue_count = len(output.splitlines())
    if issue_count == 0:
        print(color_text("flake8: No issues found ✓", "green"))
        return True, 0
    else:
        print(color_text(f"flake8: Found {issue_count} issues ✗", "red"))
        return False, issue_count


def run_pylint() -> Tuple[bool, int]:
    """Run pylint to check for code quality issues."""
    print("\nRunning pylint...")
    ensure_directory_exists("reports")
    report_path = "reports/pylint-report.txt"

    command = ["pylint", "app"]
    exit_code, output = run_command(command)

    with open(report_path, "w") as f:
        f.write(output)

    # Count lines containing ":" which usually indicate issues
    issue_count = output.count(":")
    if issue_count == 0:
        print(color_text("pylint: No issues found ✓", "green"))
        return True, 0
    else:
        print(color_text(f"pylint: Found {issue_count} issues ✗", "red"))
        return False, issue_count


def run_mypy() -> Tuple[bool, int]:
    """Run mypy to check for type issues."""
    print("\nRunning mypy...")
    ensure_directory_exists("reports")
    report_path = "reports/mypy-report.txt"

    command = ["mypy", "app"]
    exit_code, output = run_command(command)

    with open(report_path, "w") as f:
        f.write(output)

    issue_count = output.count("error:")
    if issue_count == 0:
        print(color_text("mypy: No type issues found ✓", "green"))
        return True, 0
    else:
        print(color_text(f"mypy: Found {issue_count} type issues ✗", "red"))
        return False, issue_count


def run_bandit() -> Tuple[bool, int]:
    """Run bandit to check for security issues."""
    print("\nRunning bandit...")
    ensure_directory_exists("reports")
    report_path = "reports/bandit-report.txt"

    command = ["bandit", "-r", "app"]
    exit_code, output = run_command(command)

    with open(report_path, "w") as f:
        f.write(output)

    issue_count = output.count("Issue:")
    if issue_count == 0:
        print(color_text("bandit: No security issues found ✓", "green"))
        return True, 0
    else:
        print(color_text(f"bandit: Found {issue_count} security issues ✗", "red"))
        return False, issue_count


def count_python_files() -> int:
    """Count Python files in the project, excluding certain directories."""
    excluded_dirs = ["venv", ".venv", "migrations", "__pycache__"]
    count = 0

    for root, dirs, files in os.walk("."):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for file in files:
            if file.endswith(".py"):
                count += 1

    return count


def main() -> None:
    """Run linting checks based on command line arguments."""
    parser = argparse.ArgumentParser(description="Run code quality checks.")
    parser.add_argument(
        "--fix", action="store_true", help="Automatically fix issues where possible"
    )
    parser.add_argument(
        "--format", action="store_true", help="Run only formatting tools (black, isort)"
    )
    parser.add_argument(
        "--lint", action="store_true", help="Run only linting tools (flake8, pylint)"
    )
    parser.add_argument("--strict", action="store_true", help="Run with stricter settings")
    parser.add_argument("--summary", action="store_true", help="Show only summary of issues")
    args = parser.parse_args()

    # If neither --format nor --lint is specified, run all checks
    if not args.format and not args.lint:
        run_format = True
        run_lint = True
    else:
        run_format = args.format
        run_lint = args.lint

    print(color_text("Running code quality checks...", "bold"))
    print(color_text("-----------------------------", "bold"))

    # Count Python files
    file_count = count_python_files()
    print(f"Found {file_count} Python files to check")

    # Track issues
    total_issues = 0

    # Run formatting tools
    if run_format:
        isort_success = run_isort(args.fix)
        black_success = run_black(args.fix)

    # Run linting tools
    if run_lint:
        flake8_success, flake8_issues = run_flake8()
        pylint_success, pylint_issues = run_pylint()
        mypy_success, mypy_issues = run_mypy()
        bandit_success, bandit_issues = run_bandit()

        total_issues = flake8_issues + pylint_issues + mypy_issues + bandit_issues

    # Print summary
    print("\nSUMMARY:")
    print("--------")

    if run_lint:
        if total_issues == 0:
            print(color_text("All checks passed successfully! ✓", "green"))
        else:
            print(color_text(f"Total issues found: {total_issues}", "yellow"))
            print(f" - Flake8: {flake8_issues} issues")
            print(f" - Pylint: {pylint_issues} issues")
            print(f" - MyPy: {mypy_issues} issues")
            print(f" - Bandit: {bandit_issues} issues")
            print("\nReports are saved in the 'reports' directory.")

    if args.fix and run_format and (not run_lint or total_issues > 0):
        print("\nSome issues were fixed automatically, but manual fixes may still be required.")
        print("Run this script again to see remaining issues.")


if __name__ == "__main__":
    main()
