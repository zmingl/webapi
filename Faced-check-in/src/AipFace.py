# -*- coding: utf-8 -*-
from aip import AipFace
import constant
import base64
from PIL import Image
import sys
import os
import time
import json
from io import BytesIO


"""图像分割"""
def crop(path, input, height, width, page):
    k = 0
    im = Image.open(input)
    imgwidth, imgheight = im.size
    images = []
    """软切割"""
    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            x0 = j - width * 0.2
            if (x0<0):
                x0 = 0
            y0 = i - height * 0.2
            if(y0<0):
                y0 = 0
            x1 = j + width
            if (x1 > imgwidth):
                x1 = imgwidth
            y1 = i + height
            if (y1 > imgheight):
                y1 = imgheight      
            box = (x0, y0, x1, y1)    
            buffer = BytesIO()
            im.crop(box).save(buffer,"JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8") 
            images.append(img_str)
            # im.crop(box).save(os.path.join(path,"PNG","%s" % page,"IMG-%s.png" % k))
            k +=1
    return images
images = crop('/Users/mei/python/webapi/Faced-check-in','/Users/mei/python/webapi/Faced-check-in/src/people-to-people.jpg',200,200,'ww')

""" 读取图片 """
def get_file_content(filename):
    with open(filename, "rb") as fp:
        date = str(base64.b64encode(fp.read()))
        return date

client = AipFace(constant.APP_ID, constant.API_KEY, constant.SECRET_KEY)

# image = get_file_content('/Users/mei/Faced-check-in/harry-meghan-15.jpg')

imageType = "BASE64"

""" 调用人脸检测 """
# ret = client.detect(image, imageType)
""" 如果有可选参数 """
options = {}
options["face_field"] = "age"
options["max_face_num"] = 10
options["face_type"] = "LIVE"

""" 带参数调用人脸检测 """

faces = []
for image in images:
    ret = client.detect(image, imageType, options)
    if (ret['result'] != None):
        face_list = ret['result']['face_list']
        for f in face_list :
            faces.append(f)
            print (f['face_token'])
    time.sleep(0.5)
print(len(faces))