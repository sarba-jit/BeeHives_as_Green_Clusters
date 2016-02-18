import cv2.cv as cv
import cv2
import matplotlib.pyplot as plt
import math
import os

test_path = "test/green_pad_same_name_new/skewed_images/"

for root, dirs, files in os.walk(test_path):
    for item in files:
        if item.endswith(".png"):
            x=os.path.join(root, item)
            im = cv.LoadImage(x, cv.CV_LOAD_IMAGE_GRAYSCALE)
            dst_32f = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_32F, 1)

            neighbourhood = 3
            aperture = 3
            k = 0.01
            maxStrength = 0.0
            threshold = 0.01
            nonMaxSize = 3

            cv.CornerHarris(im, dst_32f, neighbourhood, aperture, k)

            minv, maxv, minl, maxl = cv.MinMaxLoc(dst_32f)

            dilated = cv.CloneImage(dst_32f)
            cv.Dilate(dst_32f, dilated) # By this way we are sure that pixel with local max value will not be changed, and all the others will

            localMax = cv.CreateMat(dst_32f.height, dst_32f.width, cv.CV_8U)
            cv.Cmp(dst_32f, dilated, localMax, cv.CV_CMP_EQ) #compare allow to keep only non modified pixel which are local maximum values which are corners.

            threshold = 0.01 * maxv
            cv.Threshold(dst_32f, dst_32f, threshold, 255, cv.CV_THRESH_BINARY)

            cornerMap = cv.CreateMat(dst_32f.height, dst_32f.width, cv.CV_8U)
            cv.Convert(dst_32f, cornerMap) #Convert to make the and
            cv.And(cornerMap, localMax, cornerMap) #Delete all modified pixels

            radius = 3
            thickness = 1

            l = []
            for x in range(cornerMap.height): #Create the list of point take all pixel that are not 0 (so not black)
                for y in range(cornerMap.width):
                    if cornerMap[x,y]:
                        l.append((y,x))

            for center in l:
                cv.Circle(im, center, radius, (255,255,255), thickness)


            #cv.ShowImage("Image", im)
            #cv.ShowImage("CornerHarris Result", dst_32f)
            #cv.ShowImage("Unique Points after Dilatation/CMP/And", cornerMap)
            #cv.WaitKey(0)

            #print l
            #print l[224]
            #print l[224][1]
            #print l[224][0]
            #print len(l)

            first_line = {}


            #Creating a dictionary of key value pair, where each key represents the row number and the value represents a lists of edges found on that row

            for item1 in range(300):
                line_1=[]
                for item2 in range(len(l)):
                    if l[item2][1] == item1:
                        line_1.append(l[item2])
                if len(line_1)!=0:
                    first_line[item1]=line_1 #Using only those row values that has edges on it

            second_line={}

            for item1 in range(720):
                line_12=[]
                for item2 in range(len(l)):
                    if l[item2][0] == item1:
                        line_12.append(l[item2])
                if len(line_12)!=0:
                    second_line[item1]=line_12 #Using only those column values that has edges on it

            #print (second_line)
            #print second_line[1]

            #print len(first_line)
            #print first_line[243]


###############################################################################################
        # For plotting the histogram, we calculate in a list the number of points in each row

            hist_plot =[]
            hist_plot_index =[]

            for key in first_line:
                hist_plot.append(len(first_line[key]))
                hist_plot_index.append(key)

            #plt.bar(hist_plot_index,hist_plot)
            #plt.title("Distribution of Horizontal Edges")
            #plt.xlabel("Row Number")
            #plt.ylabel("Frequency")
            #plt.show()

            #print hist_plot_vertical
            #print hist_plot_index_vertical


            hist_plot_vertical =[]
            hist_plot_index_vertical =[]

            for key in second_line:
                hist_plot_vertical.append(len(second_line[key]))
                hist_plot_index_vertical.append(key)


            #plt.bar(hist_plot_index_vertical,hist_plot_vertical)
            #plt.title("Distribution of Vertical Edges")
            #plt.xlabel("Column Number")
            #plt.ylabel("Frequency")
            #plt.show()


            #print hist_plot_vertical
            #print hist_plot_index_vertical

        #######################################################################################

            #for key in second_line:
            #   x=[i for i in range(445,455)]
            #  if key in x:
            #     print len(second_line[key]),

            pad = []
            for x in range(len(hist_plot_vertical)):
                if (hist_plot_vertical[x]-hist_plot_vertical[x-1])<=-4:
                    pad.append(hist_plot_index_vertical[x])

            #print'\n'
            #print pad
#####################################################################################

            pad2 = []

            for x in range(len(hist_plot)):
                if (hist_plot[x]-hist_plot[x-1])<=-6:
                    pad2.append(hist_plot_index[x])


            #for key in first_line:
            #   x=[i for i in range(138,150)]
            #  if key in x:
            #     print len(first_line[key]),


            #print'\n'


        ########################################################################################
            #print pad2
            #print hist_plot[94]
            #print hist_plot[95]
            #print hist_plot[102]
            #print hist_plot[103]

            #print'\n'

            #pad_2=[]

            #for x in range(len(hist_plot)):
            #   if (hist_plot[x]-hist_plot[x-1])<1:
            #      pad_2.append(hist_plot_index[x])

            #for key in range(135,150):
            #   print len(first_line[key]),

            #print'\n'
            #print pad_2

            img = cv2.imread(test_path+item)


            for item_v_l in pad:
                if item_v_l > 135:
                    y_l = item_v_l
                    break

            for item_v_r in pad:
                if item_v_r > 445:
                    y_r = item_v_r
                    break

            for item_h in pad2:
                if item_h > 140:
                    y = item_h
                    break


            #print y_l,
            #print(y_r)
            #print y,
            #print y-45

            if y!=719:
                if (y_r - y_l)!=0:
                    img = img[(y-45):y,y_l:y_r]

                    cv2.imwrite("test/green_pad_same_name_new/pad/"+item, img)


                    #print img.shape
                    x = float(45/3)
                    #print x,
                    angle = math.degrees(math.atan(float(x/(y_r-y_l))))
                    my_file = open('test/green_pad_same_name_new/angles.txt','a')
                    my_file.write(str(angle)+'\n')
                    #print angle
                    my_file.close()

                    if angle < 5:
                        image = cv2.imread(test_path+item)
                        (h, w) = image.shape[:2]
                        center = (w / 2, h / 2)

                        # rotate the image by 'angle' degrees
                        M = cv2.getRotationMatrix2D(center, angle, 1.0)
                        rotated = cv2.warpAffine(image, M, (w, h))
                        cv2.imwrite("test/green_pad_same_name_new/final_rotated/"+item, rotated)
                        print 'item: '+item+' done'
                    else:
                        my_file = open('test/green_pad_same_name_new/rotated_more.txt','a')
                        my_file.write('item no: '+item+'\n')
                        my_file.close()

                else:
                    my_file = open('test/green_pad_same_name_new/no_result.txt','a')
                    my_file.write('item no: '+item+'\n')
                    my_file.close()
            else:
                my_file = open('test/green_pad_same_name_new/pad_not_detected.txt','a')
                my_file.write('item no: '+item+'\n')
                my_file.close()



