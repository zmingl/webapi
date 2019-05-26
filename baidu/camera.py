import time
import cv2
import base64
import searchFace
import requests
import json

# 电脑默认摄像头的port为0，当连接不同的USB摄像头时，查看摄像头端口，进行赋值
# 设计：1为签到；2为离开
camera_port1 = 0
#camera_port2 = 1
camera1 = cv2.VideoCapture(camera_port1)
# 启用第二个摄像头
# camera2 = cv2.VideoCapture(camera_port2)
time.sleep(0.1)  #等待摄像头初始化完成，避免拍出的照片亮度暗

meeting_id = 3

while True:
    return_value, image = camera1.read()
    return_value, buffer = cv2.imencode('.jpg', image)
    img_b64= base64.b64encode(buffer).decode("utf-8")
    user_ids = searchFace.search(img_b64)
    for user_id in user_ids:
        user_info = {'user_id': user_id , 'meeting_id': meeting_id , 'status' : '已签到'}
        user_info = json.dumps(user_info)
        r = requests.post("http://127.0.0.1:8000/accounts/update_user_status",data = user_info)
    time.sleep(1)