from django.db import models
from django.contrib.auth.models import User
from fanme.support.models import Rubro
from fanme.segmentation.models import Topico
from fanme.items.models import Item


# Create your models here.
class AbstractProfile(models.Model):
    #Mandatory field
    user = models.OneToOneField(User, related_name='%(class)s',
        verbose_name=u'Django user', unique=True,)
    #Common fields
    #rol = models.TextField()
    #credibilidad = models.OneToOneField(Credibilidad)
    #buzon = models.OneToOneField(Buzon)
    #evento = models.OneToOneField(Evento)
    #localizacion = models.OneToOneField(Localizacion)
    #imagen = models.ImageField(blank=True)
    topicos = models.ManyToManyField(Topico, null=True, blank=True)
    is_first_time = models.BooleanField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return 'Perfil de {0}'.format(self.user.username)


class Persona(AbstractProfile):
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=20)
    items = models.ManyToManyField(Item, null=True, blank=True)
    following = models.ManyToManyField(User, null=True, blank=True,
        related_name='followers')


class Empresa(AbstractProfile):
    razon_social = models.CharField(max_length=40)
    rubros = models.ManyToManyField(Rubro)
    site = models.URLField(verify_exists=False)
