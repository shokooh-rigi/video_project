from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, related_name='videos')

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
