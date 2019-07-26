from django.shortcuts import render
from django.http import HttpResponseRedirect

from Buyer.models import *
from Store.views import set_password
from Store.models import *

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
    print(type_id)
    goods_type = GoodType.objects.filter(id = type_id).first() #从商品类型表查找出商品类型
    if goods_type:#判断商品类型是否为空
        goodsList = goods_type.goods_set.filter(goods_under = 1) #查询
    return render(request,'buyer/goods_list.html',locals())

def logout(request):
    response = HttpResponseRedirect('/buyer/index/')
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session['username']
    return response


