from django.db import models
from django.core.validators import MinLengthValidator

from user.models import CustomUser

# Create your models here.
class Post(models.Model):
    title = models.CharField(
        max_length=256,
        validators= [MinLengthValidator(5, 'The title of your blog should be at least 5 characters long')]
    )
    content = models.TextField()
    blog_picture = models.ImageField(upload_to='blog_pictures', default=None, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

