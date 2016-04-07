from helpers import sliding_window
import time
import cv2
import os

test_path = '/home/sarbajit/PycharmProjects/BeeHive/sliding_test_image/'

for root, dirs, files in os.walk(test_path):
    for item in files:
        if item.endswith(".png"):
            x=os.path.join(root, item)
            target = cv2.imread(x)
            (winW, winH) = (50, 30)
            for (x, y, window) in sliding_window(target, stepSize=5, windowSize=(winW, winH)):
                # if the window does not meet our desired window size, ignore it
                if window.shape[0] != winH or window.shape[1] != winW:
                    continue

                # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW,AND DO THE NECESSARY STEPS

                # we'll just draw the window and show the results
                clone = target.copy()
                cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
                cv2.imshow("window", clone)
                cv2.waitKey(1)
                time.sleep(0.025)
