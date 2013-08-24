# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Plan'
        db.create_table('bussiness_plan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('bussiness', ['Plan'])


    def backwards(self, orm):
        
        # Deleting model 'Plan'
        db.delete_table('bussiness_plan')


    models = {
        'bussiness.plan': {
            'Meta': {'object_name': 'Plan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['bussiness']
