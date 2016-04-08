# import the necessary packages
import imutils


def pyramid(image, scale=1.5, minSize=(30, 30)):
    # yield the original image
    yield image

    # keep looping over the pyramid
    while True:
        # compute the new dimensions of the image and resize it
        w = int(image.shape[1] / scale)
        image = imutils.resize(image, width=w)

        # if the resized image does not meet the supplied minimum
        # size, then stop constructing the pyramid
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break

        # yield the next image in the pyramid
        yield image


def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])



def sliding_window_test(image,r1,r2,stepSize,windowSize):
    # slide a window across the image
    # r1=19
    # r2=49
    # stepSize=30
    for y in xrange(r1,r2, stepSize):
        #The starting point for y in xrange should be row_cmt[0] that would come directly after running contour function of the image.
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


def sliding_window_x(image,stepSize,windowSize):
    # slide a window across the image
    # r1=19
    # r2=49
    # stepSize=30
    for y in xrange(28,58, stepSize):
        #The starting point for y in xrange should be row_cmt[0] that would come directly after running contour function of the image.
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])