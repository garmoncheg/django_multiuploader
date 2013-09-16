import os,shutil
from sorl.thumbnail.management.commands import thumbnail
from sorl.thumbnail.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Clean all temporary attachments loaded to MultiuploaderFile model'

    def handle(self, *args, **options):
        thumbnail.Command().execute("clear")
        folder = os.path.join(settings.MEDIA_ROOT,settings.THUMBNAIL_PREFIX)
        if os.path.exists(folder):
            shutil.rmtree(folder)
            
        print "Thumbnails cache cleaning complete."
