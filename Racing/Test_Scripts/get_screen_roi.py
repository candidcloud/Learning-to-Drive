"""
A script to continuously capture part of the computer screen and print some
loop time information for consideration during implementation. The screen
capture is further processed to get a region of interest based on given
vertices.
"""

import numpy as np
from PIL import ImageGrab
import cv2
import time

def roi(img, vertices):
    """
    Cuts out a region of interest from the given image.
    """
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

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
    p_scn = np.array(ImageGrab.grab(bbox=(x0, y0, xf, yf)))
    p_scn = process_img(p_scn)
    # Use vertices to outline part of window needed (and ignore the rest)
    vertices = [np.array([[10,500],[10,300],[300,200],[500,200],
                          [800,500]])]
    p_scn = roi(p_scn, vertices)

    # Show the processed capture
    cv2.imshow('window', p_scn)

    # Press q to close window
    if cv2.waitKey(25) == ord('q'):
        cv2.destroyAllWindows()
        break

    # Print update time (for comparison with game's FPS)
    print(f"Last update took {time.time()-t:.5} seconds\n"
          f"\t\tand {1/(time.time()-t):.5} FPS.")
    t = time.time()
