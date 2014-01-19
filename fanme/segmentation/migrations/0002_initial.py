# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Topico'
        db.create_table('segmentation_topico', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('padre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['segmentation.Topico'], null=True, blank=True)),
        ))
        db.send_create_signal('segmentation', ['Topico'])

        # Adding model 'Tag'
        db.create_table('segmentation_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('segmentation', ['Tag'])

        # Adding model 'Credibilidad'
        db.create_table('segmentation_credibilidad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('segmentation', ['Credibilidad'])

        # Adding model 'Denuncia'
        db.create_table('segmentation_denuncia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('segmentation', ['Denuncia'])


    def backwards(self, orm):
        
        # Deleting model 'Topico'
        db.delete_table('segmentation_topico')

        # Deleting model 'Tag'
        db.delete_table('segmentation_tag')

        # Deleting model 'Credibilidad'
        db.delete_table('segmentation_credibilidad')

        # Deleting model 'Denuncia'
        db.delete_table('segmentation_denuncia')


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
