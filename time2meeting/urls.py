from django.conf.urls import url

from . import views

app_name = 'time2meeting'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^guidance/', views.guidance, name='guidance'),
    url(r'^team/', views.team, name='team'),
    # ex: /polls/5/
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^create_event/', views.create_event, name='create_event'),
    url(r'^create_publish/', views.create_publish, name='create_publish'),
    url(r'^select_timeslots/', views.select_timeslots, name=

]
