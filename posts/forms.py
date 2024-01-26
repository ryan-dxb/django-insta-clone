from django.forms import ModelForm, Textarea, TextInput, CheckboxSelectMultiple

from .models import Post, Comments, Reply


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


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["body"]
        widgets = {
            "body": TextInput(
                attrs={"placeholder": "Add comment ...", "class": "flex-1"}
            )
        }
        labels = {"body": ""}


class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ["body"]
        widgets = {
            "body": TextInput(
                attrs={"placeholder": "Add reply ...", "class": "!text-sm"}
            )
        }
        labels = {"body": ""}
