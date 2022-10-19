# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *


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
    num = 3
    page = request.GET.get("page", 1)
    obj_list = route.objects.all().order_by("-id")

    paginator = Paginator(obj_list, num)
    page_obj = paginator.get_page(page)
    page_list = paginator.get_elided_page_range(number=page, on_each_side=2, on_ends=1)
    data_list = list()

    for data in page_obj:
        Pcd1_list, Ctcd_list = list(), list()
        for detail_data in data.routedetail_set.all():
            Pcd1_list.append(detail_data.ccbaCpno.ccbaPcd1Nm)
            Ctcd_list.append(detail_data.ccbaCpno.ccbaCtcdNm)
        Pcd1 = ", ".join(set(Pcd1_list))
        Ctcd = ", ".join(set(Ctcd_list))
        data_list.append([data, Pcd1, Ctcd])

    context = {"bulletin":
                   {"page_obj": page_obj, "data_list": data_list, "page_list": page_list}
               }

    return render(request, "home/route-bulletin.html", context)


def route_view(request, pindex):
    post = route.objects.get(id=pindex)
    post_detail = post.routedetail_set.all()
    context = {"post": post, "post_detail": post_detail}

    return render(request, "home/route-view.html", context)


def route_write(request):
    if request.method == "POST":
        print(request.POST)
        ccbaCpno = request.POST.getlist("ccbaCpno")
        comments = request.POST.getlist("comments")

        r_list = route(writer_id=1)
        r_list.save()

        p_id = route.objects.last().id

        for i in range(len(ccbaCpno)):
            r_detail = routeDetail(order=i+1, comment=comments[i], ccbaCpno_id=ccbaCpno[i], post_id=p_id)
            r_detail.save()

    return render(request, "home/route-write.html")


def route_write_search(request):
    page = request.GET.get("page", 1)
    keyword = request.GET.get("keyword", None)
    order = request.GET.get("order", 1)
    if keyword:
        obj_list = heritage.objects.filter(ccbaMnm1__contains=keyword).order_by("ccbaCpno")
    else:
        obj_list = heritage.objects.all().order_by("ccbaCpno")

    paginator = Paginator(obj_list, 5)
    page_obj = paginator.get_page(page)
    page_list = paginator.get_elided_page_range(number=page, on_each_side=2, on_ends=1)
    context = {"page_obj": page_obj, "page_list": page_list,
               "keyword": keyword, "resultlen": len(obj_list),
               "order":order}

    return render(request, "home/route-write-search.html", context)




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
