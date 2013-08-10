# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Persona'
        db.create_table('accounts_persona', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='persona', unique=True, to=orm['auth.User'])),
            ('fecha_nacimiento', self.gf('django.db.models.fields.DateField')()),
            ('sexo', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('accounts', ['Persona'])

        # Adding M2M table for field topicos on 'Persona'
        db.create_table('accounts_persona_topicos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('persona', models.ForeignKey(orm['accounts.persona'], null=False)),
            ('topico', models.ForeignKey(orm['support.topico'], null=False))
        ))
        db.create_unique('accounts_persona_topicos', ['persona_id', 'topico_id'])

        # Adding model 'Empresa'
        db.create_table('accounts_empresa', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='empresa', unique=True, to=orm['auth.User'])),
            ('razon_social', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('site', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('accounts', ['Empresa'])

        # Adding M2M table for field topicos on 'Empresa'
        db.create_table('accounts_empresa_topicos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('empresa', models.ForeignKey(orm['accounts.empresa'], null=False)),
            ('topico', models.ForeignKey(orm['support.topico'], null=False))
        ))
        db.create_unique('accounts_empresa_topicos', ['empresa_id', 'topico_id'])

        # Adding M2M table for field rubros on 'Empresa'
        db.create_table('accounts_empresa_rubros', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('empresa', models.ForeignKey(orm['accounts.empresa'], null=False)),
            ('rubro', models.ForeignKey(orm['support.rubro'], null=False))
        ))
        db.create_unique('accounts_empresa_rubros', ['empresa_id', 'rubro_id'])


    def backwards(self, orm):
        
        # Deleting model 'Persona'
        db.delete_table('accounts_persona')

        # Removing M2M table for field topicos on 'Persona'
        db.delete_table('accounts_persona_topicos')

        # Deleting model 'Empresa'
        db.delete_table('accounts_empresa')

        # Removing M2M table for field topicos on 'Empresa'
        db.delete_table('accounts_empresa_topicos')

        # Removing M2M table for field rubros on 'Empresa'
        db.delete_table('accounts_empresa_rubros')


    models = {
        'accounts.empresa': {
            'Meta': {'object_name': 'Empresa'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'razon_social': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'rubros': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['support.Rubro']", 'symmetrical': 'False'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'topicos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['support.Topico']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'empresa'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'accounts.persona': {
            'Meta': {'object_name': 'Persona'},
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'topicos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['support.Topico']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'persona'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
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

    complete_apps = ['accounts']
