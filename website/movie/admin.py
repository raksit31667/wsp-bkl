from django.contrib import admin
from .models import Movie, Genre, Rating, Refillment
# Register your models here.

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(Refillment)
