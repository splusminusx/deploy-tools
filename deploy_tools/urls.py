from django.conf.urls import include, url
from django.contrib import admin

from release.views import week, index


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^week/(?P<year>\d\d\d\d)/(?P<month>[1-9]|1[012])/(?P<day>[1-9]|[12][0-9]|3[01])$', week, name='week'),
    url(r'^admin/', include(admin.site.urls)),
]
