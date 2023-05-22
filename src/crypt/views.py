from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import PictureCreationForm


def index(request):
    return HttpResponse("Hello")


def create_picture(request):
    if request.method == "GET":
        form = PictureCreationForm()
        return render(request, "crypt/create_picture.html", {"form": form})

    form = PictureCreationForm(request.POST)
    if form.is_valid():
        print(form)
        return redirect("create_picture")


def show_picture(request):
    pass
