from picamera import PiCamera
from time import sleep
import os

if os.path.isfile("image0.jpg"):
	print("Images already captured")

else:
	camera = PiCamera()
	camera.resolution = (1024, 1024)

	for i in range(10):
		imagename = "image" + str(i) + ".jpg"
		print("Capturing " + imagename)
		camera.start_preview()
		sleep(5)
		camera.capture(imagename)
		camera.stop_preview()
		sleep(5)

	print(subprocess.call("sh test.sh"))
