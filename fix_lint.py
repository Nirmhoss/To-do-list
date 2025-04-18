#!/usr/bin/env python
"""
Simple script to automatically fix linting issues in the Todo API project.
This script will run isort and black to fix formatting and import order issues.
"""

import os
import subprocess
import sys
from pathlib import Path


def print_colored(message, color="white"):
    """Print colored text to the console."""
    colors = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "blue": "\033[94m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "end": "\033[0m",
    }
    print(f"{colors.get(color, '')}{message}{colors['end']}")


def run_command(command, description):
    """Run a shell command and print its output."""
    print_colored(f"\n▶ {description}...", "blue")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            print_colored(f"✓ Success: {description}", "green")
        else:
            print_colored(f"⚠ Warning: {description} had some issues", "yellow")
            print(result.stdout)
            print(result.stderr)

        return result.returncode == 0
    except Exception as e:
        print_colored(f"✗ Error: {description} failed - {str(e)}", "red")
        return False


def count_linting_issues():
    """Run linting checks and count issues."""
    issues = {}

    # Ensure reports directory exists
    Path("reports").mkdir(exist_ok=True)

    # Run flake8
    subprocess.run(
        ["flake8", "."],
        stdout=open("reports/flake8-report.txt", "w"),
        stderr=subprocess.STDOUT,
        check=False,
    )
    with open("reports/flake8-report.txt", "r") as f:
        issues["flake8"] = len(f.readlines())

    # Run pylint
    subprocess.run(
        ["pylint", "app"],
        stdout=open("reports/pylint-report.txt", "w"),
        stderr=subprocess.STDOUT,
        check=False,
    )
    with open("reports/pylint-report.txt", "r") as f:
        # Count lines containing ":" which usually indicate issues
        issues["pylint"] = sum(1 for line in f if ":" in line)

    # Run mypy
    subprocess.run(
        ["mypy", "app"],
        stdout=open("reports/mypy-report.txt", "w"),
        stderr=subprocess.STDOUT,
        check=False,
    )
    with open("reports/mypy-report.txt", "r") as f:
        issues["mypy"] = sum(1 for line in f if "error:" in line)

    return issues


def main():
    """Main function to run linting fixes."""
    print_colored("🔍 Running automatic code quality fixes", "bold")
    print_colored("======================================", "bold")

    # Check for initial issues
    print_colored("\n📊 Counting initial issues...", "bold")
    initial_issues = count_linting_issues()
    total_initial = sum(initial_issues.values())
    print_colored(f"Found {total_initial} total issues:", "yellow")
    for tool, count in initial_issues.items():
        print(f"  - {tool}: {count} issues")

    # Run isort to fix import ordering
    run_command(["isort", "."], "Fixing import ordering with isort")

    # Run black to fix code formatting
    run_command(["black", "."], "Formatting code with black")

    # Check for remaining issues
    print_colored("\n📊 Counting remaining issues...", "bold")
    remaining_issues = count_linting_issues()
    total_remaining = sum(remaining_issues.values())

    # Calculate improvement
    if total_initial > 0:
        improvement = ((total_initial - total_remaining) / total_initial) * 100
        print_colored(f"\n🎉 Fixed {total_initial - total_remaining} issues!", "green")
        print_colored(f"🔍 Improvement: {improvement:.1f}%", "green")

        if improvement >= 90:
            print_colored("✅ You've reached the 90% improvement target!", "green")
        elif improvement >= 50:
            print_colored("✅ You've reached the 50% improvement target!", "green")
            print_colored("🚀 Keep going to reach the 90% target!", "blue")
        else:
            print_colored(
                f"🚀 You're making progress! Still need {50 - improvement:.1f}% to reach the 50% target.",
                "blue",
            )

    print_colored("\n📝 Remaining issues:", "yellow")
    for tool, count in remaining_issues.items():
        print(f"  - {tool}: {count} issues")

    if total_remaining > 0:
        print_colored("\n📋 Next steps:", "bold")
        print("1. Review reports in the 'reports' directory")
        print("2. Manually fix remaining issues, focusing on:")
        print("   - Adding docstrings to functions and classes")
        print("   - Adding type annotations")
        print("   - Fixing complex functions")
        print("   - Addressing any security issues")
        print("3. Run this script again to check your progress")
    else:
        print_colored("\n🎉 All issues fixed! Your code now meets all quality standards.", "green")


if __name__ == "__main__":
    main()
