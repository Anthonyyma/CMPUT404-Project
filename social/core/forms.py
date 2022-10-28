# import form class from django
#from msilib.schema import CheckBox
from django import forms
from django.forms import TextInput, Textarea
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from .models import User
 
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

# RegisterForm that inherits from Django's UserCreationForm
class RegisterForm(UserCreationForm):
    # define form fields
    username = forms.CharField(min_length=5, max_length=150,widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email'}))
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    
    # set model and fields
    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password1", "password2"]
