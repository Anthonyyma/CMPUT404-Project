# import form class from django
from msilib.schema import CheckBox
from django import forms
from django.forms import TextInput
from .models import Post
 
 
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["id"]
        # fields = ["author", "title", "source", "content_type", "categories", "content", "published",]
        # fields = ["title", "categories", "content", "friends_only", "unlisted"]
        widgets = {
            "title": TextInput(attrs={
                "class": "forms",
                "placeholder": "Title"
            }),
            "source": TextInput(attrs={
                "class": "forms",
                "placeholder": "Source"
            }),
            "origin": TextInput(attrs={
                "class": "forms",
                "placeholder": "origin"
            }),
            "content_type": TextInput(attrs={
                "class": "forms",
                "placeholder": "content_type"
            }),
            "categories": TextInput(attrs={
                "class": "forms",
                "placeholder": "categories"
            }),
            "content": TextInput(attrs={
                "class": "forms",
                "style": "height: 200px",
                "placeholder": "Content"
            }),        
            # "published": TextInput(attrs={
            #     "class": "forms",
            #     "style": "height: 200px",
            #     "placeholder": "published"
            # }),        
            # "friends_only": CheckBox(attrs={
            #     "class": "forms",
            #     "style": "height: 200px",
            #     "placeholder": "Content"
            # }),        
            # "unlisted": TextInput(attrs={
            #     "class": "forms",
            #     "style": "height: 200px",
            #     "placeholder": "Content"
            # }),        
        }