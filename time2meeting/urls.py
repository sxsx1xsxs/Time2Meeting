from django.conf.urls import url

from . import views

app_name = 'time2meeting'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),

    url(r'^organize/$', views.organize_index, name='organize_index'),
    url(r'^participate/$', views.participate_index, name='participate_index'),

    url(r'^guidance/', views.guidance, name='guidance'),
    url(r'^team/', views.team, name='team'),

    # ex: /polls/5/
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/

    url(r'^create_event/$', views.create_event, name='create_event'),

    url(r'^(?P<event_id>[0-9]+)/make_decision/$', views.make_decision, name='make_decision'),
    url(r'^(?P<event_id>[0-9]+)/make_decision_results/$', views.make_decision_results, name='make_decision_results'),
    url(r'^(?P<event_id>[0-9]+)/$', views.make_decision_detail, name='make_decision_detail'),

    url(r'^create_event/', views.create_event, name='create_event'),
    url(r'^create_publish/', views.create_publish, name='create_publish'),
    url(r'^select_timeslots/', views.select_timeslots, name='select_timeslots')


]
