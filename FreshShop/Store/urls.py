from django.urls import path,include
from Store.views import *

urlpatterns = [
    path('index/',index),
    path('cart/',cart),
    path('detail/',detail),
    path('list/',list),
    path('login/',login),
    path('place_order/',place_order),
    path('register/',register),
    path('user_center_info/',user_center_info),
    path('user_center_order/',user_center_order),
    path('user_center_site/',user_center_site),

]
