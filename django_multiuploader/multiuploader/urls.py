from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
                       url(r'^multiuploader_delete_multiple/$', 'multiuploader.views.multiuploader_delete_multiple',
                           name='multiuploader_delete_multiple'),
                       url(r'^multiuploader_delete/(?P<pk>\w+)/$', 'multiuploader.views.multiuploader_delete',
                           name='multiuploader_delete'),
                       url(r'^multiuploader/$', 'multiuploader.views.multiuploader', name='multiuploader'),
                       url(r'^multiuploader_noajax/$', 'multiuploader.views.multiuploader', kwargs={"noajax": True},
                           name='multiploader_noajax'),
                       url(r'^multiuploader_file/(?P<pk>\w*)/$', 'multiuploader.views.multi_show_uploaded',
                           name='multiuploader_file_link')
)
