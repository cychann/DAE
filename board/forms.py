from django
from django.db.models import fields from forms
from .models import Board

class BoardWriteForm(forms.ModelForm):
    
    class Meta:
        model = Board
        fields = [
            'title',
            'content',
            'category'
        ]