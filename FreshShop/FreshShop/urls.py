"""FreshShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from Buyer.views import index #从Buyer视图引入index

from rest_framework import routers
from Store.views import UserViewSet,TypeViewSet






router = routers.DefaultRouter()
router.register(r'goods',UserViewSet)
router.register(r'goodsType',TypeViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/',include('Store.urls')),
    path('buyer/',include('Buyer.urls')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    re_path('^API',include(router.urls)),  #restful接口的根路由，如输入127...8000/APIgoodsType/来访问
    re_path('^api-auth',include('rest_framework.urls')),
]
urlpatterns +=[
    re_path(r'^$',index), #其他路径就让他调到buyer的index页面
]
