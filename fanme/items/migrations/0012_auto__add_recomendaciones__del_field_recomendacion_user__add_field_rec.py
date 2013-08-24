# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Recomendaciones'
        db.create_table('items_recomendaciones', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_origen', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('items', ['Recomendaciones'])

        # Deleting field 'Recomendacion.user'
        db.delete_column('items_recomendacion', 'user_id')

        # Adding field 'Recomendacion.user_destino'
        db.add_column('items_recomendacion', 'user_destino', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']), keep_default=False)

        # Adding field 'Recomendacion.user_origen'
        db.add_column('items_recomendacion', 'user_origen', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['items.Recomendaciones']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Recomendaciones'
        db.delete_table('items_recomendaciones')

        # Adding field 'Recomendacion.user'
        db.add_column('items_recomendacion', 'user', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']), keep_default=False)

        # Deleting field 'Recomendacion.user_destino'
        db.delete_column('items_recomendacion', 'user_destino_id')

        # Deleting field 'Recomendacion.user_origen'
        db.delete_column('items_recomendacion', 'user_origen_id')


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
        'items.comentario': {
            'Meta': {'object_name': 'Comentario'},
            'comentario': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Item']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'items.item': {
            'Meta': {'object_name': 'Item'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topico': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['segmentation.Topico']", 'null': 'True', 'blank': 'True'}),
            'users_are_comment': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['items.Comentario']", 'symmetrical': 'False'}),
            'users_recomendation': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recomendaciones_recibidas'", 'symmetrical': 'False', 'through': "orm['items.Recomendacion']", 'to': "orm['auth.User']"})
        },
        'items.marca': {
            'Meta': {'object_name': 'Marca'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'items.recomendacion': {
            'Meta': {'object_name': 'Recomendacion'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Item']"}),
            'user_destino': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_origen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Recomendaciones']"})
        },
        'items.recomendaciones': {
            'Meta': {'object_name': 'Recomendaciones'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_origen': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
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
