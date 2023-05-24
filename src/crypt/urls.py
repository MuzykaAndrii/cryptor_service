from django.urls import path

from .views import (
    index,
    create_picture,
    show_picture,
    picture_action,
    pictures_list,
)


urlpatterns = [
    path("", index, name="index"),
    path("create_picture", create_picture, name="create_picture"),
    path("picture/<int:pk>", show_picture, name="show_picture"),
    path("action/", picture_action, name="picture_action"),
    path("pictures/", pictures_list, name="pictures_list"),
]
