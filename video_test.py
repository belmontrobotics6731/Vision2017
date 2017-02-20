import cv2
import time
from vision.camera import Camera
import vision.finder as finder

camera = Camera(0, 100)

#cv2.imshow("video", camera.get_image());

while 1:
	start_time = time.time()

	im = camera.capture();

#	edg = cv2.Canny(im, 50, 250)

	p = finder.findPoints(im)

	#cv2.imshow("video", p)

	#if cv2.waitKey(1) > 0:
	#	break

	print("frame time: %.3f" % (time.time() - start_time))
