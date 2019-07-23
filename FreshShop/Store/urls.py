from django.urls import path,include
from Store.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/', index),
    path('logout/',logout),
    path('base/',base),
    path('register_store/',register_store),
    path('add_goods/',add_goods),
    path('list_goods/',list_goods),
]
