# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Comentario.comentario'
        db.add_column('items_comentario', 'comentario', self.gf('django.db.models.fields.TextField')(default=0, max_length=300), keep_default=False)

        # Adding field 'Comentario.fecha'
        db.add_column('items_comentario', 'fecha', self.gf('django.db.models.fields.DateField')(default=0), keep_default=False)

        # Adding field 'Comentario.item'
        db.add_column('items_comentario', 'item', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['items.Item']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Comentario.comentario'
        db.delete_column('items_comentario', 'comentario')

        # Deleting field 'Comentario.fecha'
        db.delete_column('items_comentario', 'fecha')

        # Deleting field 'Comentario.item'
        db.delete_column('items_comentario', 'item_id')


    models = {
        'items.comentario': {
            'Meta': {'object_name': 'Comentario'},
            'comentario': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Item']"})
        },
        'items.item': {
            'Meta': {'object_name': 'Item'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topico': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['segmentation.Topico']", 'null': 'True', 'blank': 'True'})
        },
        'items.marca': {
            'Meta': {'object_name': 'Marca'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'segmentation.topico': {
            'Meta': {'object_name': 'Topico'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['segmentation.Topico']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['items']
