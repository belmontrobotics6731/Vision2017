import cv2
import numpy as np

class Camera(object):

	def __init__(self, camera_port, discard_frames):
		self.camera_port = camera_port
		self.discard_frames = discard_frames
		self.camera = cv2.VideoCapture(self.camera_port)

	def __def__(self):
		del(self.camera)

	def set(self, p, v):
		self.camera.set(p, v)

	def capture(self):
		retval, im = self.camera.read()
		#im = cv2.resize(im, (640,480))
		if retval:
			return im
		else:
			print("fail")
			return np.zeros((0,0,3), np.uint8)

	def get_image(self):
		for i in range(self.discard_frames):
			temp = self.capture()

		return self.capture()


#  cv2.imwrite("./pic.png", image)


