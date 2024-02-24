import cv2 as cv
import numpy as np
import os

def detect(test_img, IntersectionAreas = {}):
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