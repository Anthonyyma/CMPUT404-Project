# import form class from django
from msilib.schema import CheckBox
from django import forms
from django.forms import TextInput, Textarea
from .models import Post
 
 
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["id", "content_type"]
        # fields = ["author", "title", "source", "content_type", "categories", "content", "published",]
        # fields = ["title", "categories", "content", "friends_only", "unlisted"]
        widgets = {
            "title": TextInput(attrs={
                "class": "form-group form",
            }),
            "source": TextInput(attrs={
                "class": "form-group form",
            }),
            "origin": TextInput(attrs={
                "class": "form-group form",
            }),
            # "content_type": TextInput(attrs={
            #     "class": "form-group form",
            # }),
            "categories": TextInput(attrs={
                "class": "form-group form",
            }),
            "content": Textarea(attrs={
                "class": "form-group form",
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