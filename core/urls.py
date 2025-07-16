from django.urls import path, include

urlpatterns = [
    path("api/token/", include("app.auth.urls")),
    path("api/accounts/", include("app.accounts.urls")),
    path("api/transactions/", include("app.transactions.urls")),
    path("", include("app.frontend.urls", namespace="frontend")),
]
