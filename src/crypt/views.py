from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello")


def create_picture(request):
    pass


def show_picture(request):
    pass
