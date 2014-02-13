# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EstadoxInvitado.invitado'
        db.add_column(u'social_estadoxinvitado', 'invitado',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='invitacion_eventos', to=orm['auth.User']),
                      keep_default=False)

        # Removing M2M table for field invitado on 'EstadoxInvitado'
        db.delete_table(db.shorten_name(u'social_estadoxinvitado_invitado'))


    def backwards(self, orm):
        # Deleting field 'EstadoxInvitado.invitado'
        db.delete_column(u'social_estadoxinvitado', 'invitado_id')

        # Adding M2M table for field invitado on 'EstadoxInvitado'
        m2m_table_name = db.shorten_name(u'social_estadoxinvitado_invitado')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('estadoxinvitado', models.ForeignKey(orm[u'social.estadoxinvitado'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['estadoxinvitado_id', 'user_id'])


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
        },
        u'social.actividad': {
            'Meta': {'object_name': 'Actividad'},
            'comentario': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_coment'", 'null': 'True', 'blank': 'True', 'to': u"orm['items.Comentario']"}),
            'descripcion': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_item'", 'null': 'True', 'blank': 'True', 'to': u"orm['items.Item']"}),
            'recomendacion': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_recom'", 'null': 'True', 'blank': 'True', 'to': u"orm['items.Recomendacion']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'usuario_destino': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_destino'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'usuario_origen': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_origen'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'social.consulta': {
            'Meta': {'object_name': 'Consulta'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mis_consultas'", 'to': u"orm['items.Item']"}),
            'mensaje': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas_enviadas'", 'to': u"orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas_recibidas'", 'to': u"orm['auth.User']"})
        },
        u'social.estadoxinvitado': {
            'Meta': {'object_name': 'EstadoxInvitado'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'evento': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['social.Evento']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitado': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitacion_eventos'", 'to': u"orm['auth.User']"})
        },
        u'social.evento': {
            'Meta': {'object_name': 'Evento'},
            'creador': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventos_creados'", 'to': u"orm['auth.User']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha_creacion': ('django.db.models.fields.DateField', [], {}),
            'fecha_fin': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'default': "'images/calendario-default.png'", 'max_length': '100'}),
            'invitados': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'eventos_invitado'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'latitud': ('django.db.models.fields.CharField', [], {'default': "'0.0'", 'max_length': '30'}),
            'longitud': ('django.db.models.fields.CharField', [], {'default': "'0.0'", 'max_length': '30'}),
            'nombre': ('django.db.models.fields.CharField', [], {'default': "'Nombre'", 'max_length': '30'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['social.TipoEvento']", 'null': 'True', 'blank': 'True'})
        },
        u'social.mensaje': {
            'Meta': {'object_name': 'Mensaje'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mensaje': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mensajes_enviados'", 'to': u"orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mensajes_recibidos'", 'to': u"orm['auth.User']"})
        },
        u'social.notificacion': {
            'Meta': {'object_name': 'Notificacion'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notificaciones_enviadas'", 'to': u"orm['auth.User']"}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_desde': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_expiracion': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'default': "'images/calendario-default.png'", 'max_length': '100'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'usuarios_to': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notificaciones_recibidas'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'social.tipoevento': {
            'Meta': {'object_name': 'TipoEvento'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['social']