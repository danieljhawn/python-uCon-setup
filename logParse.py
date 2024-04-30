import os
import json
from pygments import highlight, lexers, formatters

def create_json_from_logs(directory):
    logs = {}
    files = os.listdir(directory)
    text_files = [file for file in files if file.endswith('.txt') and 'COM' in file]

    for file in text_files:
        file_path = os.path.join(directory, file)
        file_name = os.path.splitext(os.path.basename(file))[0]  # Remove extension
        logs[file_name] = {"configuration": {}, "pre-test": {}, "post-test": {}}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='utf-16') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                print(f"Failed to decode {file_path} with common encodings.")
                continue  # Skip to the next file

        state_sections = []
        current_section = []
        config_collecting = False
        test_collecting = False
        config_complete = False

        for line in lines:
            line = line.strip()
            if line == "--= System Config =--" and not config_complete:
                config_collecting = True
            elif config_collecting and line == "":
                config_collecting = False
                config_complete = True
            elif config_collecting:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    logs[file_name]["configuration"][key] = value
                elif "CRST On" in line:
                    logs[file_name]["configuration"]["Current Reset"] = "On"
                elif "CRST Not Allowed" in line:
                    logs[file_name]["configuration"]["Current Reset"] = "Not Allowed"
                else:
                    logs[file_name]["configuration"][line] = True  # Treat lines without ':' as key with True value

            if line.startswith("State:"):
                if test_collecting:  # Finish the last section if another "State:" is found
                    state_sections.append(current_section)
                test_collecting = True
                current_section = [line]
            elif test_collecting and ("Bat" in line or "Line" in line):
                power_source = "Bat" if "Bat" in line else "Line"
                current_section.append(f"Power Source: {power_source}")
                state_sections.append(current_section)
                test_collecting = False  # Only collect first two sections (two "State:")
                if len(state_sections) == 2:
                    break
            elif test_collecting:
                current_section.append(line)

        for index, section in enumerate(state_sections):
            test_phase = "pre-test" if index == 0 else "post-test"
            for entry in section:
                if entry is None:  # Skip None entries
                    continue
                if ':' in entry:
                    key, value = entry.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == "State" and test_phase == "post-test" and section.index(entry) < len(section) - 1 and section[section.index(entry) + 1].startswith("*"):
                        value = section[section.index(entry) + 1][1:].strip()
                        section[section.index(entry) + 1] = None
                    logs[file_name][test_phase][key] = value
                else:
                    logs[file_name][test_phase][entry] = entry

    return json.dumps(logs, indent=4)  # Return JSON string formatted nicely

# Using your specified directory path
directory_path = r'C:\Users\dhawn\OneDrive\Desktop\CODE\python-uCon-setup'

# Call your function to get the JSON data
json_data = create_json_from_logs(directory_path)

# Use Pygments to colorize the JSON output
colorful_json = highlight(json_data, lexers.JsonLexer(), formatters.TerminalFormatter())

# Print the colorized JSON to the terminal
print(colorful_json)