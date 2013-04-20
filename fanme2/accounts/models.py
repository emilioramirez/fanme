from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_activated
from django.utils.translation import ugettext_lazy as _


CHOICE_SEX = (
    ('M', _('Masculino')),
    ('F', _('Femenino')),
)


class Profile(models.Model):
    """
    All profiles must be inherit from this abstract class, this provide some
    some basic common data.
    """
    user = models.OneToOneField(User, related_name='%(class)s',
        verbose_name=_('Usuario'), unique=True,)
    first_login = models.BooleanField(_('Primer ingreso'), blank=True)
    avatar = models.ImageField(_('Foto de perfil'), upload_to='avatars',
        default='avatars/default.jpg')

    class Meta:
        verbose_name = _("Perfil base")
        verbose_name_plural = _("Perfiles base")

    def get_extra_profile(self):
        """
        If exist, return a ProfileUser or ProfileBusiness object related, if not
        return None
        """
        extra_profile = None
        try:
            extra_profile = self.profileuser
        except ProfileUser.DoesNotExist:
            #extra_profile =  self.profilebusiness
        #except ProfileBusiness.DoesNotExist:
            pass
        return extra_profile


class ProfileUser(Profile):
    """
    Profile for common user account
    """
    birthday = models.DateField(_('Fecha de nacimiento'))
    sex = models.CharField(_('Sexo'), max_length=20, choices=CHOICE_SEX)

    class Meta:
        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfiles")


def create_profile(sender, **kwargs):
    if (kwargs["user"]):
        print("crear el perfil del usuario") #o ver la posibilidad de mandar a alguna url que cree el tipo de usuario correspondiente...
    else:
        print("no crear nada")


user_activated.connect(create_profile)