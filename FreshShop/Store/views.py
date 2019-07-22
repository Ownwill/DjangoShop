from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'store/index.html')

def cart(request):
    return render(request,'store/cart.html')

def detail(request):
    return render(request,'store/detail.html')

def list(request):
    return render(request,'store/list.html')

def login(request):
    return render(request,'store/login.html')

def place_order(request):
    return render(request,'store/place_order.html')

def register(request):
    return render(request,'store/register.html')

def user_center_info(request):
    return render(request,'store/user_center_info.html')

def user_center_order(request):
    return render(request,'store/user_center_order.html')

def user_center_site(request):
    return render(request,'store/user_center_site.html')





