from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(requuest):
    return HttpResponse('This is app 1')
def index1(requuest):
    return HttpResponse('This is app 1: Nguyen van quynh')
