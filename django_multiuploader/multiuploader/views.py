from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from models import MultiuploaderImage
from django.core.files.uploadedfile import UploadedFile

#importing json parser to generate jQuery plugin friendly json response
from django.utils import simplejson

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail import get_thumbnail


from django.views.decorators.csrf import csrf_exempt

import logging
log = logging

@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
        log.info('Called delete image. image id='+str(pk))
        image = get_object_or_404(MultiuploaderImage, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def multiuploader(request):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('Got file: "%s"' % str(filename))
        log.info('Content type: "$s" % file.content_type')

        #writing file manually into model
        #because we don't need form of any type.
        image = MultiuploaderImage()
        image.filename=str(filename)
        image.image=file
        image.key_data = image.key_generate
        image.save()
        log.info('File saving done')

        #getting thumbnail url using sorl-thumbnail
        if 'image' in file.content_type.lower():
            im = get_thumbnail(image, "80x80", quality=50)
            thumb_url = im.url
        else:
            thumb_url = ''

        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
            file_url = settings.MULTI_IMAGE_URL+'/'+image.key_data+'/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/'+image.key_data+'/'

        """
        is actually: [{"name": "Screenshot from 2012-11-14 16:17:46.png", "url": "multi_image/95925526541943247735000327303075602114185579370918344597903504067450818566531/", "thumbnail_url": "/media/cache/f8/bd/f8bd83aadeba651ff9c040bb394ce117.jpg", "delete_type": "POST", "delete_url": "multi_delete/7/", "size": 38520}]
        should be:   {"files":[{"url":"http://jquery-file-upload.appspot.com/AMIfv9734HSTDGd3tIybbnKVru--IjhjULKvNcIGUL2lvfqA93RNCAizDbvP-RQJNbh-N9m8UXsk-90jFFYSp8TlbZYhEcNN6Vb9HzQVQtdmF83H6sE_XkdnlI2V8lHX5V3Y4AamdX6VMbAt9sNWNx2BVGzhTfAYkRLYmRE1VzzWSe9C8c8Fu8g/Screenshot%20from%202012-11-14%2016%3A17%3A46.png","thumbnail_url":"http://lh5.ggpht.com/fcjVNT6qUGoMDtqqaNDNtU4mghy34qlzfj2GujikLgC7Nj5Bs4LUT_DWG_Q8OWujqvYHsKbeQ9pkvoAW4WiaubmqQxobIPyt=s80","name":"Screenshot from 2012-11-14 16:17:46.png","type":"image/png","size":38520,"delete_url":"http://jquery-file-upload.appspot.com/AMIfv9734HSTDGd3tIybbnKVru--IjhjULKvNcIGUL2lvfqA93RNCAizDbvP-RQJNbh-N9m8UXsk-90jFFYSp8TlbZYhEcNN6Vb9HzQVQtdmF83H6sE_XkdnlI2V8lHX5V3Y4AamdX6VMbAt9sNWNx2BVGzhTfAYkRLYmRE1VzzWSe9C8c8Fu8g/Screenshot%20from%202012-11-14%2016%3A17%3A46.png?delete=true","delete_type":"DELETE"}]}
        """

        #generating json response array
        result = {
            'files': [ {"name":filename, 
                       "size":file_size, 
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/', 
                       "delete_type":"POST",}
                    ]
        }
        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')

def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(MultiuploaderImage, key_data=key)
    url = settings.MEDIA_URL+image.image.name
    return render_to_response('multiuploader/one_image.html', {"multi_single_url":url,})