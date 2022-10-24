# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm

#sooeun
from django.core.mail.message import EmailMessage

def send_email(request):
    subject = 'message'
    to = ["dodamtrinity@gmail.com"]
    from_email = 'id@gmail.com'
    message = '메세지 테스트'
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "이메일 혹은 비밀번호를 잘못 입력하셨습니다"
        else:
            msg = "입력 형식을 확인하세요"

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)

            msg = "회원가입이 완료되었습니다"
            success = True
            # return redirect("/login/")

        else:
            msg = "입력 형식을 확인하세요"
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def policy(request):
    return render(request, "accounts/policy.html")


def policy_check(request):
    return render(request, "accounts/policy-check.html")


def newPw(request):
    return render(request, "accounts/newPw.html")