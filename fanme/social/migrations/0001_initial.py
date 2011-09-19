# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Evento'
        db.create_table('social_evento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('social', ['Evento'])


    def backwards(self, orm):
        
        # Deleting model 'Evento'
        db.delete_table('social_evento')


    models = {
        'social.evento': {
            'Meta': {'object_name': 'Evento'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['social']
