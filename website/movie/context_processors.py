from .models import Genre, Movie
from django.utils.safestring import mark_safe

def base_util(request):
    all_genres = Genre.objects.all()
    all_movies_list = list(Movie.objects.values_list('movie_name', flat=True))

    return {
        'all_genres': all_genres,
        'all_movies_list': mark_safe(all_movies_list),
    }
