from django.conf.urls import url

from . import views

app_name = 'time2meeting'
urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^guidance/', views.guidance, name='guidance'),
    url(r'^team/', views.team, name='team'),

    url(r'^create_event/', views.create_event, name='create_event'),
    url(r'^create_publish/', views.create_publish, name='create_publish'),
    url(r'^select_timeslots/', views.select_timeslots, name='select_timeslots')


]
