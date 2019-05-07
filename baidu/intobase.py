import base64
""" 读取图片 """
def get_file_content(filename):
    with open(filename, "rb") as fp:
        data = base64.b64encode(fp.read()).decode("utf-8")
        # print(data)
        return data