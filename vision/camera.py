import cv2

class Camera(object):

	def __init__(self, camera_port, discard_frames):
		self.camera_port = camera_port
		self.discard_frames = discard_frames
		self.camera = cv2.VideoCapture(self.camera_port)
		#cap = cv2.VideoCapture(0)
		#cap.set(3,640)
		#cap.set(4,480)
	def __def__(self):
		del(self.camera)

	def capture(self):
		retval, im = self.camera.read()
		#im = cv2.resize(im, (640,480))
		return im

	def get_image(self):
		for i in range(self.discard_frames):
			temp = self.capture()

		return self.capture()


#  cv2.imwrite("./pic.png", image)


