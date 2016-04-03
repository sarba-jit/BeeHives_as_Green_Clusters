import cv2
import numpy as np
import os

test_path = "/home/sarbajit/PyCharm_Scripts/test/green_pad_same_name_new/2015-08-08/"

for root, dirs, files in os.walk(test_path):
    for item in files:
        if item.endswith(".png"):
            x=os.path.join(root, item)
            target = cv2.imread(x)
            target = target[125:135,150:350]
            cv2.imwrite("/home/sarbajit/PyCharm_Scripts/test/back_project_test/roi_day/"+item, target)
