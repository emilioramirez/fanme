# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemDenuncias'
        db.create_table(u'items_itemdenuncias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='item_denunciado', to=orm['items.Item'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='usuario_que_denuncia', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'items', ['ItemDenuncias'])


        # Changing field 'ItemImagen.imagen'
        db.alter_column(u'items_itemimagen', 'imagen', self.gf('fanmelegacy.thumbs.ImageWithThumbsField')(max_length=100, null=True))

    def backwards(self, orm):
        # Deleting model 'ItemDenuncias'
        db.delete_table(u'items_itemdenuncias')


        # Changing field 'ItemImagen.imagen'
        db.alter_column(u'items_itemimagen', 'imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

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
        u'items.comentario': {
            'Meta': {'object_name': 'Comentario'},
            'comentario': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'denuncias': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comentarios_recibidos'", 'to': u"orm['items.Item']"}),
            'me_gusta': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comentarios_realizados'", 'to': u"orm['auth.User']"})
        },
        u'items.item': {
            'Meta': {'object_name': 'Item'},
            'cantidad_fans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['segmentation.Topico']", 'null': 'True', 'blank': 'True'}),
            'users_are_comment': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'items_comentados'", 'symmetrical': 'False', 'through': u"orm['items.Comentario']", 'to': u"orm['auth.User']"})
        },
        u'items.itemdenuncias': {
            'Meta': {'object_name': 'ItemDenuncias'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'item_denunciado'", 'to': u"orm['items.Item']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'usuario_que_denuncia'", 'to': u"orm['auth.User']"})
        },
        u'items.itemimagen': {
            'Meta': {'object_name': 'ItemImagen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('fanmelegacy.thumbs.ImageWithThumbsField', [], {'default': "'items/default.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mis_imagenes'", 'to': u"orm['items.Item']"})
        },
        u'items.marca': {
            'Meta': {'object_name': 'Marca'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'items.recomendacion': {
            'Meta': {'object_name': 'Recomendacion'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'user_destino': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recomendaciones_recibidas'", 'to': u"orm['auth.User']"}),
            'user_origen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recomendaciones_enviadas'", 'to': u"orm['auth.User']"})
        },
        u'segmentation.topico': {
            'Meta': {'object_name': 'Topico'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['segmentation.Topico']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['items']