from django.forms import ModelForm
from .models import Picture


class PictureCreationForm(ModelForm):
    class Meta:
        model = Picture
        fields = [
            "width",
            "height",
            "draw_method",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
