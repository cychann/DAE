from django import forms
from django.forms.widgets import Textarea
from .models import Post, Comment

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class PostForm(forms.ModelForm):
    category = forms.ChoiceField(
        widget=forms.RadioSelect, 
        choices=Post.CATEGORY_CHOICES,
        label='카테고리'
    )
    meet_date = forms.DateField(
        widget=DateTimeInput(),
        label='날짜'
    )
    title = forms.CharField(
        widget = forms.TextInput(),
        label='제목'
    )
    location = forms.ChoiceField(
        choices=Post.CATEGORY_CHOICES,
        label='지역'
    )
    capacity = forms.IntegerField(
        widget = forms.NumberInput(attrs = {'step':1, 'min':1 }),
        label='정원'
    )
    body = forms.CharField(
        widget = forms.Textarea(),
        label = "본문"
    )
    class Meta:
        model = Post
        fields = ['title', 'category', 'location', 'capacity', 'meet_date', 'body']


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget = forms.Textarea(),
        label = "댓글"
    )
    class Meta:
        model = Comment
        fields = ['body']
