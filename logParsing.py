import os
import serial.tools.list_ports
import time
import pyautogui

def readLog(logName):
    # Flag to track if any "State: " lines were found
    found_state_lines = False

    # Open the file in read mode
    with open(logName, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Check if the line starts with "State: "
            if line.startswith("State: "):
                # Update the flag to indicate that "State: " lines were found
                found_state_lines = True
                # Check if the line contains "Sleep"
                if "Sleep" not in line:
                    # Show a warning message to the user
                    print("Warning: 'Sleep' not found in line:", line.strip())
                    # Open the file in append mode and write the warning message to it
                    with open(logName, 'a') as outfile:
                        outfile.write("Warning: 'Sleep' not found in line: " + line.strip() + "\n")
                else:
                    # Print the line if it contains "Sleep"
                    print(line)

    # Check if no "State: " lines were found
    if not found_state_lines:
        print("No lines starting with 'State: ' were found in the log file.")
        # Open the file in append mode and write the message to it
        with open(logName, 'a') as outfile:
            outfile.write("No lines starting with 'State: ' were found in the log file.\n")