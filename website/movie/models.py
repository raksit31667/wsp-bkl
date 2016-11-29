from django.db import models
from django.db.models import Avg
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
        if self.movie_name:
            return self.movie_name + " (%d)" % self.release_year

    def get_avg_rating(self):
        return Rating.objects.filter(movie=self).aggregate(Avg('rating'))['rating__avg']

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1)
    rating = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "%s reviewed %s as %d" % (self.user, self.movie, self.rating)

class Serial(models.Model):
    serial_code = models.CharField(max_length=15)
    price = models.SmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
       return self.serial_code

class Transaction(models.Model):
    user = models.ForeignKey(User, default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.SmallIntegerField(default=0)
    net = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        if(self.price > 0):
            return "%s refilled %d.(%s)" % (self.user, self.price, self.timestamp)
        else:
            return self.user

class UserNet(models.Model):
    user = models.ForeignKey(User, default=1)
    net = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "%s has %d." % (self.user, self.net)

class UserOwn(models.Model):
    user = models.ForeignKey(User, default=1)
    movie = models.ForeignKey(Movie)

    def __str__(self):
        return "%s has %s." % (self.user, self.movie)
