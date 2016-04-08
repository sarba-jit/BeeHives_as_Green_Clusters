from helpers import sliding_window_test
import time
import cv2
import os
import numpy as np


def sliding_window(image,r1,r2,step):
    count = 0
    test_path = "/home/sarbajit/PyCharm_Scripts/test/green_pad_same_name_new/final_rotated/"
    # for root, dirs, files in os.walk(test_path):
    item = image
    if item.endswith(".png") or item.endswith(".PNG"):
        # x = os.path.join(root, item)
        x = test_path+item
        target2 = cv2.imread(x)
        target = target2[90:150, 90:520]
            # print np.size(target, 0)
        (winW, winH) = (50, 30)
            # print r1
            # print r2
            # print step
        for (x, y, window) in sliding_window_test(target,r1,r2,stepSize=step, windowSize=(winW, winH)):
            # if the window does not meet our desired window size, ignore it
            if window.shape[0] != winH or window.shape[1] != winW:
                continue
                # count = count +1
                # print x
            # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW,AND DO THE NECESSARY STEPS

        # we'll just draw the window and show the results
            clone = target.copy()
            cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
            cv2.imshow("window", clone)
            cv2.waitKey(1)
            time.sleep(0.01)
    # print count


# sliding_window('2015-08-06_06-27-48.png',28,58,30)