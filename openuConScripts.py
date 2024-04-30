import os
import serial.tools.list_ports
import time
import pyautogui
from logParsing import readLog

# Get the list of available COM ports
com_ports = [port.device for port in serial.tools.list_ports.comports()]

print(sorted(com_ports), "PORTS")

def open_ucon_for_com_port(com_port_name, index):
    print(com_port_name, "COM PORT NAME")
    # Specify the path to uCon executable
    ucon_path = r"C:\Program Files (x86)\uCon\ucon.exe"  # Adjust the path if needed

    # Launch uCon
    os.startfile(ucon_path)
    time.sleep(1)  # Wait for uCon to open

    # Select the desired COM port using keystrokes
    pyautogui.press('tab', presses=4, interval=0.1)  # Navigate to the COM port dropdown
    time.sleep(1) 
    pyautogui.write(com_port_name)
    # for _ in range(index + 1):  # Move down to the desired COM port
    #     pyautogui.press('down')
    pyautogui.press('tab', presses=2, interval=0.01)  # Navigate to the User Defined checkbox
    pyautogui.press('space', presses=1, interval=0.01)  # check the checkbox
    pyautogui.press('tab', presses=1, interval=0.01)  # Navigate to the baud rate field
    pyautogui.write('4096')  # set baud rate to 4096
    pyautogui.press('enter')  # open uCon
    time.sleep(1)  
  
    terminal_window_x = 50
    terminal_window_y = 250

    # Move the mouse to the terminal window and click to focus it
    pyautogui.click(terminal_window_x, terminal_window_y)

    # Assuming the position of the text input area in the terminal window
    text_input_x = terminal_window_x + 50
    text_input_y = terminal_window_y + 50

    # Move the mouse to the text input area and click to focus it
    pyautogui.click(text_input_x, text_input_y)

    # navigate to the logging menu to select the log file
    pyautogui.press('alt')
    pyautogui.write("l")
    pyautogui.write("s")
    pyautogui.press('space')
    pyautogui.press('tab', presses=5, interval=0.01) 
    logName = com_port_name + ".txt"
    pyautogui.write(logName)
    pyautogui.press('enter')

    # Type the text into the text input area
    pyautogui.write("con")
    pyautogui.press('enter')
    time.sleep(.5)  # Wait for uCon to catch up
    pyautogui.write("sta")
    pyautogui.press('enter')
    time.sleep(.5)  # Wait for uCon to catch up

    readLog(logName)


# Iterate through the list of COM ports and open a uCon instance for each one
for index, com_port_name in enumerate(sorted(com_ports)):
    open_ucon_for_com_port(com_port_name, index)
