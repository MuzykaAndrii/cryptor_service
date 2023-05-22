from io import BytesIO

from django.core.files import File
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import PictureCreationForm
from .painter.painter import Painter


def index(request):
    return HttpResponse("Hello")


def create_picture(request):
    if request.method == "GET":
        form = PictureCreationForm()
        return render(request, "crypt/create_picture.html", {"form": form})

    form = PictureCreationForm(request.POST)
    if form.is_valid():
        picture = form.save(commit=False)
        painter = Painter(picture.width, picture.height)
        image = painter.draw(picture.draw_method)
        blob = BytesIO()
        image.save(blob, "BMP")

        picture.owner = request.user
        picture.image.save("some_name.bmp", File(blob), save=False)
        picture.save()

        return redirect("create_picture")


def show_picture(request):
    pass
