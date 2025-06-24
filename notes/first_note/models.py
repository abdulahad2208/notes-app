from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    pdf = models.FileField(upload_to='tweets/pdfs/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."


# Create your models here.
