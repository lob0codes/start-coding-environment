import ctypes
import os
import json
import sys
import time
from typing import List
import pygetwindow as gw
import pyautogui
import subprocess
import traceback


def get_resource_path(relative_path):
    """Get the absolute path to a resource, works for both PyInstaller bundle and development."""
    if hasattr(sys, '_MEIPASS'):  # PyInstaller extracts files to a temp folder at runtime
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)


def get_folder_name(folder_path: str) -> str:
    return folder_path.split('\\')[-1]


def get_work_area_dimensions():
    user32 = ctypes.windll.user32
    work_area = ctypes.wintypes.RECT()
    user32.SystemParametersInfoW(
        48, 0, ctypes.byref(work_area), 0)  # SPI_GETWORKAREA
    work_width = work_area.right - work_area.left
    work_height = work_area.bottom - work_area.top
    return work_width, work_height


def move_window_to(target_window, position, left_offset=0, top_offset=0):

    screen_w, _ = get_work_area_dimensions()

    target_y = 0

    if position == 'left':
        target_x = 0

    elif position == 'right':
        target_x = screen_w // 2

    target_window.moveTo(target_x + left_offset, target_y + top_offset)


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


def open_git_bash_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        return

    # Construct the command to open Git Bash in the specified folder
    command = ['F:\\Git\\git-bash.exe', f'--cd={folder_path}']

    # Launch Git Bash in the given folder
    subprocess.Popen(command)


def get_git_bash_name(target_git_path):
    output: List[str] = target_git_path.split('\\')
    output = output[1:]
    output = '/'.join(output)
    output = f'MINGW64:/f/{output}'
    return output


def get_visual_studio_windows_names():
    names = [name for name in gw.getAllTitles() if 'Visual Studio Code' in name]
    return names


def open_vscode_in_folder(folder_path):
    # Validate if the path exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

    # Open VS Code in the specified folder
    subprocess.Popen(['F:\\Microsoft VS Code\\Code.exe', folder_path])


def select_visual_studio_window(reference, names):
    windows = [name for name in names if reference in name]
    return windows[0]


try:
    # Opens two working folders.
    folders_config_file = get_resource_path('folders.json')
    with open(folders_config_file, 'r') as file:
        folders = json.load(file)

    folder_a = folders['folder_a']
    folder_b = folders['folder_b']

    folder_a_name: str = get_folder_name(folder_a)
    folder_a_name = f'{folder_a_name} - File Explorer'
    folder_b_name: str = get_folder_name(folder_b)
    folder_b_name = f'{folder_b_name} - File Explorer'

    os.startfile(folder_a)
    os.startfile(folder_b)

    time.sleep(1)

    # Activate the first folder window
    if activate_window(folder_a_name):
        time.sleep(1.1)  # Wait to ensure the window is active
        snap_window_to_side('left')  # Snap to left

    time.sleep(1)  # Wait before focusing the next window

    # Activate the second folder window
    if activate_window(folder_b_name):
        time.sleep(1.1)  # Wait to ensure the window is active
        snap_window_to_side('right')  # Snap to right

    open_git_bash_in_folder(folder_a)
    time.sleep(2)
    open_git_bash_in_folder(folder_b)
    time.sleep(2)

    screen_width, screen_height = get_work_area_dimensions()

    git_bash_a_window_name = get_git_bash_name(folder_a)
    git_bash_a_window = gw.getWindowsWithTitle(git_bash_a_window_name)[0]
    move_window_to(git_bash_a_window, position='left',
                   left_offset=200, top_offset=325)

    git_bash_b_window_name = get_git_bash_name(folder_b)
    git_bash_b_window = gw.getWindowsWithTitle(git_bash_b_window_name)[0]

    move_window_to(git_bash_b_window, position='right',
                   left_offset=200, top_offset=325)

    # Open vscode in both folders and position opened windows.
    open_vscode_in_folder(folder_a)
    time.sleep(5)
    open_vscode_in_folder(folder_b)
    time.sleep(5)

    visual_studio_windows_names = get_visual_studio_windows_names()

    files = ''
    vs_references = get_resource_path('visual_studio_files_references.json')
    with open(vs_references, 'r') as file:
        files = json.load(file)

    visual_studio_a_window_name = select_visual_studio_window(
        files['file_a'], visual_studio_windows_names)

    if activate_window(visual_studio_a_window_name):
        time.sleep(1.1)  # Wait to ensure the window is active
        snap_window_to_side('left')
        time.sleep(1.1)

    visual_studio_b_window_name = select_visual_studio_window(
        files['file_b'], visual_studio_windows_names)

    if activate_window(visual_studio_b_window_name):
        time.sleep(1.1)  # Wait to ensure the window is active
        snap_window_to_side('right')
        time.sleep(1.1)

except Exception as e:
    print(e)
    traceback.print_exc()
