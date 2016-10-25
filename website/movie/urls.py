from django.conf.urls import url
from . import views

app_name = 'movie'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api/login/$', views.login_api, name="login_api"),
    url(r'^filter/$', views.filter, name="filter"),
    url(r'^([0-9]+)/$',views.DescriptView.as_view() , name='description'),
]
