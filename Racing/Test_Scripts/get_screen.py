"""
A script to continuously capture part of the computer screen and print some
loop time information for consideration during implementation.
"""

import numpy as np
from PIL import ImageGrab
import cv2
import time

def process_img(img):
    """
    A simple processing function to check that no FPS is sacrificed in
    processing of the captured image.
    """
    p_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    p_img = cv2.Canny(p_img, threshold1=200, threshold2=200)
    return p_img

# Location parameters for desired region of screen
x0,xf = 0,600
y0,yf = 40,340

# Start timer for timing the loop
t = time.time()

while True:
    # Continually get an np array of the capture and process it
    scn = np.array(ImageGrab.grab(bbox=(x0, y0, xf, yf)))
    p_scn = process_img(scn)

    # Show the processed capture (or the original)
    cv2.imshow('window', p_scn)
    #cv2.imshow('window',cv2.cvtColor(scn, cv2.COLOR_BGR2RGB))

    # Press q to close window
    if cv2.waitKey(25) == ord('q'):
        cv2.destroyAllWindows()
        break

    # Print update time (for comparison with game's FPS)
    print(f"Last update took {time.time()-t:.5} seconds\n"
          f"\t\tand {1/(time.time()-t):.5} FPS.")
    t = time.time()
