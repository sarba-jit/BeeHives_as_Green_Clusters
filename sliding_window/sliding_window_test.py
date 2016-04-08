from helpers import sliding_window
from helpers import sliding_window_x
import time
import cv2
import os

test_path = '/home/sarbajit/PycharmProjects/BeeHive/sliding_test_image/'
count = 0

for root, dirs, files in os.walk(test_path):
    for item in files:
        if item.endswith(".png"):
            x=os.path.join(root, item)
            target = cv2.imread(x)
            target = target[90:150, 90:520]
            (winW, winH) = (50, 30)
            for (x, y, window) in sliding_window_x(target,stepSize=30, windowSize=(winW, winH)):
                # if the window does not meet our desired window size, ignore it
                if window.shape[0] != winH or window.shape[1] != winW:
                    continue
                # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW,AND DO THE NECESSARY STEPS
                count = count+1
                # we'll just draw the window and show the results
                clone = target.copy()
                cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
                cv2.imshow("window", clone)
                cv2.waitKey(1)
                time.sleep(0.5)


print count