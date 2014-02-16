# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Plan'
        db.create_table(u'bussiness_plan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(default='Empty', max_length=30)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(default='Empty', max_length=300)),
            ('cant_items', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateField')(default='01/01/1970')),
            ('fecha_inicio_vigencia', self.gf('django.db.models.fields.DateField')(default='01/01/1970')),
            ('fecha_fin_vigencia', self.gf('django.db.models.fields.DateField')(default='01/01/1970')),
            ('precio', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'bussiness', ['Plan'])

        # Adding model 'PlanXEmpresa'
        db.create_table(u'bussiness_planxempresa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plan_empresa', to=orm['auth.User'])),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plan_elegido', to=orm['bussiness.Plan'])),
            ('fecha_inicio_vigencia', self.gf('django.db.models.fields.DateField')()),
            ('fecha_fin_vigencia', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'bussiness', ['PlanXEmpresa'])

        # Adding M2M table for field item on 'PlanXEmpresa'
        m2m_table_name = db.shorten_name(u'bussiness_planxempresa_item')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('planxempresa', models.ForeignKey(orm[u'bussiness.planxempresa'], null=False)),
            ('item', models.ForeignKey(orm[u'items.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['planxempresa_id', 'item_id'])


    def backwards(self, orm):
        # Deleting model 'Plan'
        db.delete_table(u'bussiness_plan')

        # Deleting model 'PlanXEmpresa'
        db.delete_table(u'bussiness_planxempresa')

        # Removing M2M table for field item on 'PlanXEmpresa'
        db.delete_table(db.shorten_name(u'bussiness_planxempresa_item'))


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
        u'bussiness.plan': {
            'Meta': {'object_name': 'Plan'},
            'cant_items': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'default': "'Empty'", 'max_length': '300'}),
            'fecha_creacion': ('django.db.models.fields.DateField', [], {'default': "'01/01/1970'"}),
            'fecha_fin_vigencia': ('django.db.models.fields.DateField', [], {'default': "'01/01/1970'"}),
            'fecha_inicio_vigencia': ('django.db.models.fields.DateField', [], {'default': "'01/01/1970'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'default': "'Empty'", 'max_length': '30'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'})
        },
        u'bussiness.planxempresa': {
            'Meta': {'object_name': 'PlanXEmpresa'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plan_empresa'", 'to': u"orm['auth.User']"}),
            'fecha_fin_vigencia': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio_vigencia': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'enlaces_externos'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['items.Item']"}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plan_elegido'", 'to': u"orm['bussiness.Plan']"})
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
        u'segmentation.topico': {
            'Meta': {'object_name': 'Topico'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['segmentation.Topico']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bussiness']