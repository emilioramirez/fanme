from django.db import models
from django.contrib.auth.models import User


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


class Persona(AbstractProfile):
    fecha_nacimiento = models.DateField()
    sexo = models.TextField()


class Empresa(AbstractProfile):
    razon_social = models.TextField()
    #rubro = models.OneToOneField(Rubro)
    site = models.URLField(verify_exists=False)

