from django.urls import path
from .views import get_transactions, make_transaction_page, create_transaction_api

urlpatterns = [
    path("open-transaction-form/", make_transaction_page, name="make_transaction"),
    path("create/", create_transaction_api, name="create_transaction_api"),
    path("list/", get_transactions, name="get_transactions"),
]