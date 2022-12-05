# import form class from django
# from msilib.schema import CheckBox
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import CheckboxInput, Textarea, TextInput

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["id", "content_type"]
        widgets = {
            "title": TextInput(
                attrs={"class": "form-group form", "placeholder": "Title"}
            ),
            "source": TextInput(
                attrs={"class": "form-group form", "placeholder": "Source"}
            ),
            "origin": TextInput(
                attrs={"class": "form-group form", "placeholder": "Origin"}
            ),
            "categories": TextInput(
                attrs={"class": "form-group form", "placeholder": "Categories"}
            ),
            "content": Textarea(
                attrs={
                    "class": "form-group form",
                    "placeholder": "Content",
                }
            ),
            "private_to": TextInput(
                attrs={
                    "class": "form-group form",
                    "placeholder": "Private To [Username]",
                }
            ),
            # "published": TextInput(attrs={
            #     "class": "forms",
            #     "style": "height: 200px",
            #     "placeholder": "published"
            # }),
            "friends_only": CheckboxInput(
                attrs={"class": "box", "style": "height: 30px"}
            ),
            "unlisted": CheckboxInput(attrs={"class": "box", "style": "height: 30px"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["id", "content_type"]
        widgets = {
            "content": Textarea(
                attrs={
                    "class": "form-group form",
                }
            ),
        }


class EditUserForm(forms.ModelForm):
    username = forms.CharField(
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email"}
        )
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    github = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Github"}
        ),
    )
    profile_image = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "github",
            "profile_image",
        ]


# RegisterForm that inherits from Django's UserCreationForm
class RegisterForm(UserCreationForm):
    # define form fields
    username = forms.CharField(
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email"}
        )
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        )
    )

    # set model and fields
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
