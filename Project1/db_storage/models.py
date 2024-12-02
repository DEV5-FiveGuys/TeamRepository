from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=50)
    score = models.DecimalField(max_digits=4, decimal_places=2)
    summary = models.TextField()
    country = models.CharField(max_length=50)
    genre = models.JSONField()
    stars = models.JSONField()
    rank = models.IntegerField()

    def __str__(self):
        return self.title
