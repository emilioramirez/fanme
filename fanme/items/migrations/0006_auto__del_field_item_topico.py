# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Item.topico'
        db.delete_column('items_item', 'topico_id')


    def backwards(self, orm):
        
        # Adding field 'Item.topico'
        db.add_column('items_item', 'topico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['segmentation.Topico'], null=True, blank=True), keep_default=False)


    models = {
        'items.comentario': {
            'Meta': {'object_name': 'Comentario'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'items.item': {
            'Meta': {'object_name': 'Item'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'items.marca': {
            'Meta': {'object_name': 'Marca'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['items']
