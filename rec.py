import base64
import json
import os
import urllib
from urllib import request, parse
from aip import AipFace

APP_ID = '16346340'
API_KEY = 'OFkGXfjm05D5DmpAKSbZT0rC'
SECRET_KEY = 'ANr2qF02hfmHI0ok5Kt3lcYjbrNNF3hX'


def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(
        API_KEY, SECRET_KEY)
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    content = eval(content.decode()[:-1])
    return content["access_token"]

def open_image(path):
    f=open(r'{0}'.format(path),'rb')
    pic = base64.b64encode(f.read())
    f.close()
    return str(pic,'utf-8')

def detect():
    access_token = get_token()
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    pic1 = open_image("my_image\\wyl.jpeg")
    # pic2 = open_image("3900510477\\page_2\\12.jpeg")
    params = {"image":pic1,"image_type":"BASE64"}
    data = parse.urlencode(params).encode('utf-8')
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=data)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        print(content)

def match():
    access_token = get_token()
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    pic1 = open_image("my_image\\wyl.jpeg")
    pic2 = open_image("3900510477\\page_2\\12.jpeg")
    params = json.dumps(
        [{"image": pic1, "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
         {"image": pic2, "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"}])
    request_url = request_url + "?access_token=" + access_token
    params = params.encode('utf-8')
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read()
    content = bytes.decode(content)
    content = eval(content)
    # 获得分数
    score = content['result']['score']
    if score > 80:
        return '照片相似度：' + str(score) + ',同一个人'
    else:
        return '照片相似度：' + str(score) + ',不是同一个人'

print(match())


# 离线版本
# client = AipFace(APP_ID, API_KEY, SECRET_KEY)
# result = client.match([
#     {
#         'image': str(base64.b64encode(open('my_image\\wyl.jpeg', 'rb').read()),'utf-8'),
#         'image_type': 'BASE64',
#     },
#     {
#         'image': str(base64.b64encode(open('3900510477\\page_2\\12.jpeg', 'rb').read()),'utf-8'),
#         'image_type': 'BASE64',
#     }
# ])
# print(result)