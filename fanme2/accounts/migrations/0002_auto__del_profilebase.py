# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ProfileBase'
        db.delete_table('accounts_profilebase')


    def backwards(self, orm):
        
        # Adding model 'ProfileBase'
        db.create_table('accounts_profilebase', (
            ('fecha_nacimiento', self.gf('django.db.models.fields.DateField')()),
            ('is_first_time', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sexo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(default='default.jpg', max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profilebase', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('accounts', ['ProfileBase'])


    models = {
        
    }

    complete_apps = ['accounts']
