from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    url(r'^guidance/$', views.guidance, name='guidance'),
    url(r'^team/$', views.team, name='team'),
    url(r'^$', views.homepage, name='homepage'),
]