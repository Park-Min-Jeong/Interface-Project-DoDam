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
    path("routeView/<int:pindex>/", views.route_view, name="routeView"),
    path("search/", views.search, name="search"),
    path("supportWrite/", views.support_write, name="supportWrite"),
    path("supportView/<int:id>", views.support_view, name="supportView"), #localhost:8000/ 뒤에 supportView/숫자 가 붙는다. #forthapp\urls.py 참고
    path("routeWrite/", views.route_write, name="routeWrite"),
    path("routeWriteSearch/", views.route_write_search, name="routeWriteSearch"),
]
