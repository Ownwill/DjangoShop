import requests

#接口地址
url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'  #互亿无线的地址
account = 'C13473179'                   #填写APIID
password = 'xxxxxxxxxxxxxxxxxxxxxxxxx'  #填写APIKEY
mobile = '1xxxxxxxxxxx'                 #填写接收人的手机号
content = '您的验证码是：201981。请不要把验证码泄露给其他人。'  #只能更改数字

#定义请求的头部
headers = {
    "Content-type":'application/x-www-form-urlencoded', #发送的数据格式
    'Accept':'text/plain'  #接收数据的文本格式
}
#定义请求的数据
data = {
    'account':account,
    "password": password,
    "mobile": mobile,
    "content": content,
}

#发送数据
response = requests.post(url,headers=headers,data=data)
print(response)