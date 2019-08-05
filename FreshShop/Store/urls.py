from django.urls import path,re_path
from Store.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/', index),
    path('logout/',logout),
    # path('base/',base),
    path('register_store/',register_store),
    path('goods_type/', goods_type),
    path('add_goods/',add_goods),
    path('delete_goods_type/',delete_goods_type),
    path('update_good_type/',update_good_type),
    path('pending_list/',pending_list),
    path('order_confirm/',order_confirm),
    path('solved_list/',solved_list),
    path('order_refuse/',order_refuse),
    re_path(r'list_goods/(?P<state>\w+)',list_goods),
    re_path(r'^goods/(?P<goods_id>\d+)',goods),
    re_path(r'update_goods/(?P<goods_id>\d+)',update_goods),
    re_path('set_goods/(?P<state>\w+)',set_goods),
]

from django.views.decorators.cache import cache_page

urlpatterns += [
    path('agl/',ajl),
    path('get_add/',get_add),
    path('lw/',littlewrite),
    path(r'lw1/',cache_page(10*60)(littlewrite)),
    #cache_page(10*60)(littlewrite),10*60为缓存时间，littlewrite为路由对应的视图
]