#!/usr/bin/env python
"""
Enhanced fixing script for the Todo API project.
This script automatically fixes common linting issues and measures improvement.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def print_colored(message: str, color: str = "white") -> None:
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


def run_command(command: List[str], description: str) -> bool:
    """Run a shell command and print its output."""
    print_colored(f"\n▶️ {description}...", "blue")

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
            print_colored(f"⚠️ Warning: {description} had some issues", "yellow")
            print(result.stdout)
            print(result.stderr)

        return result.returncode == 0
    except Exception as e:
        print_colored(f"✗ Error: {description} failed - {str(e)}", "red")
        return False


def count_linting_issues() -> Dict[str, int]:
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


def fix_trailing_whitespace_and_newlines() -> int:
    """
    Fix trailing whitespace and ensure files end with a newline.

    Returns:
        Number of files fixed
    """
    print_colored("\n▶️ Fixing trailing whitespace and missing newlines...", "blue")

    fixed_count = 0
    python_files = []

    # Find all Python files
    for root, _, files in os.walk("."):
        if "venv" in root or ".git" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    # Process each file
    for file_path in python_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Fix trailing whitespace
        new_content = re.sub(r"[ \t]+$", "", content, flags=re.MULTILINE)

        # Ensure file ends with exactly one newline
        if not new_content.endswith("\n"):
            new_content += "\n"
        else:
            while new_content.endswith("\n\n"):
                new_content = new_content[:-1]

        # Fix blank lines with whitespace
        new_content = re.sub(r"\n[ \t]+\n", "\n\n", new_content)

        # Ensure proper spacing between functions/classes (2 blank lines)
        new_content = re.sub(r"(\n)class ", r"\n\n\nclass ", new_content)
        new_content = re.sub(r"(\n)def ", r"\n\n\ndef ", new_content)
        new_content = re.sub(r"\n\n\n\n+class", r"\n\n\nclass", new_content)
        new_content = re.sub(r"\n\n\n\n+def", r"\n\n\ndef", new_content)

        # Write changes if content was modified
        if content != new_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed_count += 1

    print_colored(f"✓ Fixed whitespace and newline issues in {fixed_count} files", "green")

    return fixed_count


def add_missing_docstrings() -> int:
    """
    Add missing module docstrings to Python files.

    Returns:
        Number of files fixed
    """
    print_colored("\n▶️ Adding missing module docstrings...", "blue")

    fixed_count = 0
    python_modules = []

    # Find Python module files
    for root, _, files in os.walk("app"):
        if "__pycache__" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                python_modules.append(os.path.join(root, file))

    # Process each module
    for module_path in python_modules:
        with open(module_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if file lacks a module docstring
        if not re.search(r'^""".*?"""', content, re.DOTALL) and not re.search(
            r"^'''.*?'''", content, re.DOTALL
        ):
            # Generate an appropriate docstring based on the module name
            module_name = os.path.basename(module_path).replace(".py", "")
            parent_dir = os.path.basename(os.path.dirname(module_path))

            if module_name == "__init__":
                docstring = f'"""\n{parent_dir} package initialization.\n"""\n'
            elif parent_dir == "models":
                docstring = f'"""\nDatabase model for {module_name}.\n\nThis module defines the {module_name} model class and its related methods.\n"""\n'
            elif parent_dir == "routes":
                docstring = f'"""\nAPI routes for {module_name} endpoints.\n\nThis module defines endpoints for interacting with {module_name} resources.\n"""\n'
            elif parent_dir == "utils":
                docstring = f'"""\nUtility functions for {module_name}.\n\nThis module provides helper functions related to {module_name}.\n"""\n'
            else:
                docstring = f'"""\n{module_name.replace("_", " ").title()} module.\n"""\n'

            # Add docstring to the beginning of the file
            new_content = docstring + content

            with open(module_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            fixed_count += 1

    print_colored(f"✓ Added module docstrings to {fixed_count} files", "green")

    return fixed_count


def main() -> None:
    """Main function to run code quality fixes."""
    print_colored("🔍 Running enhanced code quality fixes", "bold")
    print_colored("=====================================", "bold")

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

    # Fix trailing whitespace and ensure newlines
    files_fixed_whitespace = fix_trailing_whitespace_and_newlines()

    # Add missing docstrings
    files_fixed_docstrings = add_missing_docstrings()

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

    print_colored("\n📝 Summary of fixes:", "bold")
    print(f"  - Fixed formatting with Black and isort")
    print(f"  - Fixed whitespace and newline issues in {files_fixed_whitespace} files")
    print(f"  - Added docstrings to {files_fixed_docstrings} files")

    print_colored("\n📝 Remaining issues:", "yellow")
    for tool, count in remaining_issues.items():
        print(f"  - {tool}: {count} issues")

    if total_remaining > 0:
        print_colored("\n📋 Next steps:", "bold")
        print("1. Review reports in the 'reports' directory")
        print("2. Manually fix remaining issues, focusing on:")
        print("   - Adding function and class docstrings")
        print("   - Adding type annotations")
        print("   - Fixing cyclic imports by restructuring your imports")
        print("   - Addressing any security issues")
        print("3. Run this script again to check your progress")
    else:
        print_colored("\n🎉 All issues fixed! Your code now meets all quality standards.", "green")


if __name__ == "__main__":
    main()
