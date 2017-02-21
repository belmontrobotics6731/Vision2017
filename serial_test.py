import serial

ser = serial.Serial("/dev/ttyAMA0")
ser.baudrate = 115200

while 1:
	print(ser.read(10))
	ser.write("qasdasd")

ser.close()
