from .models import Genre, Movie
import json

def base_util(request):
    all_genres = Genre.objects.all()
    all_movies_list = list(Movie.objects.values_list('movie_name', flat=True))

    return {
        'all_genres': all_genres,
        'all_movies_list': json.dumps(all_movies_list),
    }
