from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^guidance/$', views.guidance, name='guidance'),
    url(r'^team/$', views.team, name='team'),
]