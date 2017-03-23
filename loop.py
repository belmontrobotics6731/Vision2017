# includes
import cv2
import numpy as np
from networktables import NetworkTable

import time
import math
import sys
import threading
import usb.core

from vision.camera import Camera
import vision.finder as finder


# constants

SHOW_IMAGE = True
USE_VISION = True
CAMERA_WIDTH = 480
CAMERA_HEIGHT = 270
HEIGHT_DIFF = (21.75 - 13.25) * 0.0254  # meters
CAMERA_START_INDEX = 0
CAMERA_MAX_INDEX = 2

# functions

def connectionListener(conn, inf):
        print(inf, '; Connected=%s' % conn)


# init

if SHOW_IMAGE :
        cv2.startWindowThread()
        cv2.namedWindow("image")

camera = None

def find_camera():
	global camera
	
	cidx = CAMERA_START_INDEX

	while True :
		try:
			if camera:
				del(camera)

			print(cidx)

			camera = Camera(cidx, 10)
			camera.set(3, CAMERA_WIDTH)
			camera.set(4, CAMERA_HEIGHT)
			camera.set(5, 20)

			cidx = cidx + 1
			if cidx > CAMERA_MAX_INDEX:
				cidx = CAMERA_START_INDEX

			if camera == None:
				print("none")

			im = camera.get_image()

			if im == None:
				continue

			h,w,_ = im.shape

			print("%d, %d" % (h, w))

			if w < 1 or h < 1:
				continue
		
			if SHOW_IMAGE :
				cv2.imshow("image", im)

			break

		except (KeyboardInterrupt, SystemExit):
			sys.exit()
		except:
			time.sleep(0.01)
			pass

find_camera()

print("done")

NetworkTable.setIPAddress("roboRIO-6731-FRC.local")
NetworkTable.setClientMode()
NetworkTable.initialize()

vtable = NetworkTable.getTable("vision")

NetworkTable.addConnectionListener(connectionListener, immediateNotify=True)

# main

vtable.putNumber("centerX", CAMERA_WIDTH / 2.0)
vtable.putNumber("centerY", CAMERA_HEIGHT / 2.0)
vtable.putNumber("area1", 0.0)
vtable.putNumber("area2", 0.0)
vtable.putNumber("offset", 0.0)
vtable.putNumber("distance", 0.0)


dev_count = -1

def count_devices():
	global dev_count
	count = 0

	dev = usb.core.find()
#	count = len(dev)

	for d in dev:
		count = count + 1

	print("count: %d" % count)

	if count != dev_count and dev_count != -1:
		find_camera()

	dev_count = count

#threading.Timer(2.0, count_devices).start()

while True:

	try:
		st = time.time()

#		print("here")

#		count_devices()

		img = camera.capture()

	#	if img == None:
	#		find_camera()
	#		break
	#	else:
	#		h,w,_ = img.shape

	#		if h < 1 or w < 1:
	#			print("x")
	#			find_camera()
	#			break

#		print("there")

		if USE_VISION:
			img,a1,a2,c1,c2,ct = finder.findPoints(img, SHOW_IMAGE)

			fovh = 30.686  # degrees
			x = 8.0 * 0.0254  # meters
			w = 1.0  # meters
			h = w * CAMERA_HEIGHT / CAMERA_WIDTH
			xp = w * abs((c1[0] - CAMERA_WIDTH/2.0) - (c2[0] - CAMERA_WIDTH/2.0)) / CAMERA_WIDTH  # meters
			ep = w * (ct[0] - CAMERA_WIDTH/2.0) / CAMERA_WIDTH  # meters

			cy = h * (ct[1] - CAMERA_HEIGHT/2.0) / CAMERA_HEIGHT  # meters

			d = HEIGHT_DIFF
			if xp > 0.00001 :
				d = (x / xp) * math.sqrt(math.pow(w / (math.tan(math.radians(fovh)) * 2.0), 2.0) + cy*cy)  # meters
			d = math.sqrt(d * d - HEIGHT_DIFF * HEIGHT_DIFF)
		
			e = x * ep / xp

#			print("d: %f, e: %f" % (d, e))
#			print("ct: %f" % c1[0])	
			print("a1: %f, a2: %f, cx: %f, cy: %f" % (a1, a2, ct[0], ct[1]))

			vtable.putNumber("centerX", ct[0])
			vtable.putNumber("centerY", ct[1])
			vtable.putNumber("area1", a1)
			vtable.putNumber("area2", a2)
			vtable.putNumber("offset", e)
			vtable.putNumber("distance", d)

		if SHOW_IMAGE :
			cv2.imshow("image", img)

		print("Frame time: %f" % (time.time() - st))

	except (KeyboardInterrupt, SystemExit):
		break
	except:
		pass

cv2.destroyAllWindows()

del(camera)
