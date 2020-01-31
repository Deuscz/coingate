from django.contrib import admin
from django.urls import path, include
from .views import *
from django.shortcuts import redirect

urlpatterns = [
    path('', TransactionView.as_view(), name='transaction'),
    path('proceed/', ProceedView.as_view(), name='proceed'),
    path('success/', SuccessView.as_view(), name='success'),
    path('fail/', FailView.as_view(), name='fail'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('callback/', CallBackView.as_view(), name='callback'),
    path('list/', Transactions_list_View.as_view(), name='list'),
]