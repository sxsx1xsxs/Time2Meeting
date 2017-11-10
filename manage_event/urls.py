from django.conf.urls import url

from . import views

app_name = 'manage_event'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^organize/$', views.organize_index, name='organize_index'),
    url(r'^participate/$', views.participate_index, name='participate_index'),


    url(r'^(?P<event_id>[0-9]+)/make_decision/$', views.make_decision, name='make_decision'),
    url(r'^(?P<event_id>[0-9]+)/make_decision_results/$', views.make_decision_results, name='make_decision_results'),
    url(r'^(?P<event_id>[0-9]+)/$', views.make_decision_detail, name='make_decision_detail'),
    url(r'^(?P<event_id>[0-9]+)/show_decision_result/$', views.show_decision_result, name='show_decision_result'),

    url(r'^create_event/$', views.create_event, name='create_event'),
    url(r'^(?P<event_id>[0-9]+)/create_publish/$', views.create_publish, name='create_publish'),
    url(r'^(?P<event_id>[0-9]+)/select_timeslots/$', views.select_timeslots, name='select_timeslots'),
    url(r'^(?P<event_id>[0-9]+)/modify_timeslots/$', views.modify_timeslots, name='modify_timeslots'),
    # url(r'^$', views.Home),
    url(r'^profile/$', views.update_profile),
    url(r'^logout/$', views.webLogout),
    url(r'^(?P<event_id>[0-9]+)/select_publish/$', views.select_publish, name="select_publish"),
    url(r'^(?P<event_id>[0-9]+)/modify_timeslots_read/$',views.modify_timeslots_read, name= "modify_timeslots_read"),
    url(r'^(?P<event_id>[0-9]+)/read_timeslots/$', views.read_timeslots, name='read_timeslots'),
    url(r'^(?P<event_id>[0-9]+)/initialize_timeslots/$', views.initialize_timeslots, name='initialize_timeslots'),
    url(r'^(?P<event_id>[0-9]+)/modify_timeslots_update/$', views.modify_timeslots_update, name='modify_timeslots_update'),
    url(r'^(?P<event_id>[0-9]+)/select_publish_render/$', views.select_publish_render, name="select_publish_render"),

    #url(r'^(?P<event_id>[0-9]+)/read_timeslots/$', views.get_each_user_timeslots, name='get_each_user_timeslots'),
]
