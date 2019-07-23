import hashlib

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator #引入分页
from django.http import HttpResponseRedirect

from Store.models import *
# Create your views here.

def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

def UserVaild(func):
    def inner(request,*args,**kwargs):
        u_cookies = request.COOKIES.get('username')
        u_session = request.session.get('username')
        if u_cookies and u_session and u_cookies == u_session:
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
                    return response
    return response

@UserVaild
def index(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        user_id = int(user_id)
    else:
        user_id = 0
    store = Store.objects.filter(user_id=user_id).first()
    if store:
        is_store = 1
    else:
        is_store = 0
    return render(request,'store/index.html',{'is_store':is_store,'user_id':user_id})

#退出
def logout(request):
    response = HttpResponseRedirect('/store/login/')
    response.delete_cookie('username')
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
    return render(request,'store/register_store.html',locals())

#添加商品
def add_goods(request):
    if request.method == "POST":
        #获取数据
        goods_name = request.POST.get('goods_name')
        goods_price = request.POST.get('goods_price')
        goods_number = request.POST.get('goods_number')
        goods_description = request.POST.get('goods_description')
        goods_date = request.POST.get('goods_date')
        goods_safeDate = request.POST.get('goods_safeDate')
        goods_store = request.POST.get('goods_store')
        goods_image = request.POST.get('goods_image')

        #开始保存数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.save()

        #因为是多对多关系所以需要再保存一次
        goods.store_id.add(
            Store.objects.get(id = int(goods_store))
        )
        goods.save()
        return HttpResponseRedirect('/store/list_goods/')
    return render(request,'store/add_goods.html')

def list_goods(request):
    #获取两个关键字
    keywords = request.GET.get('keywords','')
    page_num = request.GET.get('page_num',1) #获取前台传来的页数，没有的话就默认是第一页
    if keywords:
        goods_list = Goods.objects.filter(goods_name__contains=keywords) #模糊查询，字段__contains=关键字
    else:
        goods_list = Goods.objects.all()
    paginator = Paginator(goods_list,3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request,'store/goods_list.html',locals())













