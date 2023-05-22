from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from .forms import PictureCreationForm, PictureActionForm
from .painter.painter import Painter
from .models import Picture


def index(request):
    return render(request, "crypt/index.html")


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
    if picture.owner != request.user:
        raise PermissionDenied
    return render(request, "crypt/show_picture.html", {"picture": picture})


def picture_action(request):
    form = PictureActionForm()
    return render(request, "crypt/picture_action.html", {"form": form})
