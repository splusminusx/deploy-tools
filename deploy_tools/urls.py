from django.conf.urls import include, url
from django.contrib import admin

from release.views import period, index, fact_list, fact_create, fact_request


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<status>plan|history)/(?P<period>month|week)/(?P<year>\d\d\d\d)/(?P<month>[1-9]|1[012])/(?P<day>[1-9]|[12][0-9]|3[01])$', period, name='period'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^deploymentfact/list', fact_list, name='deployment_fact'),
    url(r'^deploymentfact/request', fact_request, name='fact_request'),
    url(r'^deploymentfact/create', fact_create, name='fact_create'),
]
