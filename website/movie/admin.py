from django.contrib import admin
from .models import Movie, Genre, Rating, Serial, Transaction, UserNet
# Register your models here.

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(Serial)
admin.site.register(Transaction)
admin.site.register(UserNet)

