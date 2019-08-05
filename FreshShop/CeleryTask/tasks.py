from __future__ import absolute_import
from FreshShop.celery import app

@app.task
def taskExample():
    print('send email ok!')

@app.task
def add(x=1,y=2):
    return x+y

import json
import requests
@app.task
def DingTask():
    #钉钉机器人的webhook地址
    url = 'https://oapi.dingtalk.com/robot/send?access_token=2d33d53383aaae6199e81d569c31d5d2f8e872b9e2d61c31a636ae31b8c108f4'
    headers = {
        'Content-Type': 'application/json',
        'Chartset': 'utf-8'
    }

    requests_data = {
        'msgtype': 'text',
        #发送的内容
        'text': {
            'content': '啤酒饮料矿泉水，花生瓜子八宝粥,没买的走了啊'
        },
        'at': {
            'atMobiles': [],
        },
        'isAtAll': True,
    }

    sendData = json.dumps(requests_data)
    response = requests.post(url, headers=headers, data=sendData)
    content = response.json()
    print(content)