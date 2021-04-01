from django.conf.urls import url, include
from django.urls import path
from walletapi.views import *

urlpatterns = [
    url(r'^init', create_wallet_account, name='create_wallet_account'),
    path('', enable_wallet_account, name='enable_wallet_account'),
    url(r'^(?P<transaction_type>withdrawals|deposits)', wallet_transaction, name='wallet_transaction'),
]