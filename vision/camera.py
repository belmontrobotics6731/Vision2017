import cv2

class Camera(object):

	def __init__(self, camera_port, discard_frames):
		self.camera_port = camera_port
		self.discard_frames = discard_frames
		self.camera = cv2.VideoCapture(self.camera_port)

	def __def__(self):
		del(self.camera)

	def capture(self):
		retval, im = self.camera.read()
		return im

	def get_image(self):
		for i in range(self.discard_frames):
			temp = self.capture()

		return self.capture()


#  cv2.imwrite("./pic.png", image)


