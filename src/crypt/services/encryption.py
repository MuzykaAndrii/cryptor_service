from django.contrib import messages
from django.shortcuts import redirect

from crypt.cryptor.exceptions import TooSmallImageError
from crypt.cryptor.cryptor import (
    hide,
    clear_usefull_data,
    open_bmp,
)


def encryptor(request, text, picture, image_file_path, action, image_pk, redirect_):
    if not text.isascii():
        messages.error(request, "The input text should be an ASCII string")
        return redirect_

    image = open_bmp(image_file_path)

    if picture.last_action == "encryption":
        image = clear_usefull_data(image)

    try:
        image_crypted = hide(image, text)
    except TooSmallImageError:
        messages.error(
            request,
            "The given text is too large for encryption for this image, select another image or make text more breif",
        )
        return redirect_

    picture.last_action = action
    picture.last_action_result = text
    picture.save(image_crypted)

    messages.warning(request, "Text crypted successfully")
    return redirect("show_picture", pk=image_pk)
