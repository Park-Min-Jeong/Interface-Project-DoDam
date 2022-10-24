# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.urls import path
from apps.home import views

urlpatterns = [
    path("", views.index, name="home"),
    path("copyright/", views.copyright, name="copyright"),
    path("search/", views.search, name="search"),
    path("routeBulletin/", views.route_bulletin, name="routeBulletin"),
    path("routeView/<int:id>/", views.route_view, name="routeView"),
    path("routeWrite/", views.route_write, name="routeWrite"),
    path("routeWriteSearch/", views.route_write_search, name="routeWriteSearch"),
    path("supportBulletin/", views.support_bulletin, name="supportBulletin"),
    path("supportView/<int:id>", views.support_view, name="supportView"),
    path("supportWrite/", views.support_write, name="supportWrite"),
]