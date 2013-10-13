# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Rubro'
        db.create_table('support_rubro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('support', ['Rubro'])

        # Adding model 'Topico'
        db.create_table('support_topico', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('padre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Topico'], null=True, blank=True)),
        ))
        db.send_create_signal('support', ['Topico'])

        # Adding model 'Item'
        db.create_table('support_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('topico', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Topico'])),
        ))
        db.send_create_signal('support', ['Item'])


    def backwards(self, orm):
        
        # Deleting model 'Rubro'
        db.delete_table('support_rubro')

        # Deleting model 'Topico'
        db.delete_table('support_topico')

        # Deleting model 'Item'
        db.delete_table('support_item')


    models = {
        'support.item': {
            'Meta': {'object_name': 'Item'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topico': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['support.Topico']"})
        },
        'support.rubro': {
            'Meta': {'object_name': 'Rubro'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'support.topico': {
            'Meta': {'object_name': 'Topico'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['support.Topico']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['support']
