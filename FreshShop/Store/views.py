import hashlib

from django.shortcuts import render
from django.http import HttpResponse
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
                    request.session['username'] = username
                    return response
    return response

@UserVaild
def index(request):
    return render(request,'store/index.html')

def page_404(request):
    return render(request,'store/404.html')

def base(request):
    return render(request,'store/base.html')

def blank(request):
    return render(request,'store/blank.html')

def buttons(request):
    return render(request,'store/buttons.html')

def cards(request):
    return render(request,'store/cards.html')

def charts(request):
    return render(request,'store/charts.html')

def forgotPwd(request):
    return render(request,'store/forgot-password.html')

def tables(request):
    return render(request,'store/tables.html')

def utiAni(request):
    return render(request,'store/utilities-animation.html')

def utiBor(request):
    return render(request,'store/utilities-border.html')

def utiCol(request):
    return render(request,'store/utilities-color.html')

def utiOth(request):
    return render(request,'store/utilities-other.html')












