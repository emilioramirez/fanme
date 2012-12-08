# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Evento.fecha_inicio'
        db.delete_column('social_evento', 'fecha_inicio')

        # Deleting field 'Evento.localizacion'
        db.delete_column('social_evento', 'localizacion_id')

        # Deleting field 'Evento.descripcion'
        db.delete_column('social_evento', 'descripcion')

        # Deleting field 'Evento.fecha_creacion'
        db.delete_column('social_evento', 'fecha_creacion')

        # Deleting field 'Evento.fecha_fin'
        db.delete_column('social_evento', 'fecha_fin')

        # Removing M2M table for field invitados on 'Evento'
        db.delete_table('social_evento_invitados')


    def backwards(self, orm):
        
        # Adding field 'Evento.fecha_inicio'
        db.add_column('social_evento', 'fecha_inicio', self.gf('django.db.models.fields.DateTimeField')(default=0), keep_default=False)

        # Adding field 'Evento.localizacion'
        db.add_column('social_evento', 'localizacion', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['support.Localizacion']), keep_default=False)

        # Adding field 'Evento.descripcion'
        db.add_column('social_evento', 'descripcion', self.gf('django.db.models.fields.TextField')(default=0, max_length=300), keep_default=False)

        # Adding field 'Evento.fecha_creacion'
        db.add_column('social_evento', 'fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(default=0), keep_default=False)

        # Adding field 'Evento.fecha_fin'
        db.add_column('social_evento', 'fecha_fin', self.gf('django.db.models.fields.DateTimeField')(default=0), keep_default=False)

        # Adding M2M table for field invitados on 'Evento'
        db.create_table('social_evento_invitados', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('evento', models.ForeignKey(orm['social.evento'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('social_evento_invitados', ['evento_id', 'user_id'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'social.evento': {
            'Meta': {'object_name': 'Evento'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'social.mensaje': {
            'Meta': {'object_name': 'Mensaje'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mensaje': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mensajes_enviados'", 'to': "orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mensajes_recibidos'", 'to': "orm['auth.User']"})
        },
        'social.notificacion': {
            'Meta': {'object_name': 'Notificacion'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notificaciones_enviadas'", 'to': "orm['auth.User']"}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_expiracion': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usuarios_to': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notificaciones_recibidas'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['social']
