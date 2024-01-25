from django.forms import ModelForm, Textarea, TextInput, CheckboxSelectMultiple

from .models import Post


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ["url", "body", "tags"]
        labels = {"body": "Caption", "tags": "Category"}
        widgets = {
            "body": Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add a caption...",
                    "class": "font1 text-4xl",
                }
            ),
            "url": TextInput(attrs={"placeholder": "Add url..."}),
            "tags": CheckboxSelectMultiple(),
        }


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ["body", "tags"]
        labels = {"body": "", "tags": "Category"}
        widgets = {
            "body": Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add a caption...",
                    "class": "font1 text-4xl",
                }
            ),
            "tags": CheckboxSelectMultiple(),
        }
