import time
import cv2
import base64
import searchFace
from accounts import mysql
camera_port0 = 0
camera1 = cv2.VideoCapture(camera_port)
time.sleep(0.1)  # If you don't wait, the image will be dark

while True:
    return_value, image = camera.read()
    img_b64 = base64.b64decode(image)

    # cv2.imwrite("Faced-check-in/pic/cvv%s.jpg" % time.time(), image)
    user_id = searchFace.search(img_b64)
    
    time.sleep(1)
# del(camera)  # so that others can use the camera as soon as possible