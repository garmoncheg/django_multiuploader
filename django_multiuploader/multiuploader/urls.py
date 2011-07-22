from django.conf.urls.defaults import *
from django.conf import settings

if settings.MULTI_FILE_DELETE_URL:
    delete_url = settings.MULTI_FILE_DELETE_URL
else:
    delete_url = 'multi_delete'

urlpatterns = patterns('',
    (r'^'+delete_url+'/(\d+)/$', 'multiuploader.views.multiuploader_delete'),
    url(r'^multi/$', 'multiuploader.views.multiuploader', name='multi'),
    (r'^image/(\d+)/$', 'multiuploader.views.multi_show_uploaded'),
)