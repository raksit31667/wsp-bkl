from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Genre(models.Model):
    genre_name = models.CharField(max_length=15)
    genre_description = models.CharField(max_length=500)

    def __str__(self):
        return self.genre_name

class Movie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=300)
    movie_description = models.CharField(max_length=500)
    release_year = models.PositiveSmallIntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    movie_price = models.SmallIntegerField(default=0)
    movie_teaser_url = models.CharField(max_length=100)
    movie_thumbnail = models.FileField()
    movie_file = models.FileField()
    user = models.ForeignKey(User, default=1)

    def __str__(self):
        return self.movie_name
