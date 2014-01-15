# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Consulta.item'
        db.delete_column('social_consulta', 'item_id')


    def backwards(self, orm):
        
        # Adding field 'Consulta.item'
        db.add_column('social_consulta', 'item', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='mis_consultas', to=orm['items.Item']), keep_default=False)


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
            'denuncias': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comentarios_recibidos'", 'to': "orm['items.Item']"}),
            'me_gusta': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comentarios_realizados'", 'to': "orm['auth.User']"})
        },
        'items.item': {
            'Meta': {'object_name': 'Item'},
            'cantidad_fans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topico': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['segmentation.Topico']", 'null': 'True', 'blank': 'True'}),
            'users_are_comment': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'items_comentados'", 'symmetrical': 'False', 'through': "orm['items.Comentario']", 'to': "orm['auth.User']"})
        },
        'items.recomendacion': {
            'Meta': {'object_name': 'Recomendacion'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['items.Item']"}),
            'user_destino': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recomendaciones_recibidas'", 'to': "orm['auth.User']"}),
            'user_origen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recomendaciones_enviadas'", 'to': "orm['auth.User']"})
        },
        'segmentation.topico': {
            'Meta': {'object_name': 'Topico'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['segmentation.Topico']", 'null': 'True', 'blank': 'True'})
        },
        'social.actividad': {
            'Meta': {'object_name': 'Actividad'},
            'comentario': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_coment'", 'null': 'True', 'blank': 'True', 'to': "orm['items.Comentario']"}),
            'descripcion': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_item'", 'null': 'True', 'blank': 'True', 'to': "orm['items.Item']"}),
            'recomendacion': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_recom'", 'null': 'True', 'blank': 'True', 'to': "orm['items.Recomendacion']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'usuario_destino': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_destino'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'usuario_origen': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_origen'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'social.consulta': {
            'Meta': {'object_name': 'Consulta'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mensaje': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas_enviadas'", 'to': "orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas_recibidas'", 'to': "orm['auth.User']"})
        },
        'social.evento': {
            'Meta': {'object_name': 'Evento'},
            'creador': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventos_creados'", 'to': "orm['auth.User']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha_creacion': ('django.db.models.fields.DateField', [], {}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'default': "'images/calendario-default.png'", 'max_length': '100'}),
            'invitados': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'eventos_invitado'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'localizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['support.Localizacion']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'default': "'Nombre'", 'max_length': '30'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': "orm['social.TipoEvento']", 'null': 'True', 'blank': 'True'})
        },
        'social.mensaje': {
            'Meta': {'object_name': 'Mensaje'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mensaje': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mensajes_enviados'", 'to': "orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mensajes_recibidos'", 'to': "orm['auth.User']"})
        },
        'social.notificacion': {
            'Meta': {'object_name': 'Notificacion'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notificaciones_enviadas'", 'to': "orm['auth.User']"}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_desde': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_expiracion': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'usuarios_to': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notificaciones_recibidas'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'social.tipoevento': {
            'Meta': {'object_name': 'TipoEvento'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
        }
    }

    complete_apps = ['social']
