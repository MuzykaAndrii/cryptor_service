from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import PictureCreationForm, PictureActionForm, SinglePictureActionForm
from .painter.painter import Painter
from .models import Picture
from .services.encryption import encryptor
from .services.decryption import decryptor


@login_required(login_url="login_user")
def about(request):
    return render(request, "crypt/about.html")


@login_required(login_url="login_user")
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


@login_required(login_url="login_user")
def show_picture(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    if picture.owner != request.user:
        raise PermissionDenied

    if request.method == "GET":
        form = SinglePictureActionForm(instance=picture)
        return render(
            request, "crypt/show_picture.html", {"picture": picture, "form": form}
        )

    elif request.method == "POST":
        form = SinglePictureActionForm(request.POST)
        redirect_dest = redirect("show_picture", pk=picture.pk)

        if not form.is_valid():
            messages.error(request, "Wrong form data received")
            return redirect_dest

        text = form.cleaned_data["text"]
        action = form.cleaned_data["last_action"]
        image_file_path = picture.image.path

        if action == "encryption":
            return encryptor(
                request,
                text,
                picture,
                image_file_path,
                action,
                picture.pk,
                redirect_dest,
            )

        elif action == "decryption":
            return decryptor(
                request, picture, image_file_path, action, picture.pk, redirect_dest
            )

        else:
            messages.error(request, "Invalid action")
            return redirect_dest


@login_required(login_url="login_user")
def picture_action(request):
    if request.method == "GET":
        pictures = Picture.objects.filter(owner=request.user)[:3]
        form = PictureActionForm(pictures)

        return render(
            request, "crypt/picture_action.html", {"form": form, "pictures": pictures}
        )

    if request.method == "POST":
        pictures = Picture.objects.filter(owner=request.user)[:3]
        form = PictureActionForm(pictures, request.POST)
        redirect_url = redirect("picture_action")

        if not form.is_valid() or not form.cleaned_data["image"]:
            messages.error(request, "Wrong form data received")
            return redirect_url

        image_pk = form.cleaned_data["image"]
        text = form.cleaned_data["text"]
        action = form.cleaned_data["last_action"]
        picture = Picture.objects.get(pk=image_pk)
        image_file_path = picture.image.path

        if action == "encryption":
            return encryptor(
                request,
                text,
                picture,
                image_file_path,
                action,
                image_pk,
                redirect_url,
            )

        elif action == "decryption":
            return decryptor(
                request,
                picture,
                image_file_path,
                action,
                image_pk,
                redirect_url,
            )

        else:
            messages.error(request, "Invalid action")
            return redirect_url


@login_required(login_url="login_user")
def pictures_list(request):
    pictures = Picture.objects.filter(owner=request.user)

    return render(request, "crypt/pictures_list.html", {"pictures": pictures})
