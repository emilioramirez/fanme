# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccionAnalisisDenuncia'
        db.create_table(u'segmentation_accionanalisisdenuncia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accion', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'segmentation', ['AccionAnalisisDenuncia'])

        # Adding model 'EstadoAnalisisDenuncia'
        db.create_table(u'segmentation_estadoanalisisdenuncia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'segmentation', ['EstadoAnalisisDenuncia'])

        # Adding model 'AnalisisDenuncia'
        db.create_table(u'segmentation_analisisdenuncia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fecha_resolucion', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('moderador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('accion_tomada', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['segmentation.AccionAnalisisDenuncia'])),
            ('estado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['segmentation.EstadoAnalisisDenuncia'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_analisisdenuncia', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'segmentation', ['AnalisisDenuncia'])


    def backwards(self, orm):
        # Deleting model 'AccionAnalisisDenuncia'
        db.delete_table(u'segmentation_accionanalisisdenuncia')

        # Deleting model 'EstadoAnalisisDenuncia'
        db.delete_table(u'segmentation_estadoanalisisdenuncia')

        # Deleting model 'AnalisisDenuncia'
        db.delete_table(u'segmentation_analisisdenuncia')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'segmentation.accionanalisisdenuncia': {
            'Meta': {'object_name': 'AccionAnalisisDenuncia'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'segmentation.analisisdenuncia': {
            'Meta': {'ordering': "('fecha_creacion',)", 'object_name': 'AnalisisDenuncia'},
            'accion_tomada': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['segmentation.AccionAnalisisDenuncia']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_analisisdenuncia'", 'to': u"orm['contenttypes.ContentType']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['segmentation.EstadoAnalisisDenuncia']"}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_resolucion': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'segmentation.credibilidad': {
            'Meta': {'object_name': 'Credibilidad'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'segmentation.denuncia': {
            'Meta': {'object_name': 'Denuncia'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'fecha_denuncia': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_resolucion': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'segmentation.estadoanalisisdenuncia': {
            'Meta': {'object_name': 'EstadoAnalisisDenuncia'},
            'descripcion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'segmentation.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'segmentation.topico': {
            'Meta': {'object_name': 'Topico'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['segmentation.Topico']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['segmentation']