"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import notifications.urls
from django.conf.urls import include, url
from django.contrib import admin
from home import views

urlpatterns = [
    url(r'^manage_event/', include('manage_event.urls')),
    url(r'^admin/', admin.site.urls),
    # This is our homepage!
    url(r'^$', views.homepage),
    url(r'^home/', include('home.urls')),
    url(r'^account/', include('social_django.urls', namespace='social')),
    url(r'^account/', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),

]
