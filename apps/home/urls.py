# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path("", views.index, name="home"),

    # Matches any html file
    # re_path(r"^.*\.*", views.pages, name="pages"),

    # 추가한 내용
    path("support/", views.support_bulletin),
    path("route/", views.route_bulletin),
    path("search/", views.search),
    path("supportWrite/", views.support_write),
    path("supportView/", views.support_view),
    path("routeWrite/", views.route_write),
    path("routeView/", views.route_view),
]
