# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MultiuploaderFile'
        db.create_table('multiuploader_multiuploaderfile', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('multiuploader', ['MultiuploaderFile'])


    def backwards(self, orm):
        # Deleting model 'MultiuploaderFile'
        db.delete_table('multiuploader_multiuploaderfile')


    models = {
        'multiuploader.multiuploaderfile': {
            'Meta': {'object_name': 'MultiuploaderFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['multiuploader']