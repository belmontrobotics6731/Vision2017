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

table = NetworkTable.getTable("SmartDashboard")

while 1:
	print(table.getNumber("Left encoder", 0.0))

