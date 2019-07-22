from django.urls import path,include
from Store.views import *

urlpatterns = [
    path('index/',index),
]
