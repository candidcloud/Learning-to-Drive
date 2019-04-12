"""
A script to press a single key for a given time interval and release it.
This is meant to be tested while a game is open.
"""

import pyautogui
import time

# Countdown to key being pressed
for i in list(range(5))[::-1]:
    print(i+1)
    time.sleep(1)

# Press the key
print('Pressing key...')
pyautogui.keyDown('up')

# Hold
time.sleep(3)

# Release the key
print('Releasing key...')
pyautogui.keyUp('up')
print('Completed Test!')
