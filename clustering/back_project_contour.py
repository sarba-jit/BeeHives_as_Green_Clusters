import cv2
import numpy as np
import os
import time

start_time = time.time()


# Function for sorting the lengths of the contour list
def list_sorted_length(number_list):
    for item1 in range(0, len(number_list)):
        for item2 in range(item1 + 1, len(number_list)):
            if len(number_list[item1]) > len(number_list[item2]):
                temp = number_list[item2]
                number_list[item2] = number_list[item1]
                number_list[item1] = temp
    return number_list


##Function for sorting the list
def list_sorted(number_list):
    for item1 in range(0, len(number_list)):
        for item2 in range(item1 + 1, len(number_list)):
            if number_list[item1] > number_list[item2]:
                temp = number_list[item2]
                number_list[item2] = number_list[item1]
                number_list[item1] = temp
    return number_list


##Function for finding the contours
def contour_finding(gray_image):
    test_path = "/home/sarbajit/PyCharm_Scripts/test/back_project_test/results_gray/"
    for root, dirs, files in os.walk(test_path):
        item = gray_image
        if item.endswith(".png") or item.endswith(".PNG"):
            x = os.path.join(root, item)
            im = cv2.imread(x)
            imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            # print item
            ret, thresh = cv2.threshold(imgray, 25, 255, 0)
            # Find the contours
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contour_list = []

            # Append the Contours in a list
            for item4 in contours:
                contour_list.append(item4)

            # Sort the length of each contours in the list in order to find the most significant contour
            contour_list = list_sorted_length(contour_list)
            cmt = []

            # Using only the largest contour
            for index in range(len(contour_list) - 1, len(contour_list) - 2, -1):
                cmt.append(contour_list[index])

            # Drawing the Largest contour on the image
            cv2.drawContours(im, cmt, -1, (0, 255, 0), 3)
            cv2.imwrite('/home/sarbajit/PyCharm_Scripts/test/back_project_test/results_contour/' + item, im)

            ####PROCESSING THE LARGEST CONTOUR:
            ##The col_width and the row_height will be used to determine the tracking rectangle.

            # Processing the starting and end point of the contour with respect to the columns
            col_cmt = []
            for item5 in range(len(cmt[0])):
                col_cmt.append(cmt[0][item5][0][0])

            col_cmt = list_sorted(col_cmt)
            col_width = col_cmt[len(col_cmt) - 1] - col_cmt[0]

            # Processing the starting and end point of the contour with respect to the rows
            row_cmt = []
            for item5 in range(len(cmt[0])):
                row_cmt.append(cmt[0][item5][0][1])

            row_cmt = list_sorted(row_cmt)
            row_height = row_cmt[len(row_cmt) - 1] - row_cmt[0]

            return row_cmt[0], col_cmt[0], len(col_cmt), row_height, col_width



test_path = "/home/sarbajit/PyCharm_Scripts/test/green_pad_same_name_new/final_rotated/"
roi = cv2.imread('/home/sarbajit/PyCharm_Scripts/test/back_project_test/test18.png')
hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

for root, dirs, files in os.walk(test_path):
    for item in files:
        if item.endswith(".png"):
            x=os.path.join(root, item)
            target = cv2.imread(x)
            #target = target[70:160,90:500]
            target = target[90:150,110:470]
            hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)

            # calculating object histogram
            roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
            inputImage = cv2.calcHist([hsvt],[0, 1], None, [180, 256], [0, 180, 0, 256] )


            # normalize histogram and apply backprojection
            cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
            dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)
            #print dst

            match = cv2.compareHist(roihist,inputImage,method=0)
            #print match
            my_file = open('/home/sarbajit/PyCharm_Scripts/test/back_project_test/txt_results/match.txt','a')
            my_file.write(item+': '+str(match)+'\n')
            my_file.close()

            # Now convolute with circular disc
            disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            cv2.filter2D(dst,-1,disc,dst)
            # threshold and binary AND
            ret,thresh = cv2.threshold(dst,50,255,0)
            thresh = cv2.merge((thresh,thresh,thresh))
            res = cv2.bitwise_and(target,thresh)

            #res = np.vstack((target,thresh,res))
            #cv2.imwrite('test/back_project_test/test4.png',res)
            cv2.imwrite("/home/sarbajit/PyCharm_Scripts/test/back_project_test/results/"+item, res)
            print 'item: '+item+' done'
            if match > 0.2:
                my_file = open('/home/sarbajit/PyCharm_Scripts/test/back_project_test/txt_results/highmatch.txt','a')
                my_file.write(item+': '+str(match)+'\n')
                my_file.close()
                cv2.imwrite("/home/sarbajit/PyCharm_Scripts/test/back_project_test/txt_results/"+item, res)
                color_res = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
                gray_res = cv2.cvtColor(color_res, cv2.COLOR_BGR2GRAY)
                cv2.imwrite("/home/sarbajit/PyCharm_Scripts/test/back_project_test/results_gray/" + item, gray_res)
                r, c, length_contour, row_height, col_width = contour_finding(item)
                print length_contour

print("--- %s seconds ---" % (time.time() - start_time))
