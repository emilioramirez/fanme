# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Item'
        db.delete_table('support_item')

        # Deleting model 'Topico'
        db.delete_table('support_topico')

        # Deleting model 'Marca'
        db.delete_table('support_marca')


    def backwards(self, orm):
        
        # Adding model 'Item'
        db.create_table('support_item', (
            ('descripcion', self.gf('django.db.models.fields.TextField')(max_length=300)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Topico'])),
        ))
        db.send_create_signal('support', ['Item'])

        # Adding model 'Topico'
        db.create_table('support_topico', (
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('padre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Topico'], null=True, blank=True)),
        ))
        db.send_create_signal('support', ['Topico'])

        # Adding model 'Marca'
        db.create_table('support_marca', (
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('support', ['Marca'])


    models = {
        'support.localidad': {
            'Meta': {'object_name': 'Localidad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['support.Provincia']"})
        },
        'support.localizacion': {
            'Meta': {'object_name': 'Localizacion'},
            'barrio': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localidad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['support.Localidad']"}),
            'numero': ('django.db.models.fields.IntegerField', [], {}),
            'numero_local': ('django.db.models.fields.IntegerField', [], {})
        },
        'support.pais': {
            'Meta': {'object_name': 'Pais'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'support.provincia': {
            'Meta': {'object_name': 'Provincia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['support.Pais']"})
        },
        'support.rubro': {
            'Meta': {'object_name': 'Rubro'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['support']
