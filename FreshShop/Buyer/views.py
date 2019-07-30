import time

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse


from Buyer.models import *
from Store.views import set_password
from Store.models import *

from alipay import AliPay


def UserVaild(func): #设置装饰器，进行校验cookie和session
    def inner(request,*args,**kwargs):
        u_cookies = request.COOKIES.get('username')
        u_session = request.session.get('username')
        if u_cookies and u_session and u_cookies == u_session:
            return func(request,*args,**kwargs)
        return HttpResponseRedirect('/buyer/login/')
        # return render(request,'buyer/index.html')
    return inner

def base(request):
    return render(request,'buyer/base.html',locals())

def register(request):
    if request.method == "POST":
        #
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        buyer = Buyer()
        buyer.username = username
        buyer.password = set_password(password)
        buyer.email = email
        buyer.save()
        return HttpResponseRedirect('/buyer/login/')
    return render(request,'buyer/register.html',locals())

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if username and password:
            user = Buyer.objects.filter(username=username).first()
            if user:
                if set_password(password) == user.password:
                    response = HttpResponseRedirect('/buyer/index/')
                    #登录校验
                    response.set_cookie('username',user.username)
                    request.session['username'] = user.username
                    #方便其他查询
                    response.set_cookie('user_id',user.id)
                    return response
    return render(request,'buyer/login.html')

@UserVaild
def index(request):
    """
    前台首页
    :param request:
    :return:
    """
    result_list = []
    goods_type_list = GoodType.objects.all()
    print(goods_type_list)
    for goods_type in goods_type_list:
        goods_list = goods_type.goods_set.values()[:4]
        if goods_list:
            goods_type = {
                'id':goods_type.id,#配置商品id，在点击更多的时候使用类型id，跳转到更多页面
                'name':goods_type.name,
                'description':goods_type.description,
                'picture':goods_type.picture,
                'goods_list':goods_list,
            }
            result_list.append(goods_type)

    return render(request,'buyer/index.html',locals())

#点击更多之后，跳转到的更多商品页
def goods_list(request):
    """
    前台列表页
    :param reuqest:
    :return:
    """
    goodsList = []
    type_id = request.GET.get('type_id') #获取index页面传来的商品类型
    page_num = int(request.GET.get('page_num',1)) #获取前端传来的页码
    goods_type = GoodType.objects.filter(id = type_id).first() #从商品类型表查找出商品类型

    if goods_type:#判断商品类型是否为空
        goodsList = goods_type.goods_set.filter(goods_under = 1) #查询
    paginator = Paginator(goodsList,4)
    page = paginator.page(page_num)
    page_range = paginator.page_range
    # print(page_range)
    return render(request,'buyer/goods_list.html',locals())

#商品详情页
def detail(request):
    goods_id = request.GET.get('id')
    if goods_id:
        goods = Goods.objects.filter(id = int(goods_id)).first()
        if goods:
            goods_name =  goods.goods_name
            goods_price = goods.goods_price
            goods_number = goods.goods_number
            goods_description = goods.goods_description
            goods_image = goods.goods_image
            goods_count = 0 #前台显示的商品数量
            return render(request,'buyer/detail.html',locals())
    return HttpResponse('没有您查找的商品')

def setOrder_id(user_id,goods_id,store_id):
    """
    设置商品订单编号
    时间+用户id+商品id+店铺id
    :return:
    """
    strtime = time.strftime('%Y%m%d%H%M%S',time.localtime())
    return strtime+user_id+goods_id+store_id

def place_order(request):

    #获取detail页面通过form表单传来的数据
    if request.method == "POST":
        count = int(request.POST.get('count'))    #获取到用户选择购买商品的数量
        goods_id = request.POST.get('goods_id')   #获取到用户购买商品的id
        user_id = int(request.COOKIES.get('user_id'))  #获取到用户的id
        goods = Goods.objects.get(id=goods_id)         #查找到goods表对应的商品
        store_id = goods.store_id.id        #查找到商品对应的商店，商品和商店是多对一关系

        #保存订单表
        order = Order()
        order.order_id = setOrder_id(str(user_id),str(goods_id),str(store_id)) #订单号
        order.goods_count = count                                              #订单数量
        order.order_user = Buyer.objects.get(id=user_id)                       #订单用户
        order.order_price = count*goods.goods_price                            #订货总价
        order.order_status = 1
        order.save()

        #保存订单详情表
        order_detail = OrderDetail()
        order_detail.order_id = order                      #对应的订单表，订单详情表和订单表是一对多关系
        order_detail.goods_id = goods_id                   #商品id
        order_detail.goods_name = goods.goods_name         #商品名称
        order_detail.goods_price = goods.goods_price       #商品价格
        order_detail.goods_number = count                  #商品数量
        order_detail.goods_total = count*goods.goods_price #商品总价
        order_detail.goods_store = store_id                #对应店铺的id
        order_detail.goods_image = goods.goods_image       #商品图片
        order_detail.save()

        detail = [order_detail]                            #把商品详情保存在列表里
        return render(request,'buyer/place_order.html',locals())
    else:
        return HttpResponse('非法请求')

#增加减少商品数量
# def goods_num_ajax(request):
#     result = {'status':'error'}  #ajax返回的结果
#
#     goods_count = int(request.GET.get('goods_count'))
#     goods_id = request.GET.get('id')
#     meth = request.GET.get('meth')
#     goods = Goods.objects.filter(id=goods_id).first()  # 查询出对应的商品
#     #点击添加的时候的方法
#     if meth == 'add':
#         # 如果数据库中商品数量大于0，前端显示的数量加一，数据库中的数据减一
#         if goods.goods_number>0:#如果数据库中的商品大于0则可以往下减
#             goods_count = goods_count + 1  # 前端显示的数量
#             goods.goods_number = int(goods.goods_number)-1  #数据库中的商品减一
#             # ajax返回的数据
#             result['status'] = 'success'
#             result['goods_count'] = goods_count
#             result['total_money'] = goods_count*int(goods.goods_price)
#             goods.save()
#             return JsonResponse(result)
#         # 如果数据库中商品数量不大于0，前端显示的数量为0，数据库中的数据不减
#         else:
#             result['status'] = 'success'
#             result['goods_count'] = goods_count
#             return JsonResponse(result)
#
#     #点击减少时的操作
#     if meth == 'sub':
#         # 如果前端商品数量大于0，前端显示的数量减一，数据库中的数据加一
#         if goods_count>0:#如果数据库中的商品大于0则可以往下减
#             goods_count = goods_count - 1  # 前端显示的数量
#             goods.goods_number = int(goods.goods_number)+1  #数据库中的商品减一
#             # ajax返回的数据
#             result['status'] = 'success'
#             result['goods_count'] = goods_count
#             result['total_money'] = goods_count*int(goods.goods_price)
#
#             print('$' * 50, result)
#             goods.save()
#             return JsonResponse(result)
#         # 如果前端商品数量不大于0，前端显示的数量为0，数据库中的数据不变
#         else:
#             result['status'] = 'success'
#             result['goods_count'] = 0
#             print('@' * 50, result)
#             return JsonResponse(result)
#
#
#     return HttpResponse()
#


#加入购物车
def add_cart(request):
    goods_id = int(request.GET.get('id')) #获取商品的id
    goods_num = request.GET.get('goods_num')
    print(goods_num)
    goods = Goods.objects.filter(id=goods_id).first()
    cart = Cart()
    cart.goods_id = goods.id
    cart.goods_name = goods.goods_name
    cart.goods_price = goods.goods_price
    cart.goods_picture = goods.goods_image
    cart.goods_num = goods_num
    print(goods)
    return  HttpResponse('nice')

#用户退出登录
def logout(request):
    response = HttpResponseRedirect('/buyer/index/')
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session['username']
    return response

#支付结果
def pay_result(request):
    """
    支付宝支付成功自动用get请求返回的参数
    #编码
    charset=utf-8
    #订单号
    out_trade_no=10002
    #订单类型
    method=alipay.trade.page.pay.return
    #订单金额
    total_amount=1000.00
    #校验值
    sign=enBOqQsaL641Ssf%2FcIpVMycJTiDaKdE8bx8tH6shBDagaNxNfKvv5iD737ElbRICu1Ox9OuwjR5J92k0x8Xr3mSFYVJG1DiQk3DBOlzIbRG1jpVbAEavrgePBJ2UfQuIlyvAY1fu%2FmdKnCaPtqJLsCFQOWGbPcPRuez4FW0lavIN3UEoNGhL%2BHsBGH5mGFBY7DYllS2kOO5FQvE3XjkD26z1pzWoeZIbz6ZgLtyjz3HRszo%2BQFQmHMX%2BM4EWmyfQD1ZFtZVdDEXhT%2Fy63OZN0%2FoZtYHIpSUF2W0FUi7qDrzfM3y%2B%2BpunFIlNvl49eVjwsiqKF51GJBhMWVXPymjM%2Fg%3D%3D&trade_no=2019072622001422161000050134&auth_app_id=2016093000628355&version=1.0&app_id=2016093000628355
    #订单号
    trade_no=2019072622001422161000050134
    #用户的应用id
    auth_app_id=2016093000628355
    #版本
    version=1.0
    #商家的应用id
    app_id=2016093000628355
    #加密方式
    sign_type=RSA2
    #商家id
    seller_id=2088102177891440
    #时间
    timestamp=2019-07-26
    """
    return render(request,'buyer/pay_result.html',locals())
    # return HttpResponse('你好')

#支付宝支付
def order_pay(request):
    money = request.GET.get('money')
    order_id = request.GET.get('order_id')

    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqYWv+ilxLUZ0Ta+HnxiDa2oSbqVLSu0Tn256MBOv3lsSo0Ea4NM/VgCkWZT0nP38VoJYoRdBzJAFRFN+prCBJKNCwgT3KuzmYcg+41Ymv/WDatw4BNMEkL9fHG3fMAIN/jKhkQy1y/Mp4Rl3ZXX1V6AnM2VTJjSxrGu00Am83R2ljnL3KTSynFekOkqoVISN6UEmfnG2NuyCsbrzFotTogyr5bf+dt8jA+sDL4EiJ6y18pkGiSQKymoIkAY28UhZ3wuhoHemwiLoywk2VEloof8mn3WugeHriNyfy54sA5Tfrau/CAiJ2FGQhQtQznIAiIG+pQmzyQoNAK0PDr2B4wIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEAqYWv+ilxLUZ0Ta+HnxiDa2oSbqVLSu0Tn256MBOv3lsSo0Ea4NM/VgCkWZT0nP38VoJYoRdBzJAFRFN+prCBJKNCwgT3KuzmYcg+41Ymv/WDatw4BNMEkL9fHG3fMAIN/jKhkQy1y/Mp4Rl3ZXX1V6AnM2VTJjSxrGu00Am83R2ljnL3KTSynFekOkqoVISN6UEmfnG2NuyCsbrzFotTogyr5bf+dt8jA+sDL4EiJ6y18pkGiSQKymoIkAY28UhZ3wuhoHemwiLoywk2VEloof8mn3WugeHriNyfy54sA5Tfrau/CAiJ2FGQhQtQznIAiIG+pQmzyQoNAK0PDr2B4wIDAQABAoIBAE7JhmdS+XncY9NzQCoOH449p0Fra1nwY41WsE1F6RgD5d6gNJjHNYmIFNpZo3KPjMa8H+sGvxsO2JPP5m4cXHkls7Iu0p1NqylJAwlvkeTne2Of5B1B4b5QYyj4W6GZYt2AtJyQdrHKWu12g4pRT2yhT3bQoduA5A7JpCiIThHJoqYc2xT4ZBkS/WgsdJyt5Ew/kt19FFjZh9D1yQKrJOi+og55TJO11b9E0q7uIjHbkYsQnIpruNhi1y5RUYMNuA4e5XJLWCUn38Fwjq2Gnp1tJGSEbXeMJfW1Hb6hTkX6ohvoet65KwIKaKC0RcdLFIwtxXeFNXiKBG3SHdHtNtECgYEA3EGPddQmGBTuGxWOmeCE3GMP9qctV/WvKw1/TrjJQcdAa89OaYHwzRiv15FmxXMhNHALfV5T0W3dFhWvf60jhYORCfv34nbiOaMeoGmTFveXV5ecxgysLST3hIHk2saKY0qFljhMXw/Tg8oZ3HIbh5Iday5r6Nu3DC5TJ46aeZkCgYEAxQhpORYpD6lzYcyt5XH8X6+g6yX+pvknNylXmtknuofFcbVPOWMUf2mGPe8ACZUa1B1miGB+A9slOlhyVdXWjiU+VYEKjxidK7QBAitRIhYFl6m/1BOZuwvc8RkrVjyjaM7gRp8SPglj6ezeQQleC+ilwGLmzgOCNoEOUs/Y3NsCgYEAt9od1xwkRDvMWV1QMFACdzhVje0UY3TYKBbXKq4CiN66foOID3gAuiKePVHIuI6Wq//PB3IigxGy14l4ehnbKcqd2fiyfR4BTl1D5mDZ//TiJqKOoZ7YZcKSvc/zaU8LG0CMa81Iqp06UKr1lVbGdg7YcaxJNRGaJRfSH5XgihkCgYATmVWWJx0ogKuIg+qcUy1Oe1LfcSUWiNwcwZEERyuLg2vhdq6Nv8xPLDj9OiPf0CQeC1qioC6Ixai7WAbvgNjZxNyhdreNKl6f9UTQaWylnlkqD+mT9+snzvNITD+iUV/T0hg/Dh2rbBWzNCubfooLVzX9oBjjTzgJoebB2AjzVwKBgQCKueCfcH5M5uGc1S8J0Fvht/iWXOaLVuxkRG4pbWZgMmQLYbYEhHBr1ijhT8eQpcbFKw+a5qYATT3SrUypmFL+LFpN3W1s+5tjiEUkVA3unxue2sGCuVsI/AqLpzbE96+lo+EToA/Y49jTKSV8IPX6dv7FvLCYT5cx0NVStDPLmw==
    -----END RSA PRIVATE KEY-----'''

    # 实例化支付应用
    alipay = AliPay(
        appid='2016100100637810',  #
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type='RSA2',
    )

    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject='生鲜交易',  # 交易主体
        return_url='http://127.0.0.1:8000/buyer/pay_result/',    #支付成功后跳转的本地路由，
        notify_url='http://127.0.0.1:8000/buyer/pay_result/',    #支付成功后跳转的异步路由，可以用ajax来完善
    )  # 生成url后面的参数
    # print('https://openapi.alipaydev.com/gateway.do?' + order_string)  # 跳转的支付页面url：'https://openapi.alipaydev.com/gateway.do?'+order_string。

    order = Order.objects.get(order_id=order_id)
    order.order_status = 2
    order.save()   #保存商品订单

    return HttpResponseRedirect('https://openapi.alipaydev.com/gateway.do?' + order_string)

def userCenter_base(request):
    return render(request,'buyer/userCenter_base.html')

def user_center_info(request):
    return render(request,'buyer/user_center_info.html')

#加入购物车
def addcart(request):
    result = {'state':'error','data':''} #设置返回给前台ajax的状态和数据
    if request.method == 'POST': #判断请求方式
        count = int(request.POST.get('count'))       #获取前台ajax传的商品数量
        goods_id = request.POST.get('goods_id')      #获取前台ajax传来的商品id

        goods = Goods.objects.get(id = int(goods_id))#获取商品表中的对应商品的信息
        print('%' * 50, count)
        user_id = request.COOKIES.get('user_id')     #获取cookies中的用户id

        #保存到购物车
        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_price = goods.goods_price
        cart.goods_total = goods.goods_price*count
        cart.goods_number = count
        cart.goods_picture = goods.goods_image
        cart.goods_id = goods.id
        cart.goods_store = goods.store_id.id
        cart.user_id = user_id
        cart.save()

        #修改状态和数据
        result['state'] = 'success'
        result['data'] = '商品添加成功'
    else:
        result['data'] = '请求错误'
    return JsonResponse(result)
#购物车
def cart(request):
    #获取用户id并返回用户对应的购物车中的商品
    user_id = request.COOKIES.get('user_id')
    goods_list = Cart.objects.filter(user_id=user_id)
    return render(request,'buyer/cart.html',locals())