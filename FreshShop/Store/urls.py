from django.urls import path,re_path
from Store.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/', index),
    path('logout/',logout),
    # path('base/',base),
    path('register_store/',register_store),
    path('add_goods/',add_goods),
    re_path(r'list_goods/(?P<state>\w+)',list_goods),
    re_path(r'^goods/(?P<goods_id>\d+)',goods),
    re_path(r'update_goods/(?P<goods_id>\d+)',update_goods),
    re_path('set_goods/(?P<state>\w+)',set_goods),
]
