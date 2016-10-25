from django.conf.urls import url
from . import views

app_name = 'movie'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api/login/$', views.login_api, name="login_api"),
    url(r'^filter//?genre_id=(?P<genre_id>[0-9]+)/$', views.filter, name="filter"),
    url(r'^search/$', views.search_movie, name="search"),
    url(r'^download/([0-9]+)/$',views.download_movie, name='movie'),
]
