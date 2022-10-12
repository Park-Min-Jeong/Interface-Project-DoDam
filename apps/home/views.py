# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render


def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/home.html')
    return HttpResponse(html_template.render(context, request))


def support_bulletin(request):
    return render(request, "home/support-bulletin.html")


def support_write(request):
    return render(request, "home/support-write.html")


def support_view(request):
    return render(request, "home/support-view.html")


def route_bulletin(request):
    return render(request, "home/route-bulletin.html")


def route_write(request):
    return render(request, "home/route-write.html")


def route_view(request):
    return render(request, "home/route-view.html")


def search(request):
    return render(request, "home/search.html")


# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:
#         load_template = request.path.split('/')[-1]
#
#         if load_template == "admin":
#             return HttpResponseRedirect(reverse("admin:index"))
#         context["segment"] = load_template
#
#         html_template = loader.get_template("home/" + load_template)
#         return HttpResponse(html_template.render(context, request))
#
#     except template.TemplateDoesNotExist:
#         html_template = loader.get_template("home/page-404.html")
#         return HttpResponse(html_template.render(context, request))
#
#     except:
#         html_template = loader.get_template("home/page-500.html")
#         return HttpResponse(html_template.render(context, request))
