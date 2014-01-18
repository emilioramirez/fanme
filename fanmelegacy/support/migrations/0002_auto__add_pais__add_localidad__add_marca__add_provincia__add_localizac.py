# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Pais'
        db.create_table('support_pais', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('support', ['Pais'])

        # Adding model 'Localidad'
        db.create_table('support_localidad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Provincia'])),
        ))
        db.send_create_signal('support', ['Localidad'])

        # Adding model 'Marca'
        db.create_table('support_marca', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('support', ['Marca'])

        # Adding model 'Provincia'
        db.create_table('support_provincia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Pais'])),
        ))
        db.send_create_signal('support', ['Provincia'])

        # Adding model 'Localizacion'
        db.create_table('support_localizacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('barrio', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('calle', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('numero', self.gf('django.db.models.fields.IntegerField')()),
            ('numero_local', self.gf('django.db.models.fields.IntegerField')()),
            ('localidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['support.Localidad'])),
        ))
        db.send_create_signal('support', ['Localizacion'])


    def backwards(self, orm):
        
        # Deleting model 'Pais'
        db.delete_table('support_pais')

        # Deleting model 'Localidad'
        db.delete_table('support_localidad')

        # Deleting model 'Marca'
        db.delete_table('support_marca')

        # Deleting model 'Provincia'
        db.delete_table('support_provincia')

        # Deleting model 'Localizacion'
        db.delete_table('support_localizacion')


    models = {
        'support.item': {
            'Meta': {'object_name': 'Item'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topico': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['support.Topico']"})
        },
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
        'support.marca': {
            'Meta': {'object_name': 'Marca'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
