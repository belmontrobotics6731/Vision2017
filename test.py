import cv2
from networktables import NetworkTables

from vision.camera import Camera
import vision.finder as finder


camera = Camera(0, 10)

img=camera.get_image()

img = finder.findPoints(img)

cv2.imshow("image", img)
cv2.waitKey(0)

cv2.destroyAllWindows()

del(camera)

