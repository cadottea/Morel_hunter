import os
import re

# Define patterns for "API" and "key"
patterns = {
    "API": r"(?i)\bapi\b",
    "key": r"(?i)\bkey\b"
}

# Directories to exclude
excluded_dirs = ["env", "venv", "__pycache__", "site-packages"]

# Scripts to exclude
excluded_files = ["replace_secrets.py", os.path.basename(__file__)]  # Add any other script names here

def scan_py_files():
    print("Scanning .py files for 'API' and 'key'...")
    for root, dirs, files in os.walk("."):
        # Exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in files:
            if file.endswith(".py") and file not in excluded_files:  # Avoid scanning excluded files
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        for name, pattern in patterns.items():
                            if re.search(pattern, line):
                                print(f"[WARNING] Found '{name}' in {filepath}, line {i+1}:")
                                print(f"  {line.strip()}")

if __name__ == "__main__":
    scan_py_files()