# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .paging import make_pagenator
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required

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
def support_write(request): #forthapp\views.py의 c() 참고함.
    if request.method == 'POST' : #주소창에 입력한 정보가 안 뜸 #POST방식으로 요청하면 DB테이블에 전달된 정보를 저장한다.
        content = request.POST.get('content')
        title = request.POST.get('title')

        if request.user.is_authenticated: #사용자가 로그인을 했다면
            #user = User.objects.get(username=request.user.username) #이 경우 후보키인 username으로 회원정보를 얻어오고
            user = User.objects.get(pk=request.user.id)             #이 경우 주 키인 id로 회원정보를 얻어옴. 구글에서 "django 로그인 사용자 가져오기" 검색했음. 사이트 링크는 이메일로 저장해둠.
            context = {"msg": request.user.username+"님의 게시글 업로드 완료!" }
            writer = user
            # writeDT는 자동.
            sup = support(title=title, writer=writer, question=content, answer=None, answered=0)  # support 테이블에 내용
            sup.save()  # 저장
        else: #사용자가 로그인을 안 했다면 #게시글 작성이 안 되게 구현해야 함.(코드 수정 필요)
            #user = User.objects.get(pk=1)  #처음에는 비로그인 상태에서는 1번 사용자로 user값을 줬음 # Visitorapp views.py의 48번째 라인 reply_create() 참고 #https://docs.djangoproject.com/en/4.1/topics/auth/default/#user-objects 도 참고 #pk는 primarykey
            #context = {"msg": "게시글 업로드 완료!"}
            # 아래 코드로 비로그인 상태에서는 게시글 작성이 안되도록 함 #일단 1차적으로 비로그인 상태라면 supportBulletin.html에서 작성 버튼이 안 보임.
            context = {"msg": "로그인 필요!" }
    else : #POST가 아닌 GET방식으로 요청하면 None을 전달하면서 support-write.html에게 렌더링을 시킨다.
        context = None
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
    context = {"post" : post, "answerContent":answering}
    return render(request, "home/support-view.html", context)


def route_bulletin(request):
    obj_list = route.objects.all().order_by("-id")
    page_obj, page_list = make_pagenator(page=request.GET.get("page", 1), num=3, obj_list=obj_list)

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
    post_detail = list()

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
        post_detail.append(detail_dict)

    context = {"post": post, "post_detail": post_detail}
    return render(request, "home/route-view.html", context)


@login_required(login_url="/login/")
def route_write(request):
    context = None
    if request.method == "POST":
        success = False
        ccbaCpno = request.POST.getlist("ccbaCpno")
        comments = request.POST.getlist("comments")
        user = User.objects.get(pk=request.user.id)

        if "" not in ccbaCpno:
            r_list = route(writer=user)
            r_list.save()
            p_id = route.objects.last().id
            for i in range(len(ccbaCpno)):
                r_detail = routeDetail(order=i+1, comment=comments[i], ccbaCpno_id=ccbaCpno[i], post_id=p_id)
                r_detail.save()

            message = request.user.username + "님의 게시글 업로드 완료!"
            success = True
        else:
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
    obj_list = list()
    for Pcd1 in ["석기", "청동기", "철기", "고구려", "백제", "신라", "가야", "통일신라",
                 "고려", "조선", "대한제국", "일제강점기"]:
        detail_list = list()
        for obj in heritage.objects.filter(ccbaPcd1Nm__exact=Pcd1).all():
            detail_dict = {
                "ccbaPcd1Nm":obj.ccbaPcd1Nm,
                "ccbaCtcdNm":obj.ccbaCtcdNm,
                "ccmaName":obj.ccmaName,
                "crltsnoNm":obj.crltsnoNm,
                "ccbaMnm1":obj.ccbaMnm1,
                "imageUrl":obj.imageUrl,
                "longitude":obj.longitude,
                "latitude":obj.latitude
            }
            detail_list.append(detail_dict)
        obj_list.append(detail_list)

    context = {"obj_list": obj_list}
    return render(request, "home/search.html", context)


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
