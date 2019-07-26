from alipay import AliPay

alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqYWv+ilxLUZ0Ta+HnxiDa2oSbqVLSu0Tn256MBOv3lsSo0Ea4NM/VgCkWZT0nP38VoJYoRdBzJAFRFN+prCBJKNCwgT3KuzmYcg+41Ymv/WDatw4BNMEkL9fHG3fMAIN/jKhkQy1y/Mp4Rl3ZXX1V6AnM2VTJjSxrGu00Am83R2ljnL3KTSynFekOkqoVISN6UEmfnG2NuyCsbrzFotTogyr5bf+dt8jA+sDL4EiJ6y18pkGiSQKymoIkAY28UhZ3wuhoHemwiLoywk2VEloof8mn3WugeHriNyfy54sA5Tfrau/CAiJ2FGQhQtQznIAiIG+pQmzyQoNAK0PDr2B4wIDAQAB
-----END PUBLIC KEY-----'''

app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAqYWv+ilxLUZ0Ta+HnxiDa2oSbqVLSu0Tn256MBOv3lsSo0Ea4NM/VgCkWZT0nP38VoJYoRdBzJAFRFN+prCBJKNCwgT3KuzmYcg+41Ymv/WDatw4BNMEkL9fHG3fMAIN/jKhkQy1y/Mp4Rl3ZXX1V6AnM2VTJjSxrGu00Am83R2ljnL3KTSynFekOkqoVISN6UEmfnG2NuyCsbrzFotTogyr5bf+dt8jA+sDL4EiJ6y18pkGiSQKymoIkAY28UhZ3wuhoHemwiLoywk2VEloof8mn3WugeHriNyfy54sA5Tfrau/CAiJ2FGQhQtQznIAiIG+pQmzyQoNAK0PDr2B4wIDAQABAoIBAE7JhmdS+XncY9NzQCoOH449p0Fra1nwY41WsE1F6RgD5d6gNJjHNYmIFNpZo3KPjMa8H+sGvxsO2JPP5m4cXHkls7Iu0p1NqylJAwlvkeTne2Of5B1B4b5QYyj4W6GZYt2AtJyQdrHKWu12g4pRT2yhT3bQoduA5A7JpCiIThHJoqYc2xT4ZBkS/WgsdJyt5Ew/kt19FFjZh9D1yQKrJOi+og55TJO11b9E0q7uIjHbkYsQnIpruNhi1y5RUYMNuA4e5XJLWCUn38Fwjq2Gnp1tJGSEbXeMJfW1Hb6hTkX6ohvoet65KwIKaKC0RcdLFIwtxXeFNXiKBG3SHdHtNtECgYEA3EGPddQmGBTuGxWOmeCE3GMP9qctV/WvKw1/TrjJQcdAa89OaYHwzRiv15FmxXMhNHALfV5T0W3dFhWvf60jhYORCfv34nbiOaMeoGmTFveXV5ecxgysLST3hIHk2saKY0qFljhMXw/Tg8oZ3HIbh5Iday5r6Nu3DC5TJ46aeZkCgYEAxQhpORYpD6lzYcyt5XH8X6+g6yX+pvknNylXmtknuofFcbVPOWMUf2mGPe8ACZUa1B1miGB+A9slOlhyVdXWjiU+VYEKjxidK7QBAitRIhYFl6m/1BOZuwvc8RkrVjyjaM7gRp8SPglj6ezeQQleC+ilwGLmzgOCNoEOUs/Y3NsCgYEAt9od1xwkRDvMWV1QMFACdzhVje0UY3TYKBbXKq4CiN66foOID3gAuiKePVHIuI6Wq//PB3IigxGy14l4ehnbKcqd2fiyfR4BTl1D5mDZ//TiJqKOoZ7YZcKSvc/zaU8LG0CMa81Iqp06UKr1lVbGdg7YcaxJNRGaJRfSH5XgihkCgYATmVWWJx0ogKuIg+qcUy1Oe1LfcSUWiNwcwZEERyuLg2vhdq6Nv8xPLDj9OiPf0CQeC1qioC6Ixai7WAbvgNjZxNyhdreNKl6f9UTQaWylnlkqD+mT9+snzvNITD+iUV/T0hg/Dh2rbBWzNCubfooLVzX9oBjjTzgJoebB2AjzVwKBgQCKueCfcH5M5uGc1S8J0Fvht/iWXOaLVuxkRG4pbWZgMmQLYbYEhHBr1ijhT8eQpcbFKw+a5qYATT3SrUypmFL+LFpN3W1s+5tjiEUkVA3unxue2sGCuVsI/AqLpzbE96+lo+EToA/Y49jTKSV8IPX6dv7FvLCYT5cx0NVStDPLmw==
-----END RSA PRIVATE KEY-----'''


#实例化支付应用
alipay = AliPay(
    appid = '2016100100637810', #
    app_notify_url = None,
    app_private_key_string= app_private_key_string,
    alipay_public_key_string = alipay_public_key_string,
    sign_type = 'RSA2',
)

#发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no = "12",#订单号
    total_amount=str(1000.01), #支付金额
    subject = '生鲜交易', #交易主体
    return_url=None,
    notify_url=None,
) #生成url后面的参数
print('https://openapi.alipaydev.com/gateway.do?'+order_string) #跳转的支付页面url：'https://openapi.alipaydev.com/gateway.do?'+order_string。