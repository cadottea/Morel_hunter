import os
import re

# Define patterns for keys to replace
patterns = {
    "API Key": r"(?i)(api_key|apikey|api\-key|key|token)\s*[:=]\s*['\"]([a-zA-Z0-9_\-+/]{20,})['\"]",
    "Authorization Header": r"(?i)(Authorization\s*[:=]\s*['\"]Bearer\s+[a-zA-Z0-9_\-+/]{20,})['\"]"
}

# Replacement string for keys
replacement_text = '"your API key here"'

def replace_keys_in_py_files():
    print("Scanning and replacing API keys in .py files...")
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Replace all patterns
                updated_content = content
                for name, pattern in patterns.items():
                    updated_content = re.sub(pattern, f'\\1 {replacement_text}', updated_content)

                # Write back the file if content changed
                if updated_content != content:
                    with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
                        f.write(updated_content)
                    print(f"[UPDATED] Replaced {name} in {filepath}")

if __name__ == "__main__":
    replace_keys_in_py_files()