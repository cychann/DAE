from django.db import models
from django.db.models.fields.related import ManyToManyField

class Board(models.Model):
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
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    like = ManyToManyField('user.User', related_name='like', blank=True)
    
    def __str__(self):
        return self.title

# class Reply(models.Model):
#     reply = models.ForeignKey(Board, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=200)
#     create_date = models.DateTimeField()

#     def __str__(self):
#         return self.comment