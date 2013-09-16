import os
import datetime

import multiuploader.default_settings as DEFAULTS

from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from multiuploader.models import MultiuploaderFile


class Command(BaseCommand):
    help = 'Clean all temporary attachments loaded to MultiuploaderFile model'

    def handle(self, *args, **options):
        expiration_time = getattr(settings, "MULTIUPLOADER_FILE_EXPIRATION_TIME", DEFAULTS.MULTIUPLOADER_FILE_EXPIRATION_TIME)
        time_threshold = datetime.datetime.now() - timedelta(seconds=expiration_time)

        for attach in MultiuploaderFile.objects.filter(upload_date__lt=time_threshold):
            try:
                os.remove(attach.file.path)
            except Exception as e:
                print e

        MultiuploaderFile.objects.filter(upload_date__lt=time_threshold).delete()

        print "Cleaning temporary upload files complete"
