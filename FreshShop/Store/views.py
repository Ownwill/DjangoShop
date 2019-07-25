import hashlib

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator #引入分页
from django.http import HttpResponseRedirect

from Store.models import *
# Create your views here.

#对密码进行MD5加密

def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

def UserVaild(func): #设置装饰器，进行校验cookie和session
    def inner(request,*args,**kwargs):
        u_cookies = request.COOKIES.get('username')
        u_session = request.session.get('username')
        if u_cookies and u_session and u_cookies == u_session:
            user = Seller.objects.filter(username=u_cookies).first()
            if user:
                return func(request,*args,**kwargs)
    return inner

def register(request):
    """
    返回注册页面，进行注册数据保存
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = Seller()
            user.username = username
            user.password = set_password(password)
            user.save()

            return HttpResponseRedirect('/store/login/')
    return render(request,'store/register.html')

def login(request):
    """
    登录成功跳转到index页面，未登录成功跳转到登录页
    :param request:
    :return:
    """
    response = render(request,'store/login.html')
    response.set_cookie("login_from","login_page")  #设置cookies说明来源，
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        if username and password: #前台是否传来账号密码
            user = Seller.objects.filter(username=username).first()
            if user: #判断用户是否存在于数据库
                web_password = set_password(password)
                print(web_password)
                cookies = request.COOKIES.get('login_from')
                if user.password == web_password and cookies == "login_page": #判断密码是否正确和来源
                    response = HttpResponseRedirect('/store/index/')
                    response.set_cookie('username',username)
                    response.set_cookie('user_id',user.id) #设施id从前台判断，有的话展示，没有的话显示注册
                    request.session['username'] = username
                    #检验是否有店铺
                    store = Store.objects.filter(user_id=user.id).first()
                    if store:
                        response.set_cookie('has_store',store.id)
                    else:
                        response.set_cookie('has_store','')
                    return response
    return response

@UserVaild
def index(request):
    # user_id = request.COOKIES.get('user_id')
    # if user_id:
    #     user_id = int(user_id)
    # else:
    #     user_id = 0
    # store = Store.objects.filter(user_id=user_id).first()
    # if store:
    #     is_store = 1
    # else:
    #     is_store = 0
    # return render(request,'store/index.html',{'is_store':is_store,'user_id':user_id})
    return render(request,'store/index.html',locals())


#退出
def logout(request):
    response = HttpResponseRedirect('/store/login/')
    for key in request.COOKIES: #获取当前浏览器的所有cookie
        response.delete_cookie(key)        #下发删除cookie的请求，删除浏览器端的所有cookie
    # response.delete_cookie('username')
    return response

def base(request):
    return render(request,'store/base.html')


def register_store(request):
    type_list = StoreType.objects.all()
    user_id = request.COOKIES.get('user_id')
    print(user_id)
    if request.method == "POST":
        post_data = request.POST
        store_name = post_data.get('store_name')
        store_descripton = post_data.get('store_descripton')
        store_phone = post_data.get('store_phone')
        store_money = post_data.get('store_money')
        store_address =  post_data.get('store_address')

        type_lists = post_data.getlist('type') #获取到所有类型,getlist
        store_logo = request.FILES.get('store_logo')  #获取图片request.FILES.get('store_logo')

        #保存数据
        store = Store()
        store.store_name = store_name
        store.store_descripton = store_descripton
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo
        store.save()

        for i in type_lists:
            store_type = StoreType.objects.get(id = i)
            store.type.add(store_type)
        store.save()
        response = HttpResponseRedirect('/store/index/')
        response.set_cookie('has_store',store.id)
        return response
    return render(request,'store/register_store.html',locals())

#添加商品
def add_goods(request):
    goods_type = GoodType.objects.all()
    if request.method == "POST":
        #获取数据
        goods_name = request.POST.get('goods_name')
        goods_price = request.POST.get('goods_price')
        goods_number = request.POST.get('goods_number')
        goods_description = request.POST.get('goods_description')
        goods_date = request.POST.get('goods_date')
        goods_safeDate = request.POST.get('goods_safeDate')
        goods_store = request.POST.get('goods_store')
        goods_image = request.FILES.get('goods_image')
        goods_type_id = request.POST.get('type') #获取到所有类型,getlist
        #开始保存数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.goods_type = GoodType.objects.get(id= goods_type_id) #一对多的保存方法
        goods.save()


        #因为是多对多关系所以需要再保存一次
        goods.store_id.add(
            Store.objects.get(id = int(goods_store))
        )
        goods.save()
        return HttpResponseRedirect('/store/list_goods/up/')
    return render(request,'store/add_goods.html',locals())

#商品列表
def list_goods(request,state):
    """
    base页中添加/store/list_goods/up/，或/store/list_goods/down/的href来请求url，
    url截取请求，截取出state，判断是请求上架列表（up）,还是下架列表（down）,然后根据请求
    把数据返回页面。如果是请求上架页，把1赋给状态state_num，如果是请求下架页，把0赋给状态state_num。
    good_under字段表示上下架，把state_num参数赋给字段来执行查询，查询上架的商品，或者下架的商品。
    :param request:
    :param state:
    :return:
    """
    #如果是请求
    if state == 'up':
        state_num = 1
    else:
        state_num = 0

    #获取两个关键字，一个决定查询内容，一个决定查询页数
    keywords = request.GET.get('keywords','')
    page_num = request.GET.get('page_num',1) #获取前台传来的页数，没有的话就默认是第一页

    #获取店铺id，获取店铺
    store_id = request.COOKIES.get('has_store')
    store = Store.objects.get(id=int(store_id))

    if keywords:
        #获取店铺对应的全部商品,反向查询
        goods_list = store.goods_set.filter(goods_name__contains=keywords,good_under=state_num)#模糊查询，字段__contains=关键字
    else:
        print(keywords)
        goods_list = store.goods_set.filter(goods_under=state_num)
    paginator = Paginator(goods_list,3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request,'store/goods_list.html',locals())

#商品详情页
def goods(request,goods_id):
    goods_data = Goods.objects.filter(id = goods_id).first()
    return render(request,'store/goods.html',locals())

#修改商品
def update_goods(request,goods_id):
    goods_data = Goods.objects.filter(id = goods_id).first()
    if request.method == "POST":
        goods_name = request.POST.get('goods_name')
        goods_price = request.POST.get('goods_price')
        goods_number = request.POST.get('goods_number')
        goods_description = request.POST.get('goods_description')
        goods_date = request.POST.get('goods_date')
        goods_safeDate = request.POST.get('goods_safeDate')
        goods_image = request.FILES.get('goods_image')


        goods = Goods.objects.get(id=goods_id)
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_image:
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect('/store/goods/%s/'%goods_id)


    return render(request,'store/update_goods.html',locals())

#商品下架
# def under_goods(request):
#     """
#     获取商品id，是为了对商品修改
#     获取referer来源是为了修改完成之后重定向到来源页
#     :param request:
#     :return:
#     """
#     id = request.GET.get('id') #获取前台href中传来的get，获取get中携带的商品id
#     referer = request.META.get('HTTP_REFERER') #获取商品来源的网页，删除完成后再重定向到来源页
#     if id: #判断是否获取到商品id
#         goods = Goods.objects.filter(id=id).first() #获取商品
#         goods.goods_under = 0  #修改商品上架状态1 为下架状态0
#         goods.save()           #保存商品数据
#     return HttpResponseRedirect(referer)  #重定向到来源页

def set_goods(request,state):
    if state == "down":
        state_num = 0
    else:
        state_num = 1

    id = request.GET.get('id')
    referer = request.META.get('HTTP_REFERER')
    if id:
        goods = Goods.objects.filter(id=id).first()
        if state == 'delete':
            goods.delete()
        else:
            goods.goods_under = state_num
            goods.save()
    return HttpResponseRedirect(referer)

#商品类型
def goods_type(request):
    goods_type_list = GoodType.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        picture = request.POST.get('picture')
        goods_type = GoodType()
        goods_type.name = name
        goods_type.description = description
        goods_type.picture = picture
        goods_type.save()
        return HttpResponseRedirect('/store/goods_type/')
    return render(request,'store/goods_type.html',locals())

#删除商品类型
def delete_goods_type(request):
    goods_id = request.GET.get('id')
    GoodType.objects.filter(id=goods_id).delete()
    return HttpResponseRedirect('/store/goods_type/')

#修改商品类型
def update_good_type(request):
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        picture = request.POST.get('picture')

        #修改商品
        goods_type = GoodType.objects.get(id = id)
        goods_type.name = name
        goods_type.description = description
        goods_type.picture = picture
        goods_type.save()
    return HttpResponseRedirect('/store/goods_type/')

#指定类型商品的显示
def show_type_goods(request):

    return







#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#密码加密
# def set_password(password):
#     md5 = hashlib.md5()
#     md5.update(password.encode())
#     result = md5.hexdigest()
#     return result
#
# def register(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         if username and password:
#             user = Seller()
#             user.username = username
#             user.password = set_password(password)
#             user.nickname = username
#             user.save()
#             return HttpResponseRedirect('/store/login/')
#     return render(request,'store/register.html')
#
# def login(request):
#     response = render(request,'store/login.html')
#     response.set_cookie('login_form',"login_page")
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         if username and password:
#             user = Seller.objects.filter(username=username).first()
#             if user:
#                 web_password = set_password(password)
#                 cookies = request.COOKIES.get('login_form')
#                 if web_password == user.password and cookies == "login_page":
#                     response = HttpResponseRedirect('/store/index/')
#                     response.set_cookie('username',username)
#                     response.set_cookie('user_id',user.id)
#                     request.session['username'] = username
#                     return response
#     return response
#
# #登录校验的装饰器
# def loginVaild(func):
#     def inner(request,*args,**kwargs):
#         c_username = request.COOKIES.get('username')
#         s_username = request.session['username']
#         if c_username and s_username and c_username==s_username:
#             user = Seller.objects.filter(username=c_username).first()
#             if user:
#                 return func(request,*args,**kwargs)
#         return HttpResponseRedirect('/store/login/')
#
#     return inner
#
# @loginVaild
# def index(request):
#     """
#     登录主页面
#     :param request:
#     :return:
#     """
#     user_id = request.COOKIES.get('user_id')
#     user_id = int(user_id)
#     if not user_id:
#         user_id = 0
#     store = Store.objects.filter(user_id=user_id).first()
#     if store:
#        is_store = 1
#     else:
#         is_store = 0
#
#     return render(request,'store/index.html',{'user_id':user_id,'is_store':is_store})
#
# #退出登录
# def logout(request):
#     response = HttpResponseRedirect('/store/login/')
#     response.delete_cookie('username')
#     del request.session['username']
#     return response
#
# def register_store(request):
#     type_list = StoreType.objects.all()
#     user_id = request.COOKIES.get('user_id')
#     if request.method == "POST":
#         post_data = request.POST
#         store_name = post_data.get('store_name')
#         store_descripton = post_data.get('store_descripton')
#         store_phone = post_data.get('store_phone')
#         store_money = post_data.get('store_money')
#         store_address =  post_data.get('store_address')
#
#         type_lists = post_data.getlist('type')
#         store_logo = post_data.FILES.get('store_logo')
#
#         store = Store()
#         store.store_name = store_name
#         store.store_descripton = store_descripton
#         store.store_phone = store_phone
#         store.store_money = store_money
#         store.store_address = store_address
#         store.store_logo = store_logo
#         store.user_id = user_id
#         store.save()
#
#         for i in type_list:
#             store_type = StoreType.objects.get(id = i)
#             store.type.add(store_type)
#         store.save()
#
#         response = HttpResponseRedirect('/store/index/')
#         response.set_cookie('has_store',store.id)
#         return response
#     return render(request,'store/register_store.html',locals())
#
# #添加商品
# def add_goods(request):
#     if request.method == "POST":
#         goods = request.POST
#         goods_name = goods.get('goods_name')
#         goods_price = goods.get('goods_price')
#         goods_number = goods.get('goods_number')
#         goods_description = goods.get('goods_description')
#         goods_date = goods.get('goods_date')
#         goods_safeDate = goods.get('goods_safeDate')
#         goods_store = goods.get('goods_store')
#         goods_image = goods.get('goods_image')
#
#         #保存数据
#         goods = Goods()
#         goods.goods_name = goods_name
#         goods.goods_price = goods_price
#         goods.goods_number = goods_number
#         goods.goods_description = goods_description
#         goods.goods_date = goods_date
#         goods.goods_safeDate =goods_safeDate
#         goods.goods_store = goods_store
#         goods.goods_image = goods_image
#         goods.save()
#
#         #关联到用户
#         goods.store_id.add(
#             Store.objects.get(user_id=goods_store)
#         )
#         goods.save()
#         return HttpResponseRedirect('/store/list_goods/')
#     return render(request,'store/add_goods.html',locals())
#
# def list_goods(request):
#     page = Goods.objects.all()
#     keyword = request.GET.get('keywords','')
#
#     store = Store.objects.get('has_store')
#     if keyword:
#         goods_list = store.goods_set.filter()
#     p = request.GET.get('page_num',1)
#     paginator = Paginator(page,3)
#     page = paginator.page(int(p))
#     page_range = paginator.page_range
#
#     return render(request,'store/goods_list.html',locals())















