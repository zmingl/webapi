from aip import AipFace
from . import constant
from . import intobase
import base64     

client = AipFace(constant.APP_ID, constant.API_KEY, constant.SECRET_KEY)

# image = intobase.get_file_content('/Users/mei/python/webapi/Faced-check-in/pic/cvv.jpg')

imageType = "BASE64"

groupId = "1"

userId = "9"

""" 调用人脸注册 """

""" 如果有可选参数 """
options = {}
options["user_info"] = "user's info"
options["quality_control"] = "NORMAL"
options["liveness_control"] = "LOW"

""" 带参数调用人脸注册 """
# client.addUser(image, imageType, groupId, userId, options)

def registerFace(Id,pic_base64):
    userId = Id
    ret = client.addUser(pic_base64, imageType, groupId, userId)
    if ret:
        print (ret)
        return True
