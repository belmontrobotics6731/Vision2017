# includes
import cv2
from networktables import NetworkTable

import time
import math

from vision.camera import Camera
import vision.finder as finder


# constants

SHOW_IMAGE = True
USE_VISION = True
CAMERA_WIDTH = 480.0
CAMERA_HEIGHT = 270.0
HEIGHT_DIFF = (21.75 - 13.25) * 0.0254  # meters

# functions

def connectionListener(conn, inf):
        print(inf, '; Connected=%s' % conn)


# init
camera = Camera(1, 10)
camera.set(3, CAMERA_WIDTH)
camera.set(4, CAMERA_HEIGHT)
camera.set(5, 20)

NetworkTable.setIPAddress("roboRIO-6731-FRC.local")
NetworkTable.setClientMode()
NetworkTable.initialize()

vtable = NetworkTable.getTable("vision")

NetworkTable.addConnectionListener(connectionListener, immediateNotify=True)

if SHOW_IMAGE :
        cv2.startWindowThread()
        cv2.namedWindow("image")
        cv2.imshow("image", camera.get_image())

# main

while True:
	st = time.time()

	img = camera.capture()

	if USE_VISION:
		img,a1,a2,c1,c2,ct = finder.findPoints(img, SHOW_IMAGE)

		fovh = 30.686  # degrees
		x = 8.0 * 0.0254  # distance between tapes (meters)
		w = 1.0  # meters
		h = w * CAMERA_HEIGHT / CAMERA_WIDTH  # meters
		dc = 0.5 * w / math.tan(math.radians(fovh))  # meters
#		xp = w * abs((c1[0] - CAMERA_WIDTH/2.0) - (c2[0] - CAMERA_WIDTH/2.0)) / CAMERA_WIDTH  # meters
		cx = w * (ct[0] - CAMERA_WIDTH/2.0) / CAMERA_WIDTH  # meters
		cy = h * (ct[1] - CAMERA_HEIGHT/2.0) / CAMERA_HEIGHT  # meters

		#d = (dc * HEIGHT_DIFF / cx) * math.sqrt((dc*dc + cy*cy + cx*cx) / (dc*dc + 2.0*cy*cy))
		d = dc * HEIGHT_DIFF / cy

		#e = cx * math.sqrt((d*d + HEIGHT_DIFF*HEIGHT_DIFF) / (dc*dc + cy*cy))
		e = cx * HEIGHT_DIFF / cy

		print("d: %f, e: %f" % (d, e))
#		print("c: %f, %f" % (cx, cy))	
#		print("a1: %f, a2: %f, cx: %f, cy: %f" % (a1, a2, ct[0], ct[1]))

		vtable.putNumber("centerX", ct[0])
		vtable.putNumber("centerY", ct[1])
		vtable.putNumber("area1", a1)
		vtable.putNumber("area2", a2)
		vtable.putNumber("offset", e)
		vtable.putNumber("distance", d)

	if SHOW_IMAGE :
		cv2.imshow("image", img)

	print("Frame time: %f" % (time.time() - st))


cv2.destroyAllWindows()

del(camera)
