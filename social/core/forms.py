# import form class from django
from django import forms
from forms import Post
 
# import GeeksModel from models.py
from .models import GeeksModel
 
# create a ModelForm
class GeeksForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Post
        fields = "__all__"