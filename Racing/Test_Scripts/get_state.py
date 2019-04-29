"""
A script to locate a window with title entered by the user.
For q_racer, this is "Go Q-Racer, go Q-Racer, go!" w/o quotes.
"""

import pyautogui

def orient_window():
    window = pyautogui.getWindow("Go Q-Racer, go Q-Racer, go!")
    window.set_position(0,0,2000,1500)


def get_dimensions(window):
    """
    Grabs the dimensions of a given window. For an unknown reason, it is
    necessary to multiply the received dimensions by numbers close to 2.
    """
    rect = win32gui.GetWindowRect(window)
    x = 2*rect[0]
    y = 2*rect[1]
    w = 2*rect[2]
    h = 2*rect[3]
    print(f"Window {win32gui.GetWindowText(window)}: ")
    print(f"\tLocation: {(x, y)}")
    print(f"\t    Size: {(w, h)}")

def main():
    """
    Prompt the user for the title of the desired window and print the
    dimensions.
    """
    win2find = input('Enter window title: ')
    window = win32gui.FindWindowEx(None, None, None, win2find)
    if not (window == 0):
        get_dimensions(window)


if __name__ == '__main__':
    main()
