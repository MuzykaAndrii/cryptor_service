from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .forms import PictureCreationForm, PictureActionForm
from .painter.painter import Painter
from .models import Picture
from .cryptor.cryptor import show, hide


def index(request):
    return render(request, "crypt/index.html")


def create_picture(request):
    if request.method == "GET":
        form = PictureCreationForm()
        return render(request, "crypt/create_picture.html", {"form": form})

    form = PictureCreationForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Picture data are not valid")
        return redirect("create_picture")

    picture = form.save(commit=False)
    picture.owner = request.user

    painter = Painter(picture.width, picture.height)
    image = painter.draw(picture.draw_method)

    picture.save(image)

    messages.success(request, "Picture created successfully")
    return redirect("show_picture", pk=picture.pk)


def show_picture(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    if picture.owner != request.user:
        raise PermissionDenied
    return render(request, "crypt/show_picture.html", {"picture": picture})


def picture_action(request):
    if request.method == "GET":
        pictures = Picture.objects.filter(owner=request.user)[:3]
        form = PictureActionForm(pictures)

        return render(
            request, "crypt/picture_action.html", {"form": form, "pictures": pictures}
        )
    else:
        pictures = Picture.objects.filter(owner=request.user)[:3]
        form = PictureActionForm(pictures, request.POST)

        if not form.is_valid():
            messages.error("Wrong action data received")
            return redirect("picture_action")

        image_pk = form.cleaned_data["image"]
        text = form.cleaned_data["text"]
        action = form.cleaned_data["last_action"]
        picture = Picture.objects.get(pk=image_pk)

        if action == "encryption":
            image_file_path = picture.image.path
            image_crypted = hide(image_file_path, text)

            picture.last_action = action
            picture.last_action_result = text
            picture.save(image_crypted)

            messages.success(request, "Text crypted successfully")
            return redirect("index")

        elif action == "decryption":
            pass
