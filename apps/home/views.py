# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from .paging import make_pagenator
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json

def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/home.html')
    return HttpResponse(html_template.render(context, request))


def support_bulletin(request):
    obj_list = support.objects.all().order_by("-id")
    page_obj, page_list = make_pagenator(page=request.GET.get("page", 1), num=5, obj_list=obj_list)
    context = {"page_obj":page_obj, "page_list": page_list}
    return render(request, "home/support-bulletin.html", context)

@login_required(login_url="/login/")
def support_write(request):
    context = None
    if request.method == "POST":
        try:
            title = request.POST.get("title")
            content = request.POST.get("content")
            user = User.objects.get(pk=request.user.id)

            if title == "" or content == "":
                raise

            sup = support(title=title, writer=user, question=content, answer=None, answered=0)
            sup.save()
        except:
            message = "잘못된 입력입니다."
            success = False
        else:
            message = request.user.username + "님의 게시글이 저장되었습니다."
            success = True

        context = {"message": message, "success": success}

    return render(request, "home/support-write.html", context)


def support_view(request, id): #forthapp\views.py의 u()와 r() 참고
    post = support.objects.get(id=id) #왼쪽 id는 support 테이블의 primary key인 id #오른쪽 id는 주소창의 supportView/뒤에 오는 숫자 값으로 글의 id값을 넘겨받음
    answering = None
    # if request.POST.get('answerQ'): #'answerQ'에 내용이 있으면 #원래는 support_write()처럼 if request.method == 'POST'가 정석인듯 함. 그래서 바꿨음.
    if request.method == 'POST':
        answering = request.POST.get('answerQ') #답변 작성한 textarea 내용을 얻어옴
        post.answer = answering #될지 모르고 해본건데 됐음
        post.answered = 1   #1은 y, 0은 n
        post.save()         # 저장
    context = {"post": post, "answerContent": answering}
    return render(request, "home/support-view.html", context)


def route_bulletin(request):
    obj_list = route.objects.all().order_by("-id")
    page_obj, page_list = make_pagenator(page=request.GET.get("page", 1), num=5, obj_list=obj_list)

    data_list = list()
    for data in page_obj:
        Pcd1_list, Ctcd_list = list(), list()
        for detail_data in data.routedetail_set.all():
            Pcd1_list.append(detail_data.ccbaCpno.ccbaPcd1Nm)
            Ctcd_list.append(detail_data.ccbaCpno.ccbaCtcdNm)
        Pcd1 = ", ".join(set(Pcd1_list))
        Ctcd = ", ".join(set(Ctcd_list))
        data_list.append([data, Pcd1, Ctcd])

    context = {"data_list": data_list, "page_obj":page_obj, "page_list": page_list}

    return render(request, "home/route-bulletin.html", context)


def route_view(request, id):
    post = route.objects.get(id=id)
    obj_list = list()

    for detail in post.routedetail_set.all():
        detail_h = detail.ccbaCpno
        detail_dict = {
            "order":detail.order,
            "comment":detail.comment,
            "ccbaPcd1Nm":detail_h.ccbaPcd1Nm,
            "ccbaCtcdNm":detail_h.ccbaCtcdNm,
            "ccmaName":detail_h.ccmaName,
            "crltsnoNm":detail_h.crltsnoNm,
            "ccbaMnm1":detail_h.ccbaMnm1,
            "imageUrl":detail_h.imageUrl,
            "longitude":detail_h.longitude,
            "latitude":detail_h.latitude
        }
        obj_list.append(detail_dict)

    context = {"post": post, "obj_list": obj_list}
    return render(request, "home/route-view.html", context)


@login_required(login_url="/login/")
def route_write(request):
    context = None
    if request.method == "POST":
        success = False

        try:
            ccbaCpno = request.POST.getlist("ccbaCpno")
            comments = request.POST.getlist("comments")
            user = User.objects.get(pk=request.user.id)

            if "" in ccbaCpno:
                raise

            r_list = route(writer=user)
            r_list.save()
            post_id = route.objects.last().id
            for i in range(len(ccbaCpno)):
                r_detail = routeDetail(order=i+1, comment=comments[i], ccbaCpno_id=ccbaCpno[i], post_id=post_id)
                r_detail.save()

            message = request.user.username + "님의 게시글이 저장되었습니다."
            success = True
        except:
            message = "잘못된 입력입니다."

        context = {"message": message, "success": success}

    return render(request, "home/route-write.html", context)


def route_write_search(request):
    keyword = request.GET.get("keyword", None)
    order = request.GET.get("order", 1)

    if keyword:
        obj_list = heritage.objects.filter(ccbaMnm1__contains=keyword).order_by("ccbaCpno")
    else:
        obj_list = heritage.objects.all().order_by("ccbaCpno")

    page_obj, page_list = make_pagenator(page=request.GET.get("page", 1), num=5, obj_list=obj_list)

    context = {"page_obj": page_obj, "page_list": page_list,
               "keyword": keyword, "resultlen": len(obj_list), "order":order}

    return render(request, "home/route-write-search.html", context)

def search(request):
    obj_dict = dict()
    for Pcd1 in ["석기", "청동기", "철기", "고구려", "백제", "신라", "가야", "통일신라",
                 "고려", "조선", "대한제국", "일제강점기"]:
        obj_dict[Pcd1] = list()
        for obj in heritage.objects.filter(ccbaPcd1Nm__exact=Pcd1).all():
            obj_dict[Pcd1].append({
                "ccbaPcd1Nm": obj.ccbaPcd1Nm,
                "ccbaCtcdNm": obj.ccbaCtcdNm,
                "ccmaName": obj.ccmaName,
                "crltsnoNm": obj.crltsnoNm,
                "ccbaMnm1": obj.ccbaMnm1,
                "imageUrl": obj.imageUrl,
                "longitude": obj.longitude,
                "latitude": obj.latitude
            })

    if request.method == "POST":
        pcd1_list = json.loads(request.POST.get("pcd1_list"))
        print(pcd1_list)
        result_dict = dict()
        for pcd1 in pcd1_list:
            result_dict[pcd1] = obj_dict[pcd1]

        return JsonResponse(result_dict, json_dumps_params={"ensure_ascii": False})
    else:
        return render(request, "home/search.html")


def copyright(request):
    return render(request, "home/copyright.html")