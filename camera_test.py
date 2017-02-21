# includes
import cv2
from networktables import NetworkTable

import time

from vision.camera import Camera
import vision.finder as finder


# init
camera = Camera(0, 10)
NetworkTable.setIPAddress("roboRIO-6731-FRC.local")
NetworkTable.setClientMode()
NetworkTable.initialize()

_=camera.get_image()

vtable = NetworkTable.getTable("vision")

# functions

def uploadData():
	img = camera.capture()

	print("picture taken")

	img,a1,a2,ct = finder.findPoints(img)

	#cv2.imshow("image", img)

	vtable.putNumber("centerX", ct[0])
	vtable.putNumber("centerY", ct[1])
	vtable.putNumber("area1", a1)
	vtable.putNumber("area2", a2)


#def valueChanged(table, key, value, isNew):
	#print("Value %s changed to %s" % (key, value))

#	if key == "requestpoint" and value == True :
#		uploadData()
#		vtable.putBoolean("requestpoint", False)

def connectionListener(conn, inf):
	print(inf, '; Connected=%s' % conn)

# main

NetworkTable.addConnectionListener(connectionListener, immediateNotify=True)

#vtable.addTableListener(valueChanged)

while True:
	uploadData()
	#time.sleep(5)

#cv2.imshow("image", img)
#cv2.waitKey(0)

#cv2.destroyAllWindows()

#del(camera)
