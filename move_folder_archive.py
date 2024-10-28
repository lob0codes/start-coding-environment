def get_work_area_dimensions():
    user32 = ctypes.windll.user32
    work_area = ctypes.wintypes.RECT()
    user32.SystemParametersInfoW(
        48, 0, ctypes.byref(work_area), 0)  # SPI_GETWORKAREA
    work_width = work_area.right - work_area.left
    work_height = work_area.bottom - work_area.top
    return work_width, work_height


def move_window_to(target_window, position, screen_w):

    target_y = 0

    if position == 'left':
        target_x = 0

    elif position == 'right':
        target_x = screen_w // 2

    target_window.moveTo(target_x, target_y)


screen_width, screen_height = get_work_area_dimensions()

time.sleep(1)

folder_a_window = gw.getWindowsWithTitle(folder_a_name)[0]
move_window_to(folder_a_window, position='left', screen_w=screen_width)
folder_a_window.resizeTo((screen_width // 2) + 10, screen_height + 5)

folder_b_window = gw.getWindowsWithTitle(folder_b_name)[0]
move_window_to(folder_b_window, position='right', screen_w=screen_width)
folder_b_window.resizeTo((screen_width // 2) + 5, screen_height + 5)
