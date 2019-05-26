from aip import AipFace
import base64
import json

# -*- coding: utf-8 -*-

""" 你的 APPID AK SK ! """
constant = {
        'APP_ID' :'15357248',
        'API_KEY' : 'yxo2FSEQkMny6j7PYO4ZEpLO',
        'SECRET_KEY' : 'H9sWswmLhc0bpM8tbStKP7todCIepN0P'
}




client = AipFace(constant['APP_ID'], constant['API_KEY'], constant['SECRET_KEY'])

imageType = "BASE64"
groupIdList = "1"

""" 调用人脸搜索 """
# client.search(image, imageType, groupIdList)

""" 如果有可选参数 """
options = {}
options["quality_control"] = "NORMAL"
options["max_face_num"] = 10
options["match_threshold"] = 50
options["max_user_num"] = 10

""" 带参数调用人脸搜索 """
def search(pic64):
    ret = client.search(pic64,imageType, groupIdList, options)
    print(ret)
    user_ids = []
    error_msg = ret['error_msg']
    if error_msg == 'SUCCESS':
        # user_id = ret['result']['user_list'][0]['user_id']
        for user in ret['result']['face_list']:
                if user['user_list']:
                        user_ids.append(user['user_list'][0]['user_id'])
                print (error_msg,user_ids)
        return user_ids
