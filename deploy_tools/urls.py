"""deploy_tools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from release.views import week


urlpatterns = [
    url(r'^week/(?P<year>\d\d\d\d)/(?P<month>0[1-9]|1[012])/(?P<day>0[1-9]|[12][0-9]|3[01])$', week, name='week'),
    url(r'^admin/', include(admin.site.urls)),
]
