import cv2 as cv
import numpy as np
import os

def normal_thresh_detect(img, IntersectionAreas = {}):
    test_thresh = cv.threshold(img, 127, 225, cv.THRESH_BINARY)[1]

    files = os.listdir('./Sample Images')
    for file in files:
        sample, SampleIntersections = cv.imread(f'Sample Images/{ file }'), []
        sample_thresh = cv.threshold(sample, 127, 225, cv.THRESH_BINARY)[1]

        for color_channel in range(3):
            test_hist = cv.calcHist([test_thresh], [color_channel], None, [256], [0, 256])
            sample_hist = cv.calcHist([sample_thresh], [color_channel], None, [256], [0, 256])   

            SampleIntersections.append( np.sum( np.minimum(test_hist, sample_hist) ) )

        IntersectionAreas[ file ] = sum( SampleIntersections )

    return max(IntersectionAreas, key=lambda x: IntersectionAreas[x])


def adaptive_thresh_detect(test_img, IntersectionAreas = {}):
    test_threshs = [ cv.adaptiveThreshold(channel, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 7) for channel in cv.split(test_img) ]

    files = os.listdir('./Sample Images')
    for file in files:
        sample_img, SampleIntersection = cv.imread(f'Sample Images/{ file }'), 0
        sample_threshs = [ cv.adaptiveThreshold(channel, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 15, 12) for channel in cv.split(sample_img) ]

        for channel in range(3):
            test_hist = cv.calcHist(test_threshs[ channel ], [channel], None, [256], [0, 256])
            sample_hist = cv.calcHist(sample_threshs[ channel ], [channel], None, [256], [0, 256])   

            SampleIntersection += np.sum( np.minimum(test_hist, sample_hist) )

        IntersectionAreas[ file ] = SampleIntersection

    return max(IntersectionAreas, key=lambda x: IntersectionAreas[x])


test_num = int(input())

img = cv.imread(f'test images/test{ test_num }.jpg')
img = cv.resize(img, (190, 90))

if test_num == 1 : 
    print( normal_thresh_detect(img) )

elif test_num == 2 :
    Canny = cv.Canny(img, 50, 150)

    contours = cv.findContours(Canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)[0]

    approx_contours = []
    for i in range( len(contours) ):
      approx_contours.append( cv.approxPolyDP(contours[i], 0.01 * cv.arcLength(contours[i], True), True) )

    cnt = max(approx_contours, key=lambda x: cv.contourArea(x, True)) # ...

    input_pts, output_pts = np.float32([(10, 10), (185, 23.788), (5, 71.5), (188, 68.5)]), np.float32([(0, 0), (190, 0), (0, 90), (190, 90)])
    M = cv.getPerspectiveTransform(input_pts, output_pts)
    perspective_img = cv.warpPerspective(img, M, (190, 90))

    print( normal_thresh_detect(perspective_img) )