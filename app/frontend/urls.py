from django.urls import path
from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.login_or_redirect, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]
