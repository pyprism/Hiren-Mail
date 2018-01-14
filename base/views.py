from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib import messages
from .models import Account
from django.db.utils import IntegrityError


def login(request):
    """
    Handles authentication
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('inbox')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('inbox')
        else:
            messages.error(request, 'Username/Password is not valid!')
            return redirect('login')
    else:
        return render(request, 'base/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('inbox')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        count = Account.objects.count()
        acc = Account(username=username, password=make_password(password))
        if count == 0:
            acc.is_admin = True
        else:
            pass
        try:
            acc.save()
        except IntegrityError:
            messages.error(request, "username is not available!")
            return redirect('signup')
        messages.success(request, 'Account created successfully!')
        return redirect('signup')
    else:
        return render(request, 'base/signup.html')


@login_required
def settings(request):
    if request.user.is_admin:
        return render(request, 'base/settings.html')



