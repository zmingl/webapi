from aip import AipFace
from . import constant
import base64
import json
from . import intobase

client = AipFace(constant.APP_ID, constant.API_KEY, constant.SECRET_KEY)

# image = intobase.get_file_content('/Users/mei/python/webapi/Faced-check-in/pic/cvv1556911362.784927.jpg')

imageType = "BASE64"

groupIdList = "1"

""" 调用人脸搜索 """
# client.search(image, imageType, groupIdList)

""" 如果有可选参数 """
options = {}
options["quality_control"] = "NORMAL"
# options["liveness_control"] = "LOW"
# options["user_id"] = "233451"
options["max_user_num"] = 1

""" 带参数调用人脸搜索 """
def search(pic64):
    ret = client.search(pic64,imageType, groupIdList, options)
    # json_data = json.loads(ret)
    error_msg = ret['error_msg']
    if error_msg == 'SUCCESS':
        user_id = ret['result']['user_list'][0]['user_id']
        print (error_msg,user_id)
        return user_id
