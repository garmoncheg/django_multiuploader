import logging
from django.conf import settings

from django.utils import simplejson
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.core.signing import Signer, BadSignature
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

from utils import FileResponse
from models import MultiuploaderFile
from forms import MultiUploadForm, MultiuploaderMultiDeleteForm

from sorl.thumbnail import get_thumbnail

log = logging


def multiuploader_delete_multiple(request, ok=False):
    if request.method == 'POST':

        form = MultiuploaderMultiDeleteForm(request.POST)

        if form.is_valid():
            return redirect(request.META.get('HTTP_REFERER', None))
        else:
            pass

        log.info('Called delete multiple files')

        """fl = get_object_or_404(MultiuploaderFile, pk=pk)
        fl.delete()
        log.info('DONE. Deleted file id=' + str(pk))"""

        return HttpResponse(1)

    else:
        log.info('Received not POST request to delete file view')
        return HttpResponseBadRequest('Only POST accepted')


def multiuploader_delete(request, pk):
    if request.method == 'POST':
        log.info('Called delete file. File id=' + str(pk))
        fl = get_object_or_404(MultiuploaderFile, pk=pk)
        fl.delete()
        log.info('DONE. Deleted file id=' + str(pk))

        return HttpResponse(1)

    else:
        log.info('Received not POST request to delete file view')
        return HttpResponseBadRequest('Only POST accepted')


def multiuploader(request, noajax=False):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """

    if request.method == 'POST':
        log.info('received POST to main multiuploader view')

        if request.FILES is None:
            response_data = [{"error": _('Must have files attached!')}]
            return HttpResponse(simplejson.dumps(response_data))

        if not u'form_type' in request.POST:
            response_data = [{"error": _("Error when detecting form type, form_type is missing")}]
            return HttpResponse(simplejson.dumps(response_data))

        signer = Signer()

        try:
            form_type = signer.unsign(request.POST.get(u"form_type"))
        except BadSignature:
            response_data = [{"error": _("Tampering detected!")}]
            return HttpResponse(simplejson.dumps(response_data))

        form = MultiUploadForm(request.POST, request.FILES, form_type=form_type)

        if not form.is_valid():
            error = _("Unknown error")

            if "file" in form._errors and len(form._errors["file"]) > 0:
                error = form._errors["file"][0]

            response_data = [{"error": error}]
            return HttpResponse(simplejson.dumps(response_data))

        file = request.FILES[u'file']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size

        log.info('Got file: "%s"' % filename)

        #writing file manually into model
        #because we don't need form of any type.
        
        fl = MultiuploaderFile()
        fl.filename = filename
        fl.file = file
        fl.save()

        log.info('File saving done')

        thumb_url = ""

        try:
            im = get_thumbnail(fl.file, "80x80", quality=50)
            thumb_url = im.url
        except Exception as e:
            log.error(e)
            
        #generating json response array
        result = [{"id": fl.id,
                   "name": filename,
                   "size": file_size,
                   "url": reverse('multiuploader_file_link', args=[fl.pk]),
                   "thumbnail_url": thumb_url,
                   "delete_url": reverse('multiuploader_delete', args=[fl.pk]),
                   "delete_type": "POST", }]

        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        
        if noajax:
            if request.META['HTTP_REFERER']:
                redirect(request.META['HTTP_REFERER'])
        
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else:  # GET
        return HttpResponse('Only POST accepted')


def multi_get_files(request, fieldname, noajax=False):
    """
    View to retrieve MultiuploaderFiles based on a list of ids.
    """

    if request.method == 'GET':
        log.info('received GET to get files view')

        if not u'form_type' in request.GET:
            response_data = [{"error": _("Error when detecting form type, form_type is missing")}]
            return HttpResponse(simplejson.dumps(response_data))

        signer = Signer()

        try:
            form_type = signer.unsign(request.GET.get(u"form_type"))
        except BadSignature:
            response_data = [{"error": _("Tampering detected!")}]
            return HttpResponse(simplejson.dumps(response_data))

        #log.info('Got file: "%s"' % filename)
        result = []
        for p in request.GET.getlist(fieldname):
            fl = MultiuploaderFile.objects.get(id=p)
    
            thumb_url = ""
            try:
                im = get_thumbnail(fl.file, "80x80", quality=50)
                thumb_url = im.url
            except Exception as e:
                log.error(e)
                
            #generating json response array
            result.append({"id": fl.id,
                       "name": fl.filename,
                       "size": fl.file.size,
                       "url": reverse('multiuploader_file_link', args=[fl.pk]),
                       "thumbnail_url": thumb_url,
                       "delete_url": reverse('multiuploader_delete', args=[fl.pk]),
                       "delete_type": "POST", })

        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        
        if noajax:
            if request.META['HTTP_REFERER']:
                redirect(request.META['HTTP_REFERER'])
        
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else:  # POST
        return HttpResponse('Only GET accepted')


def multi_show_uploaded(request, pk):
    fl = get_object_or_404(MultiuploaderFile, id=pk)
    return FileResponse(request,fl.file.path, fl.filename)