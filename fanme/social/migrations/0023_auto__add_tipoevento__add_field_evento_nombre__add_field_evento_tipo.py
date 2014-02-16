# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TipoEvento'
        db.create_table('social_tipoevento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('social', ['TipoEvento'])

        # Adding field 'Evento.nombre'
        db.add_column('social_evento', 'nombre', self.gf('django.db.models.fields.CharField')(default='Nombre', max_length=30), keep_default=False)

        # Adding field 'Evento.tipo'
        db.add_column('social_evento', 'tipo', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['social.TipoEvento'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'TipoEvento'
        db.delete_table('social_tipoevento')

        # Deleting field 'Evento.nombre'
        db.delete_column('social_evento', 'nombre')

        # Deleting field 'Evento.tipo'
        db.delete_column('social_evento', 'tipo_id')


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
        'social.consulta': {
            'Meta': {'object_name': 'Consulta'},
            'estado': ('django.db.models.fields.CharField', [], {'default': "'noleido'", 'max_length': '30'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mensaje': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas_enviados'", 'to': "orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas_recibidos'", 'to': "orm['auth.User']"})
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
