from django.conf.urls import include, url

from django.contrib import admin
from . import views

admin.autodiscover()


urlpatterns = [
   url(r'^$', views.home, name='home'),
   url(r'^admin/', include(admin.site.urls)),
   url('', include('social.apps.django_app.urls', namespace='social')),
   url('', include('django.contrib.auth.urls', namespace='auth')),
               ]
