from django import forms
from .models import Picture


class PictureCreationForm(forms.ModelForm):
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


class PictureActionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    image = forms.ChoiceField(
        choices=[],
        required=False,
    )

    class Meta:
        model = Picture
        fields = [
            "last_action",
        ]

    def __init__(self, pictures, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["image"].choices += [(picture.pk, "") for picture in pictures]

        self.fields["text"].required = False

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label


class SinglePictureActionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Picture
        fields = [
            "last_action",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["text"].required = False

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
