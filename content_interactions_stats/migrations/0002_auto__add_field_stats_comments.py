# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Stats.comments'
        db.add_column(u'content_interactions_stats_stats', 'comments',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Stats.comments'
        db.delete_column(u'content_interactions_stats_stats', 'comments')


    models = {
        u'content_interactions_stats.stats': {
            'Meta': {'unique_together': "(('content_type', 'object_pk'),)", 'object_name': 'Stats'},
            'comments': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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