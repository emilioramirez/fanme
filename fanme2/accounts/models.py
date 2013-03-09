from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class ProfileBase(models.Model):
    """
    All profiles must be inherit from this abstract class, this provide some
    some basic common data.
    """
    CHOICE_SEX = (
        ('M', _('Masculino')),
        ('F', _('Femenino')),
    )
    user = models.OneToOneField(User, related_name='%(class)s',
        verbose_name=_('Usuario'), unique=True,)
    first_login = models.BooleanField(_('Primer ingreso'))
    birthday = models.DateField(_('Fecha de nacimiento'))
    sex = models.CharField(_('Sexo'), max_length=20, choices=CHOICE_SEX)
    avatar = models.ImageField(_('Foto de perfil'), upload_to='avatars',
        default='avatars/default.jpg')

    def __unicode__(self):
        return u'{0} {1} <{2}>'.format(self.user.username,
            self.user.first_name,
            self.user.last_name)

    class Meta:
        abstract = True
