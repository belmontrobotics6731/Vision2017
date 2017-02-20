import cv2
from vision.camera import Camera
import vision.finder as finder
# from tape_parser import TapeParser

camera = Camera(0, 10)

img = camera.get_image()

# edg = cv2.Canny(img, 100, 200)

img = finder.findPoints(img)

cv2.imshow("image", img)
cv2.waitKey(0)

cv2.destroyAllWindows()

del(camera)
