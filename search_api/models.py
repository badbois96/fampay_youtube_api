from django.db import models


# Create your models here.

class Youtube(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=200)
    published_at = models.DateTimeField()
    thumbnail_url = models.CharField(max_length=150)
    video_id = models.CharField(max_length=100, unique=True)
    channel_title = models.CharField(max_length=150)
    channel_id = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    @property
    def video_url(self):
        return ' '.join(["https://www.youtube.com/watch?v=", self.video_id])
