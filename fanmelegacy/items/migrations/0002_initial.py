# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Item'
        db.create_table('items_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(max_length=300)),
        ))
        db.send_create_signal('items', ['Item'])

        # Adding model 'Marca'
        db.create_table('items_marca', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('items', ['Marca'])

        # Adding model 'Comentario'
        db.create_table('items_comentario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('items', ['Comentario'])


    def backwards(self, orm):
        
        # Deleting model 'Item'
        db.delete_table('items_item')

        # Deleting model 'Marca'
        db.delete_table('items_marca')

        # Deleting model 'Comentario'
        db.delete_table('items_comentario')


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
