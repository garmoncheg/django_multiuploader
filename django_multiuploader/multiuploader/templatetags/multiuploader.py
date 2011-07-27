from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('multiuploader/multiuploader_main.html')
def multiupform():
    return {'static_url':settings.MEDIA_URL,}