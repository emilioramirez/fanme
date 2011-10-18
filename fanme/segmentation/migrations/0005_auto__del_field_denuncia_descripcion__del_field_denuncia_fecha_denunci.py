# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Denuncia.descripcion'
        db.delete_column('segmentation_denuncia', 'descripcion')

        # Deleting field 'Denuncia.fecha_denuncia'
        db.delete_column('segmentation_denuncia', 'fecha_denuncia')

        # Deleting field 'Denuncia.fecha_resolucion'
        db.delete_column('segmentation_denuncia', 'fecha_resolucion')


    def backwards(self, orm):
        
        # Adding field 'Denuncia.descripcion'
        db.add_column('segmentation_denuncia', 'descripcion', self.gf('django.db.models.fields.TextField')(default=0, max_length=300), keep_default=False)

        # Adding field 'Denuncia.fecha_denuncia'
        db.add_column('segmentation_denuncia', 'fecha_denuncia', self.gf('django.db.models.fields.DateTimeField')(default=0), keep_default=False)

        # Adding field 'Denuncia.fecha_resolucion'
        db.add_column('segmentation_denuncia', 'fecha_resolucion', self.gf('django.db.models.fields.DateTimeField')(default=0), keep_default=False)


    models = {
        'segmentation.credibilidad': {
            'Meta': {'object_name': 'Credibilidad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'segmentation.denuncia': {
            'Meta': {'object_name': 'Denuncia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'segmentation.tag': {
            'Meta': {'object_name': 'Tag'},
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

    complete_apps = ['segmentation']
