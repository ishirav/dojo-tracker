"""dojo_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from dojo_tracker.main.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^track$', track_view, name='track'),
    url(r'^entries$', entries_view),
    url(r'^entries/([0-9]+)$', entries_view),
    url(r'^register$', register_view, name='register'),
    url(r'^([0-9a-zA-Z]+)$', personal_view, name='personal'),
]
