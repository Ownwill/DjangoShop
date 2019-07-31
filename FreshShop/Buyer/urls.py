from django.urls import path,re_path
from Buyer.views import *


urlpatterns = [
    path('login/',login),
    path('logout/', logout),
    path('register/', register),
    path('index/', index),
    path('goods_list/',goods_list),
    path('detail/',detail),
    # path('goods_num_ajax/',goods_num_ajax ),
    # path('add_cart/',add_cart),
    path('place_order/',place_order),
    path('user_center_info/',user_center_info),
    path('cart/',cart),
    path('addcart/',addcart),
]

urlpatterns +=[
    path('base/',base),
    path('order_pay/',order_pay),
    path('pay_result/',pay_result),
    path('userCenter_base/',userCenter_base),
]
