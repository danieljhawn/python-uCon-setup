import os
import json
from pygments import highlight, lexers, formatters

def parse_configuration(lines):
    config = {}
    collecting = False
    for line in lines:
        line = line.strip()
        if line == "--= System Config =--":
            collecting = True
        elif collecting:
            if line == "":
                break
            elif ':' in line:
                key, value = line.split(':', 1)
                config[key.strip()] = value.strip()
            else:
                config[line] = True
    return config

def parse_test_section(lines, start_marker, end_marker):
    section = {}
    collecting = False
    for line in lines:
        line = line.strip()
        if start_marker in line and not collecting:
            collecting = True  # Start collecting lines
        elif collecting:
            if ':' in line:
                key, value = line.split(':', 1)
                section[key.strip()] = value.strip()
            elif "ACTIVE" in line:  # Check if this line should be dynamically added
                section[line] = line  # Use the entire line as key and value
            elif "Bat" in line or "Line" in line:
                section["Power Source"] = "Bat" if "Bat" in line else "Line"
            if end_marker in line or "Bat" in line or "Line" in line:
                break  # Stop collecting after these markers
    return section


def parse_events(lines):
    events = {}
    collecting = False
    event_log_lines = []
    for line in lines:
        line = line.strip()
        if "Uptime (minutes):" in line:
            collecting = True
        if collecting:
            if ':' in line:
                key, value = line.split(':', 1)
                events[key.strip()] = value.strip()
            if "-= Newest =-" in line:
                event_log_lines = []  # Start collecting event log lines
                continue
            if "-= Oldest =-" in line:
                # Stop collecting and save event logs
                events['event logs'] = {str(10-i): event for i, event in enumerate(event_log_lines[-10:])}
                break
            if event_log_lines is not None:
                event_log_lines.append(line)
            if "WDT Resets:" in line:
                if ':' in line:
                    key, value = line.split(':', 1)
                    events[key.strip()] = value.strip()
    return events

def create_json_from_logs(directory):
    logs = {}
    files = os.listdir(directory)
    text_files = [file for file in files if file.endswith('.txt') and 'COM' in file]

    for file in text_files:
        file_path = os.path.join(directory, file)
        file_name = os.path.splitext(os.path.basename(file))[0]
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        logs[file_name] = {
            "configuration": parse_configuration(lines),
            "pre-test": parse_test_section(lines, "State:", "Bat"),
            "post-test": parse_test_section(lines, "State:", "Bat"),
            "events": parse_events(lines)
        }

    json_data = json.dumps(logs, indent=4)
    colorful_json = highlight(json_data, lexers.JsonLexer(), formatters.TerminalFormatter())
    return colorful_json

# Using your specified directory path
directory_path = r'C:\Users\dhawn\OneDrive\Desktop\CODE\python-uCon-setup'
print(create_json_from_logs(directory_path))
