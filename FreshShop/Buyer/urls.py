from django.urls import path,re_path
from Buyer.views import *


urlpatterns = [
    path('login/',login),
    path('logout/', logout),
    path('register/', register),
    path('index/', index),
    path('goods_list/',goods_list),

]

urlpatterns +=[
    path('base/',base),
    path('order_pay/',order_pay),
    path('pay_result/',pay_result),
]
