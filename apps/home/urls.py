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
    path("supportBulletin/", views.support_bulletin, name="supportBulletin"),
    path("routeBulletin/", views.route_bulletin, name="routeBulletin"),
    path("search/", views.search, name="search"),
    path("supportWrite/", views.support_write, name="supportWrite"),
    path("supportView/", views.support_view, name="supportView"),
    path("routeWrite/", views.route_write, name="routeWrite"),
    path("routeView/", views.route_view, name="routeView"),
]
