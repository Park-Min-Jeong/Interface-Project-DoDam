# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

#sooeun
from . import views

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("policy/", policy, name="policy"),
    path("policyCheck/", policy_check, name="policyCheck"),
    path("newPw/", newPw, name="newPw"),
    path("send_email/", views.send_email, name='send_email'),
]
