# coding=utf-8
import logging
from celery_instance import app

logger = logging.getLogger(__name__)


@app.task(name='content_interactions.social-networks-publish-action-message')
def social_networks_publish_action_message(message, content_type_pk, object_pk, user_pk, site_pk, social_network_ids,
                                           action, verb):
    try:
        from django.contrib.auth.models import User
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.sites.models import Site
        from django.utils.translation import ugettext as _
        from social_publisher.publisher import get_publisher
        from social_publisher.models import SocialNetwork
        from common.utils import social_network_share_app_name

        try:
            content_object = ContentType.objects.get(pk=content_type_pk).get_object_for_this_type(pk=object_pk)
            site = Site.objects.get(pk=site_pk)
            user = User.objects.get(pk=user_pk)

            social_networks = SocialNetwork.objects.filter(
                pk__in=social_network_ids,
                enabled=True,
                social_apps__socialtoken__account__user__id=user_pk,
            )

            publisher = get_publisher(user, False)
            domain = 'http://%s' % site.domain
            app_str = '%s - %s' % (site.name, social_network_share_app_name())
            link = content_object.get_absolute_url() if getattr(content_object, 'get_absolute_url', False) else content_object.get_url()
            if not link.startswith('http://') and not link.startswith('https://'):
                link = '%s%s' % (domain, link)

            action_info = {
                'link': link,
                'actor': user.get_full_name(),
                'action': action,
                'verb': verb,
                'target': content_object,
                'app': app_str,
                'domain': domain,
            }

            if content_object.get_picture():
                action_info.update({'picture': content_object.get_picture()})

            publisher.publish_action_message(
                instance=content_object,
                message=message,
                action_info=action_info,
                networks=social_networks,
            )

        except Exception as e:
            logger.exception(e.message)
    except ImportError:
        pass


@app.task(name='content_interactions.social-networks-publish-message')
def social_networks_publish_message(message, content_type_pk, object_pk, user_pk, site_pk, social_network_ids):
    try:
        from django.contrib.auth.models import User
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.sites.models import Site
        from django.utils.translation import ugettext as _
        from social_publisher.publisher import get_publisher
        from social_publisher.models import SocialNetwork
        from common.utils import social_network_share_app_name

        try:
            content_object = ContentType.objects.get(pk=content_type_pk).get_object_for_this_type(pk=object_pk)
            site = Site.objects.get(pk=site_pk)
            user = User.objects.get(pk=user_pk)

            social_networks = SocialNetwork.objects.filter(
                pk__in=social_network_ids,
                enabled=True,
                social_apps__socialtoken__account__user__id=user_pk,
            )

            publisher = get_publisher(user, False)
            domain = 'http://%s' % site.domain
            app_str = '%s - %s' % (site.name, social_network_share_app_name())
            link = content_object.get_absolute_url() if getattr(content_object, 'get_absolute_url', False) else content_object.get_url()
            if not link.startswith('http://') and not link.startswith('https://'):
                link = '%s%s' % (domain, link)

            action_info = {
                'link': link,
                'target': content_object,
                'app': app_str,
                'domain': domain,
            }

            if content_object.get_picture():
                action_info.update({'picture': content_object.get_picture()})

            publisher.publish_message(
                instance=content_object,
                message=message,
                action_info=action_info,
                networks=social_networks,
            )

        except Exception as e:
            logger.exception(e.message)
    except ImportError:
        pass