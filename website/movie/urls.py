from django.conf.urls import url
from . import views

app_name = 'movie'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api/login/$', views.login_api, name="login_api"),
    url(r'^api/logout/$', views.logout_api, name="logout_api"),
    url(r'^api/register/$', views.register_api, name="register_api"),
    url(r'^api/download/(?P<movie_id>[0-9]+)/$',views.download_api, name='download_api'),
    url(r'^api/download_bonus/(?P<movie_id>[0-9]+)/$',views.download_bonus_api, name='download_bonus_api'),
    url(r'^api/rating/(?P<movie_id>[0-9]+)/$',views.rating_api, name='rating_api'),
    url(r'^api/buy/(?P<movie_id>[0-9]+)/$',views.buy_api , name='buy_api'),
    url(r'^filter/(?P<genre>[-\w ]+)/(?P<sortby>[-\w ]+)/$', views.filter, name="filter"),
    url(r'^search/$', views.search_movie, name="search"),
    url(r'^(?P<movie_id>[0-9]+)/$',views.DescriptionView.as_view() , name='description'),
    url(r'^movies/$',views.movies , name='movies'),
    url(r'^privacypolicy/$',views.PolicyView.as_view() , name='privacypolicy'),
    url(r'^refillment/$',views.refillment_api , name='refillment'),
    url(r'^receipt/(?P<movie_id>[0-9]+)/$',views.receipt_api , name='receipt'),
    url(r'^transaction/$', views.transaction_api, name='transaction'),
    url(r'^library/$', views.LibraryView.as_view(), name='library'),
]
