import os
import serial.tools.list_ports
import time
import pyautogui

# Get the list of available COM ports
com_ports = [port.device for port in serial.tools.list_ports.comports()]

print(com_ports, "PORTS")

def open_ucon_for_com_port(com_port_name, index):
    print(com_port_name, "COM PORT NAME")
    # Specify the path to uCon executable
    ucon_path = r"C:\Program Files (x86)\uCon\ucon.exe"  # Adjust the path if needed

    # Launch uCon
    os.startfile(ucon_path)
    time.sleep(2)  # Wait for uCon to open

    # Select the desired COM port using keystrokes
    pyautogui.press('tab', presses=4, interval=0.1)  # Navigate to the COM port dropdown
    for _ in range(index):  # Move down to the desired COM port
        pyautogui.press('down')
    # pyautogui.press('enter')  # Select the COM port
    time.sleep(3)  # Wait for the operation to complete

    print(f"uCon instance opened for COM port: {com_port_name}")

# Iterate through the list of COM ports and open a uCon instance for each one
for index, com_port_name in enumerate(com_ports):
    open_ucon_for_com_port(com_port_name, index)
