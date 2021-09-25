from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField

# Create your models here.
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
    LOCATION_CHOICES = [
        ('l01', '서울특별시'), ('l02', '경기도'), ('l03', '강원도'), 
        ('l04', '충청남도'), ('l05', '충청북도'), 
        ('l06', '경상남도'),('l07', '경상북도'),
        ('l08', '전라남도'), ('l09', '전라북도'),
        ('l10', '인천광역시'), ('l11', '대전광역시'), ('l12', '광주광역시'), ('l13', '대구광역시'),
        ('l10', '울산광역시'), ('l11', '부산광역시'), ('l03', '제주특별자치도'),]
    title = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='c01')

    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='l01')
    capacity = models.IntegerField()
    currentCount = models.IntegerField(default=0)
    body = models.TextField()
    upload_date = models.DateTimeField()
    meet_date = models.DateTimeField()
    like = ManyToManyField(User, related_name='like', blank=True)
    applicant = ManyToManyField(User, related_name='apply', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']

class Comment(models.Model):
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE, db_column="post_id", default="0")
    comment_id = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    writer = models.ForeignKey(User, related_name='writer', on_delete=models.CASCADE)
    body = models.TextField()
