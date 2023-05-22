from django.urls import path

from .views import index, create_picture


urlpatterns = [
    path("index/", index, name="index"),
    path("create_image", create_picture, name="create_picture"),
]
