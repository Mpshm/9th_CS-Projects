from detector import *

img = cv.imread('Test Images/test2.jpg')
img = cv.resize(img, (190, 90))

Canny = cv.Canny(img, 50, 150)

contours = cv.findContours(Canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)[0]

approx_contours = []
for i in range( len(contours) ):
  approx_contours.append( cv.approxPolyDP(contours[i], 0.01 * cv.arcLength(contours[i], True), True) )

cnt = max(approx_contours, key=lambda x: cv.contourArea(x, True))

cv.drawContours(img, [cnt], -1, (255, 0, 255), 2, cv.LINE_AA)
cv.imshow('...', img)
cv.waitKey(0)

input_pts, output_pts = np.float32([(10, 10), (185, 23.788), (5, 71.5), (188, 68.5)]), np.float32([(0, 0), (190, 0), (0, 90), (190, 90)])
M = cv.getPerspectiveTransform(input_pts, output_pts)
perspective_img = cv.warpPerspective(img, M, (190, 90))

print( detect( perspective_img ) )