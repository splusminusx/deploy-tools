from django.conf.urls import include, url
from django.contrib import admin

from release.views import period, index


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<status>plan|history)/(?P<period>month|week)/(?P<year>\d\d\d\d)/(?P<month>[1-9]|1[012])/(?P<day>[1-9]|[12][0-9]|3[01])$', period, name='period'),
    url(r'^admin/', include(admin.site.urls)),
]
