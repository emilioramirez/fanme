# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemImagen'
        db.create_table(u'core_itemimagen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mis_imagenes', to=orm['core.Item'])),
            ('imagen', self.gf('core.thumbs.ImageWithThumbsField')(default='items/default.png', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['ItemImagen'])


    def backwards(self, orm):
        # Deleting model 'ItemImagen'
        db.delete_table(u'core_itemimagen')


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
        u'core.actividad': {
            'Meta': {'object_name': 'Actividad'},
            'descripcion': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_item'", 'null': 'True', 'blank': 'True', 'to': u"orm['core.Item']"}),
            'recomendacion': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_recom'", 'null': 'True', 'blank': 'True', 'to': u"orm['core.Recomendacion']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'usuario_destino': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_destino'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'usuario_origen': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'act_origen'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'core.consulta': {
            'Meta': {'object_name': 'Consulta'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mis_consultas'", 'to': u"orm['core.Item']"}),
            'mensaje': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas_enviadas'", 'to': u"orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas_recibidas'", 'to': u"orm['auth.User']"})
        },
        u'core.credibilidad': {
            'Meta': {'object_name': 'Credibilidad'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.denuncia': {
            'Meta': {'object_name': 'Denuncia'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'fecha_denuncia': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_resolucion': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.evento': {
            'Meta': {'object_name': 'Evento'},
            'creador': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventos_creados'", 'to': u"orm['auth.User']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha_creacion': ('django.db.models.fields.DateField', [], {}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'default': "'images/calendario-default.png'", 'max_length': '100'}),
            'invitados': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'eventos_invitado'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'localizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Localizacion']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'default': "'Nombre'", 'max_length': '30'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['core.TipoEvento']", 'null': 'True', 'blank': 'True'})
        },
        u'core.item': {
            'Meta': {'object_name': 'Item'},
            'cantidad_fans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topico': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Topico']", 'null': 'True', 'blank': 'True'})
        },
        u'core.itemimagen': {
            'Meta': {'object_name': 'ItemImagen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('core.thumbs.ImageWithThumbsField', [], {'default': "'items/default.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mis_imagenes'", 'to': u"orm['core.Item']"})
        },
        u'core.localidad': {
            'Meta': {'object_name': 'Localidad'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Provincia']"})
        },
        u'core.localizacion': {
            'Meta': {'object_name': 'Localizacion'},
            'barrio': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Localidad']"}),
            'numero': ('django.db.models.fields.IntegerField', [], {}),
            'numero_local': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.notificacion': {
            'Meta': {'object_name': 'Notificacion'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resumen': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '50'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TipoNotificacion']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notif_recibidas'", 'to': u"orm['auth.User']"})
        },
        u'core.notificacionempresa': {
            'Meta': {'object_name': 'NotificacionEmpresa'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notificaciones_enviadas'", 'to': u"orm['auth.User']"}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_desde': ('django.db.models.fields.DateTimeField', [], {}),
            'fecha_expiracion': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'usuarios_to': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notificaciones_recibidas'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'core.pais': {
            'Meta': {'object_name': 'Pais'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'core.plan': {
            'Meta': {'object_name': 'Plan'},
            'cant_items': ('django.db.models.fields.IntegerField', [], {}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'fecha_creacion': ('django.db.models.fields.DateField', [], {}),
            'fecha_fin_vigencia': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio_vigencia': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'core.provincia': {
            'Meta': {'object_name': 'Provincia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pais']"})
        },
        u'core.recomendacion': {
            'Meta': {'object_name': 'Recomendacion'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Item']"}),
            'user_destino': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recomendaciones_recibidas'", 'to': u"orm['auth.User']"}),
            'user_origen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recomendaciones_enviadas'", 'to': u"orm['auth.User']"})
        },
        u'core.rubro': {
            'Meta': {'object_name': 'Rubro'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'core.tipoevento': {
            'Meta': {'object_name': 'TipoEvento'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'core.tiponotificacion': {
            'Meta': {'object_name': 'TipoNotificacion'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'core.topico': {
            'Meta': {'object_name': 'Topico'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Topico']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']