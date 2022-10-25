# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.conf import settings


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


class support(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    writeDT = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    question = models.TextField()
    answer = models.TextField(null=True)
    answered = models.IntegerField(choices=[(1, "y"), (0, "n")])


class route(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class routeDetail(models.Model):
    post = models.ForeignKey(route, on_delete=models.CASCADE)
    order = models.IntegerField()
    ccbaCpno = models.ForeignKey(heritage, on_delete=models.CASCADE)
    comment = models.TextField(null=True)