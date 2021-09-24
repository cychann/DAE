from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('c01', '스포츠'),
        ('c02', '게임'),
        ('c03', '독서'),
        ('c04', '함께 결제'),
        ('c05', '언어'),
        ('c06', '공예'),
        ('c07', '음악'),
        ('c08', '문화'),
        ('c09', '공모전'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='c01')
    body = models.TextField()
    upload_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like = ManyToManyField(User, related_name='like', blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']

class Comment(models.Model):
     post_id = models.ForeignKey("Post", on_delete=models.CASCADE, db_column="post_id", default="0")
     comment_id = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
     writer = models.ForeignKey(User, related_name='writer', on_delete=models.CASCADE)
     body = models.TextField()