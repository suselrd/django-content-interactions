# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stats'
        db.create_table(u'content_interactions_stats_stats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('likes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ratings', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_5_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_4_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_3_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_2_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_1_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('favorite_marks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('shares', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('denounces', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_stats', to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'content_interactions_stats', ['Stats'])

        # Adding unique constraint on 'Stats', fields ['content_type', 'object_pk']
        db.create_unique(u'content_interactions_stats_stats', ['content_type_id', 'object_pk'])


    def backwards(self, orm):
        # Removing unique constraint on 'Stats', fields ['content_type', 'object_pk']
        db.delete_unique(u'content_interactions_stats_stats', ['content_type_id', 'object_pk'])

        # Deleting model 'Stats'
        db.delete_table(u'content_interactions_stats_stats')


    models = {
        u'content_interactions_stats.stats': {
            'Meta': {'unique_together': "(('content_type', 'object_pk'),)", 'object_name': 'Stats'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_stats'", 'to': u"orm['contenttypes.ContentType']"}),
            'denounces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'favorite_marks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'rating_1_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_2_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_3_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_4_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_5_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ratings': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shares': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['content_interactions_stats']