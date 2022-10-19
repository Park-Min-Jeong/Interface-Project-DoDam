# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User 사용하지 않는 이유
# https://wayhome25.github.io/django/2017/05/18/django-auth/

# 회원가입 id:개발자 pw:개발자1 영어로
class heritage(models.Model):
    ccbaCpno = models.CharField(max_length=13, primary_key=True)
    ccbaPcd1 = models.CharField(max_length=2)
    ccbaPcd1Nm = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    ccbaCtcd = models.CharField(max_length=2)
    ccbaCtcdNm = models.TextField()
    ccbaKdcd = models.CharField(max_length=2)
    ccmaName = models.CharField(max_length=2)
    crltsnoNm = models.TextField()
    ccbaMnm1 = models.TextField()
    ccbaMnm2 = models.TextField(null=True)
    imageUrl = models.URLField(max_length=100)
    content = models.TextField()
    ccceName = models.TextField(null=True)
    ccbaLcad = models.TextField()
    ccbaAdmin = models.TextField()
    ccbaPoss = models.TextField()
    ccbaAsdt = models.DateField()

    def __str__(self):
        return f"{str(self.ccbaPcd1)} / {str(self.ccbaCtcd)}: {str(self.ccbaMnm1)}"


class support(models.Model):
    # id = models.IntegerField(primary_key=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #값 지정 방법은 Visitorapp views.py의 48번째 라인 reply_create() 참고
    writeDT = models.DateTimeField(auto_now_add=True) #Visitorapp models.py 참고
    title = models.TextField()
    question = models.TextField()
    answer = models.TextField(null=True)
    answered = models.IntegerField(choices=[(1, "y"), (0, "n")])
    # home.support.answered: (fields.E005)
    # 'choices' must be an iterable containing (actual value, human readable name) tuples.


class route(models.Model):
    # id = models.IntegerField(primary_key=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class routeDetail(models.Model):
    # id = models.IntegerField(primary_key=True)
    post = models.ForeignKey(route, on_delete=models.CASCADE)
    order = models.IntegerField()
    ccbaCpno = models.ForeignKey(heritage, on_delete=models.CASCADE)
    comment = models.TextField(null=True)