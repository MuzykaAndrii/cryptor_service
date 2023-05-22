from django.urls import path

from .views import (
    index,
    create_picture,
    show_picture,
)


urlpatterns = [
    path("index/", index, name="index"),
    path("create_picture", create_picture, name="create_picture"),
    path("picture/<int:pk>", show_picture, name="show_picture"),
]
