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
    good_type_list = GoodType.objects.all()
    print(good_type_list)
    # goods = good_type_list.goods_set.all()
    # print(goods)
    return render(request,'buyer/index.html',locals())

def logout(request):
    response = HttpResponseRedirect('/buyer/index/')
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session['username']
    return response


