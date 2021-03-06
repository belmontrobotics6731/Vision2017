import cv2
import numpy as np

sens = 20
boundaries = ([0, 0, 255-sens], [255, sens, 255])

def convertImg(image):
	lower = np.array(boundaries[0], dtype = "uint8" )
	upper = np.array(boundaries[1], dtype = "uint8" )
	#image = cv2.medianBlur(image, 3)
	#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 0)
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	#mask = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hsv = cv2.bitwise_and(image, image, mask = mask)
	
	# TOOO DDDOOOOO BETTER CONVERSION
	
	bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
	gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
	#can = cv2.Canny(mimg, 100, 200)
	return gray

def getContours(image):
	cimg = convertImg(image)
	(_,contours,_) = cv2.findContours(cimg.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	#cv2.drawContours(cimg, contours, -1, (255,0,0), 2)
	return contours

def getCentroid(contour):
	M = cv2.moments(contour)
	x = 0
	y = 0
	if M['m00'] != 0.0:
		x = int(M['m10']/M['m00'])
		y = int(M['m01']/M['m00'])
	return x,y

#def getDistanceFromArea(a):
#	return 454.308943089 * ((0.031 / np.sqrt(a)) + 0.002038)

def findPoints(image, show_image):
	contours = getContours(image)
	max1 = 0
	max2 = 0
	maxcontour1 = None
	maxcontour2 = None

	for contour in contours:
		a = cv2.contourArea(contour)
		if a > max1 :
			max2 = max1
			max1 = a
			maxcontour2 = maxcontour1
			maxcontour1 = contour
		elif a > max2 :
			max2 = a
			maxcontour2 = contour

	c1 = getCentroid(maxcontour1)
	c2 = getCentroid(maxcontour2)

	if show_image :
		cv2.circle(image, c1, 5, (255, 0, 0), 1)
		cv2.putText(image, str(max1), c1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))

		cv2.circle(image, c2, 5, (255, 0, 0), 1)
		cv2.putText(image, str(max2), c2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))


	ct = ((c1[0] + c2[0])/2.0, (c1[1] + c2[1])/2.0)

	return image,max1,max2,c1,c2,ct

def get_thresh(in_img):
	img = cv2.cvtColor(in_img, cv2.COLOR_BGR2GRAY);

	ret, img = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)

	return img
