from models import MultiuploaderImage
from django.contrib import admin

class MultiuploaderImageAdmin(admin.ModelAdmin):
    search_fields = ["filename", "key_data"]
    list_display = ["filename", "image", "key_data"]
    list_filter = ["filename", "image", "key_data"]

admin.site.register(MultiuploaderImage, MultiuploaderImageAdmin)