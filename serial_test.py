import serial

ser = serial.Serial("/dev/ttyS0")
ser.baudrate = 115200

while 1:
	print(ser.read(10))
	ser.write("1234567890")

ser.close()
