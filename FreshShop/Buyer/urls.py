from django.urls import path,re_path
from Buyer.views import *


urlpatterns = [
    path('login/',login),
    path('logout/', logout),
    path('register/', register),
    path('index/', index),
]

urlpatterns +=[
    path('base/',base),
]
