from django.conf.urls.defaults import *
from django.conf import settings

try:
    delete_url = settings.MULTI_FILE_DELETE_URL
except AttributeError:
    delete_url = 'multi_delete'

try:
    image_url = settings.MULTI_IMAGE_URL
except AttributeError:
    image_url = 'multi_image'

urlpatterns = patterns('',
    (r'^'+delete_url+'/(\d+)/$', 'multiuploader.views.multiuploader_delete'),
    url(r'^multi/$', 'multiuploader.views.multiuploader', name='multi'),
    (r'^'+image_url+'/(\d+)/$', 'multiuploader.views.multi_show_uploaded'),
)