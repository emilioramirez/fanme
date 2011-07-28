from django.db import models
from django.contrib.auth.models import User
from fanme.soport.models import Rubro


# Create your models here.
class AbstractProfile(models.Model):
    #Mandatory field
    user = models.OneToOneField( User, related_name='%(class)s', verbose_name=u'Django user', unique=True,)
    #Common fields
    #rol = models.TextField()
    #credibilidad = models.OneToOneField(Credibilidad)
    #buzon = models.OneToOneField(Buzon)
    #evento = models.OneToOneField(Evento)
    #localizacion = models.OneToOneField(Localizacion)
    #imagen = models.ImageField(blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return 'Perfil de {0}'.format(self.user.username)


class Persona(AbstractProfile):
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=20)




class Empresa(AbstractProfile):
    razon_social = models.CharField(max_length=40)
    rubros = models.ManyToManyField(Rubro)
    site = models.URLField(verify_exists=False)

