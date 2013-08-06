from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms.widgets import ClearableFileInput
from django.contrib.admin.widgets import AdminFileWidget


from models import MultiuploaderFile


"""class MultiuploaderAdminFileWidget(AdminFileWidget):
    def __init__(self, multiuploader_file, *args, **kwargs):
        self.multiuploader_file = multiuploader_file
        super(MultiuploaderAdminFileWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        setattr(self.multiuploader_file, "url", reverse('multiuploader_file_link', kwargs={'pk': self.multiuploader_file.pk}))
        return super(MultiuploaderAdminFileWidget, self).render(name, self.multiuploader_file, attrs)


class MultiuploaderAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MultiuploaderAdminForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget = MultiuploaderAdminFileWidget(multiuploader_file=self.instance)

    class Meta:
        model = MultiuploaderFile"""


class MultiuploaderAdmin(admin.ModelAdmin):
    #form = MultiuploaderAdminForm
    search_fields = ["filename", "key_data"]
    list_display = ["filename", "upload_date", "file"]


admin.site.register(MultiuploaderFile, MultiuploaderAdmin)