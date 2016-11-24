from django.conf.urls import url
from . import views

app_name = 'movie'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api/login/$', views.login_api, name="login_api"),
    url(r'^api/logout/$', views.logout_api, name="logout_api"),
    url(r'^api/register/$', views.register_api, name="register_api"),
    url(r'^api/download/([0-9]+)/$',views.download_api, name='download_api'),
    url(r'^api/rating/([0-9]+)/$',views.rating_api, name='rating_api'),
    url(r'^filter/(?P<genre>[\w\-]+)/(?P<sortby>[\w\-]+)/$', views.filter, name="filter"),
    url(r'^search/$', views.search_movie, name="search"),
    url(r'^([0-9]+)/$',views.DescriptionView.as_view() , name='description'),
    url(r'^movies/$',views.movies , name='movies'),
    url(r'^privacypolicy/$',views.PolicyView.as_view() , name='privacypolicy'),
    url(r'^refillment/$',views.refillment_api , name='refillment'),
]
