from .models import Genre, Movie, UserNet
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

def base_util(request):
    all_genres = Genre.objects.all()
    all_movies_list = list(Movie.objects.values_list('movie_name', flat=True))
    user = request.user
    user_net = 0
    if user.is_authenticated:
        user_net = UserNet.objects.get
        if not UserNet.objects.filter(user=user).exists():
            UserNet.objects.filter(user=user, net=0)
        else:
            user_net = UserNet.objects.get(user=user).net
    return {
        'all_genres': all_genres,
        'all_movies_list': mark_safe(all_movies_list),
        'user_net': user_net,
    }
