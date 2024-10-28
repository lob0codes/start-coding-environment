import os
import json
import time
import pygetwindow as gw
import pyautogui


def get_folder_name(folder_path: str) -> str:
    return folder_path.split('\\')[-1]


def snap_window_to_side(direction):
    """
    Simulates pressing Windows + Left or Windows + Right to snap the window.

    :param direction: Either 'left' or 'right'.
    """
    if direction == 'left':
        pyautogui.hotkey('win', 'left')
    elif direction == 'right':
        pyautogui.hotkey('win', 'right')


def activate_window(window_title):
    """
    Activate the window with the specified title.

    :param window_title: Title of the window to activate.
    """
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        window.activate()  # Bring the window to the foreground
        return True
    return False


# Example usage:
# Update with your folder path
folder_a = "F:\\Personal\\Proyectos\\Coding\\portfolio-api"
# Update with your folder path
folder_b = "F:\\Personal\\Proyectos\\Coding\\portfolio\\portfolio"

# Open the folders
os.startfile(folder_a)
os.startfile(folder_b)

time.sleep(2)  # Wait for the folders to open

# Get the folder names
folder_a_name = get_folder_name(folder_a)
folder_a_name = f'{folder_a_name} - File Explorer'

folder_b_name = get_folder_name(folder_b)
folder_b_name = f'{folder_b_name} - File Explorer'

# Activate the first folder window
if activate_window(folder_a_name):
    time.sleep(1)  # Wait to ensure the window is active
    snap_window_to_side('left')  # Snap to left

time.sleep(1)  # Wait before focusing the next window

# Activate the second folder window
if activate_window(folder_b_name):
    time.sleep(1)  # Wait to ensure the window is active
    snap_window_to_side('right')  # Snap to right
