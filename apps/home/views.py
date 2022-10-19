# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render

from django.contrib.auth.models import User #support_write()의 User 객체 사용을 위한 구문
from .models import support                 #support_write()의 sup = support(id=id, writer = writer, question=content, answer=None, answered=0)를 위한 구문. support는 models.py에 있는 모델 클래스 이름
from django.core.paginator import Paginator #support_bulletin()의 Paginator를 위한 구문

#10/17 추가
from django.contrib.auth import get_user_model #support_write()에서 로그인한 User 정보를 가져오기 위함.
from django.contrib.auth import authenticate, login

def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/home.html')
    return HttpResponse(html_template.render(context, request))


def support_bulletin(request):  #visitorapp\views.py의 v_read()를 참고.(13~23번째 라인)
    page = request.GET.get('page', 1)
    vlist = support.objects.all()
    paginator = Paginator(vlist.order_by('-id'), 5) #페이징실습.pdf 1pg 마지막 참고함. #게시글 2개마다 페이징 #-id로 줘서 id값 내림차순으로 정렬함.
    #print(paginator)
    vlistpage = paginator.get_page(page)
    #print(type(vlistpage))
    #for d in vlistpage :
    #    print(type(d), d)
    context = {"vlist": vlistpage}  #페이지 정보를 넘겨줌
    return render(request, "home/support-bulletin.html", context)

#@login_required #로그인 했을때만 동작하도록 하는 키워드인데 비로그인시 그냥 404 에러를 리턴해버림
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
