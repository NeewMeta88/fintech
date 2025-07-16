from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import LoginForm
from .forms import RegisterForm



def login_or_redirect(request):
    if request.user.is_authenticated:
        return redirect("frontend:dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect("frontend:dashboard")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("frontend:login")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("frontend:login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})