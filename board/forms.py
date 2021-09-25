from django.db.models import fields
from .models import Post
from django import forms

class BoardWriteForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category'
        ]