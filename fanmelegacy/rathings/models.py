from django.dispatch import Signal
from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _



class BaseRating(models.Model):
    """
     An abstract base class that any custom rating models probably should
    subclass.
    """
    content_type = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Like(BaseRating):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                    blank=True, null=True, related_name="%(class)s_likes")
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date_created',)
        verbose_name = _('Me gusta')
        verbose_name_plural = _('Me gusta')


class Dislike(BaseRating):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                    blank=True, null=True, related_name="%(class)s_dislikes")
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date_created',)
        verbose_name = _('Denuncia')
        verbose_name_plural = _('Denuncias')


dislike_created = Signal(providing_args=["instance",])
