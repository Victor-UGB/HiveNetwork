from dataclasses import fields
from django.forms import ModelForm
from django import forms
from .models import *


class NewPostForm(ModelForm):
    
    class Meta:
        model = Post

        labels = {
            "body" : "Buzz here"
        }
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What\'s on your mind', 'label': 'Buzz here'})
        }