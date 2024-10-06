import os
import json
import time
from typing import List
import pygetwindow as gw
from pywinauto import application


def get_folder_name(folder_path: str) -> str:
    return folder_path.split('\\')[-1]


# Opens two working folders.
with open('folders.json', 'r') as file:
    folders = json.load(file)

folder_a = folders['folder_a']
folder_b = folders['folder_b']

os.startfile(folder_a)
os.startfile(folder_b)

# Moves windows to a part of the screen.

folder_a_name: str = get_folder_name(folder_a)
folder_b_name: str = get_folder_name(folder_b)

time.sleep(2)
windows: List[str] = gw.getAllTitles()

folder_a_window = [w for w in windows if folder_a_name in w.lower()]
folder_b_window = [w for w in windows if folder_b_name in w.lower()]
