from detector import *

img = cv.imread('Test Images/test1.jpg')
img = cv.resize(img, (190, 90))

print( detect(img) )