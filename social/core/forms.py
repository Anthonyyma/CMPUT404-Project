# import form class from django
from django import forms
from django.forms import TextInput
from .models import Post
 
 
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        # fields = ["title", "categories", "content", "friends_only", "unlisted"]
        widgets = {
            "title": TextInput(attrs={
                "class": "forms",
                "placeholder": "Title"
            }),
            "content": TextInput(attrs={
                "class": "forms",
                "style": "height: 200px",
                "placeholder": "Content"
            }),        }