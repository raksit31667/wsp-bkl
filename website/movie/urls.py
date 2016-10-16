from django.conf.urls import url

from . import views

app_name = 'movie'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^api/login/$', views.login_api, name="login_api"),
    url(r'^api/register/$', views.register_api, name="register_api"),
    url(r'^filter/$', views.filter, name="filter"),
]
