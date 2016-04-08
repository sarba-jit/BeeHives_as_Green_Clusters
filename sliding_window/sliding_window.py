from helpers import sliding_window_test
import time
import cv2


def sliding_window(image,r1,r2,step,roihist):
    test_path = "/home/sarbajit/PyCharm_Scripts/test/green_pad_same_name_new/final_rotated2/"
    item = image
    if item.endswith(".png") or item.endswith(".PNG"):
        x = test_path+item
        target2 = cv2.imread(x)
        target = target2[90:150, 90:520]
        (winW, winH) = (50, 30)
        for (x, y, window) in sliding_window_test(target,r1,r2,stepSize=step, windowSize=(winW, winH)):
            # if the window does not meet our desired window size, ignore it
            if window.shape[0] != winH or window.shape[1] != winW:
                continue
            #this section does the histogram backprojected matching window by window.
            hsvt = cv2.cvtColor(window, cv2.COLOR_BGR2HSV)
            inputImage = cv2.calcHist([hsvt], [0, 1], None, [180, 256], [0, 180, 0, 256])
            cv2.normalize(roihist, roihist, 0, 255, cv2.NORM_MINMAX)
            dst = cv2.calcBackProject([hsvt], [0, 1], roihist, [0, 180, 0, 256], 1)
            match = cv2.compareHist(roihist, inputImage, method=0)
            print match
            #the match is printed to see the difference and jumps when the window moves through the landing pad

            # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW,AND DO THE NECESSARY STEPS

        # we'll just draw the window and show the results
            clone = target.copy()
            cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
            cv2.imshow("window", clone)
            cv2.waitKey(1)
            time.sleep(1)

# sliding_window('2015-08-06_06-27-48.png',28,58,30)