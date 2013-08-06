import os
import re
import magic

from django import forms
from django.conf import settings
from django.utils import simplejson
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from utils import format_file_extensions

import multiuploader.default_settings as DEFAULTS


class MultiuploadWidget(forms.MultipleHiddenInput):
    def __init__(self, attrs={}):
        super(MultiuploadWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        widget_ = super(MultiuploadWidget, self).render(name, value, attrs)
        output = '<div id="hidden_container" style="display:none;">%s</div>' % widget_
        return mark_safe(output)


class MultiuploaderField(forms.MultiValueField):
    widget = MultiuploadWidget()

    def formfield(self, **kwargs):
        kwargs['widget'] = MultiuploadWidget
        return super(MultiuploaderField, self).formfield(**kwargs)

    def validate(self, values):
        super(MultiuploaderField, self).validate(values)

    def clean(self, values):
        super(MultiuploaderField, self).clean(values)
        return values

    def compress(self, value):
        if value:
            return value

        return None


class MultiUploadForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        multiuploader_settings = getattr(settings, "MULTIUPLOADER_FORMS_SETTINGS", DEFAULTS.MULTIUPLOADER_FORMS_SETTINGS)

        form_type = kwargs.pop("form_type", "default")

        options = {
            'maxFileSize': multiuploader_settings[form_type]["MAX_FILE_SIZE"],
            'acceptFileTypes': format_file_extensions(multiuploader_settings[form_type]["FILE_TYPES"]),
            'maxNumberOfFiles': multiuploader_settings[form_type]["MAX_FILE_NUMBER"],
            'allowedContentTypes': map(str.lower, multiuploader_settings[form_type]["CONTENT_TYPES"]),
            'autoUpload': multiuploader_settings[form_type]["AUTO_UPLOAD"]
        }

        self._options = options
        self.options = simplejson.dumps(options)

        super(MultiUploadForm, self).__init__(*args, **kwargs)

        self.fields["file"].widget = forms.FileInput(attrs={'multiple': True})

    def clean_file(self):
        content = self.cleaned_data[u'file']

        filename, extension = os.path.splitext(content.name)

        if re.match(self._options['acceptFileTypes'], extension, flags=re.I) is None:
            raise forms.ValidationError('acceptFileTypes')

        content_type = magic.from_buffer(content.read(1024), mime=True)

        if content_type.lower() in self._options['allowedContentTypes']:
            if content._size > self._options['maxFileSize']:
                raise forms.ValidationError("maxFileSize")
        else:
            raise forms.ValidationError("acceptFileTypes")

        return content


class MultiuploaderMultiDeleteForm(forms.Form):
    id = MultiuploaderField()
