from django.urls import path, include
from .views import *

urlpatterns = [
    path('', TransactionView.as_view(), name='transaction'),
    path('success/', SuccessView.as_view(), name='success'),
    path('fail/', FailView.as_view(), name='fail'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('callback/', callback, name='callback'),
    path('list/', Transactions_list_View.as_view(), name='list'),
]