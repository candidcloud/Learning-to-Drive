"""
A script which demonstrates how to locate the car image and draw a rectangle
around the supposed location on a continually updating screen.
"""

import cv2
from PIL import ImageGrab
import numpy as np
import time
import pyautogui

def identify_img(scn):
    """
    Identifies an image on the screen based on a given template. Returns
    the modified screen.
    """
    # Convert to gray
    scn_gray = cv2.cvtColor(scn, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('..\\car25.png',0)

    # Find matches
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(scn_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 1
    loc = np.where( res >= threshold)
    while len(loc[0])==0 and threshold>0.3:
        threshold -= 0.05
        loc = np.where(res >= threshold)

    # Overlay a rectangle on the screen around a likely car
    pt = list(zip(*loc[::-1]))[0]  # Pick only one detected object
    scn = cv2.rectangle(scn, (int(pt[0]-5*w),int(pt[1]-5*h)), (pt[0] + 5*w, pt[1] + 5*h), (255,0,0), 2)
    return scn

# Location parameters for desired region of screen
x0,xf = 0,800
y0,yf = 80,400

# Start timer for timing the loop
t = time.time()

while True:
    # Continually get an np array of the capture and process it
    scn = np.array(ImageGrab.grab(bbox=(x0, y0, xf, yf)))
    scn = cv2.cvtColor(scn, cv2.COLOR_BGR2RGB)
    scn = identify_img(scn)

    # Show the processed capture (or the original)
    cv2.imshow('window', scn)

    # Press q to close window
    if cv2.waitKey(25) == ord('q'):
        cv2.destroyAllWindows()
        break

    # Print update time (for comparison with game's FPS)
    print(f"Last update took {time.time()-t:.5} seconds\n"
          f"\t\tand {1/(time.time()-t):.5} FPS.")
    t = time.time()
