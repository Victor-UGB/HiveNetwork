from dataclasses import fields
from django.forms import ModelForm
from django import forms
from .models import *


class NewPostForm(ModelForm):
    
    class Meta:
        model = Post

        labels = {
            "body" : ""
        }
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Buzz here', 'style': 'height:5rem; margin-bottom: 1rem; font-weight:400; background-color: aquamarine; border:none;'})
        }