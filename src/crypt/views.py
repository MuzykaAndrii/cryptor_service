from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .forms import PictureCreationForm
from .painter.painter import Painter
from .models import Picture


def index(request):
    return HttpResponse("Hello")


def create_picture(request):
    if request.method == "GET":
        form = PictureCreationForm()
        return render(request, "crypt/create_picture.html", {"form": form})

    form = PictureCreationForm(request.POST)
    if form.is_valid():
        picture = form.save(commit=False)
        picture.owner = request.user

        painter = Painter(picture.width, picture.height)
        image = painter.draw(picture.draw_method)

        picture.save(image)

        return redirect("show_picture", pk=picture.pk)


def show_picture(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, "crypt/show_picture.html", {"picture": picture})
