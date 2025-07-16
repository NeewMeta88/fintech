from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, account_detail_view, get_all_accounts
from django.urls import path

router = DefaultRouter()
router.register(r'', AccountViewSet, basename='account')

urlpatterns = router.urls + [
    path('detail/<uuid:account_id>/', account_detail_view, name='account_detail'),
    path('all', get_all_accounts, name='accounts_all'),
]
