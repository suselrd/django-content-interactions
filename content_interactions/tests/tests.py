# coding=utf-8
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from social_graph import Graph


class TestContentInteractions(TestCase):

    def setUp(self):

        from models import A

        self.user = User.objects.create_user(username='user', password='pass')
        self.object, created = A.objects.get_or_create(name='a1')
        Graph().clear_cache()

    def test_visits(self):
        c = Client()
        logged_in = c.login(username='user', password='pass')
        self.assertTrue(logged_in)

        response = c.get(reverse('detail', kwargs={
            'pk': self.object.pk
        }))
        self.assertEqual(response.status_code, 200)
        self.assertIn('object', response.context_data)

        from content_interactions_stats.models import Stats
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.visits, 1)

    def test_shares(self):
        c = Client()
        logged_in = c.login(username='user', password='pass')
        self.assertTrue(logged_in)

        response = c.post(reverse('share_item'), data={
            'content_type': ContentType.objects.get_for_model(self.object).pk,
            'object_pk': self.object.pk,
            'addressee': 'suselrd@gmail.com'
        })
        self.assertEqual(response.status_code, 200)

        from content_interactions_stats.models import Stats
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.shares, 1)

    def test_likes(self):
        c = Client()
        logged_in = c.login(username='user', password='pass')
        self.assertTrue(logged_in)

        response = c.post(reverse('like_item'), data={
            'model': 'content_interactions.tests.models.A', 'pk': self.object.pk
        })
        self.assertEqual(response.status_code, 200)

        from content_interactions_stats.models import Stats
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.likes, 1)

        response = c.post(reverse('like_item'), data={
            'model': 'content_interactions.tests.models.A', 'pk': self.object.pk
        })
        self.assertEqual(response.status_code, 200)
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.likes, 0)

    def test_favorites(self):
        c = Client()
        logged_in = c.login(username='user', password='pass')
        self.assertTrue(logged_in)

        response = c.post(reverse('favorite_item'), data={
            'model': 'content_interactions.tests.models.A', 'pk': self.object.pk
        })
        self.assertEqual(response.status_code, 200)

        from content_interactions_stats.models import Stats
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.favorite_marks, 1)

        response = c.post(reverse('favorite_item'), data={
            'model': 'content_interactions.tests.models.A', 'pk': self.object.pk
        })
        self.assertEqual(response.status_code, 200)
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.favorite_marks, 0)

    def test_denounces(self):
        c = Client()
        logged_in = c.login(username='user', password='pass')
        self.assertTrue(logged_in)

        response = c.post(reverse('denounce_item'), data={
            'content_type': ContentType.objects.get_for_model(self.object).pk,
            'object_pk': self.object.pk,
            'comment': 'this is bad content'
        })
        self.assertEqual(response.status_code, 200)

        from content_interactions_stats.models import Stats
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.denounces, 1)

        response = c.post(reverse('denounce_item'), data={
            'content_type': ContentType.objects.get_for_model(self.object).pk,
            'object_pk': self.object.pk
        })
        self.assertEqual(response.status_code, 200)
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.denounces, 0)

    def test_ratings(self):
        c = Client()
        logged_in = c.login(username='user', password='pass')
        self.assertTrue(logged_in)

        response = c.post(reverse('rate_item'), data={
            'content_type': ContentType.objects.get_for_model(self.object).pk,
            'object_pk': self.object.pk,
            'rating': 5
        })
        self.assertEqual(response.status_code, 200)

        from content_interactions_stats.models import Stats
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.ratings, 1)
        self.assertEqual(obj_stats.rating_5_count, 1)
        self.assertEqual(obj_stats.rating, 5.0)

        response = c.post(reverse('rate_item'), data={
            'content_type': ContentType.objects.get_for_model(self.object).pk,
            'object_pk': self.object.pk,
            'rating': 4
        })
        self.assertEqual(response.status_code, 200)
        obj_stats = Stats.objects.get(content_type=ContentType.objects.get_for_model(self.object), object_pk=self.object.pk)
        self.assertEqual(obj_stats.ratings, 1)
        self.assertEqual(obj_stats.rating_5_count, 0)
        self.assertEqual(obj_stats.rating_4_count, 1)
        self.assertEqual(obj_stats.rating, 4.0)

    def test_stats_property(self):
        self.assertIsNotNone(self.object.stats)

    def test_visits_monitoring(self):
        c = Client()
        logged_in = c.login(username='user', password='pass')
        self.assertTrue(logged_in)

        self.assertEqual(self.object.activity_records.count(), 0)

        response = c.get(reverse('detail', kwargs={
            'pk': self.object.pk
        }))
        self.assertEqual(response.status_code, 200)
        self.assertIn('object', response.context_data)

        self.assertEqual(self.object.activity_records.count(), 1)
        self.assertEqual(self.object.activity_records.current().count(), 1)

        current = self.object.activity_records.current()
        users = [record.user for record in current]
        self.assertIn(self.user, users)

        response = c.get(reverse('activity'), data={
            'model': 'content_interactions.tests.models.A', 'pk': self.object.pk
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('activity_records', response.context_data)
        self.assertEqual(response.context_data['activity_records'].count(), 1)
        self.assertEqual(response.context_data['activity_records'].first().user, self.user)

    def test_activity_records_property(self):
        self.assertIsNotNone(self.object.activity_records)
