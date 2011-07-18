from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^delete/(\d+)/$', 'multiuploader.views.multiuploader_delete'),
    url(r'^multi/$', 'multiuploader.views.multiuploader', name='multi'),
    (r'^image/(\d+)/$', 'multiuploader.views.multi_show_uploaded'),
)