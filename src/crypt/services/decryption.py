from django.contrib import messages
from django.shortcuts import redirect

from crypt.cryptor.cryptor import show


def decryptor(request, picture, image_file_path, action, image_pk, redirect_):
    if not picture.last_action:
        messages.warning(request, "This picture havent crypted text")
        return redirect_

    decrypted_text = show(image_file_path)
    picture.last_action = action
    picture.last_action_result = decrypted_text
    picture.save(None)

    messages.warning(request, f"The secret decrypted text: {decrypted_text}")
    return redirect("show_picture", pk=image_pk)
