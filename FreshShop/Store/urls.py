from django.urls import path,include
from Store.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/', index),
    path('page_404/',page_404),
    path('base/',base),
    path('blank/', blank),
    path('buttons/',buttons),
    path('cards/',cards),
    path('charts/', charts),
    path('forgotPwd/',forgotPwd),
    path('tables/',tables),
    path('utiAni/',utiAni),
    path('utiBor/',utiBor),
    path('utiCol/',utiCol),
    path('utiOth/',utiOth),
]
