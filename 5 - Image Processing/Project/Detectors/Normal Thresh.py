import cv2 as cv
import numpy as np
import os

def detect(img, IntersectionAreas = {}):
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