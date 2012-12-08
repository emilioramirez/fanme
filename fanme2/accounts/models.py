from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class ProfileBase(models.Model):
    CHOICE_SEX = (
        ('M', _('Masculino')),
        ('F', _('Femenino')),
    )
    user = models.OneToOneField(User, related_name='%(class)s',
        verbose_name=_('Usuario'), unique=True,)
    is_first_time = models.BooleanField(_('primer ingreso'))
    fecha_nacimiento = models.DateField(_('fecha de nacimiento'))
    sexo = models.CharField(_('sexo'), max_length=20,
        choices=CHOICE_SEX)
    avatar = models.ImageField(_('imagen de perfil'), upload_to='avatars',
        default='avatars/default.jpg')

    def __unicode__(self):
        return u'{0} {1} <{2}>'.format(self.user.username,
            self.user.first_name,
            self.user.last_name)

    class Meta:
        verbose_name = _('perfil de usuario')
        verbose_name_plural = _('perfiles de usuarios')
