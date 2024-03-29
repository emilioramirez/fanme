from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Rubro(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre


class Pais(models.Model):
    nombre = models.CharField(max_length=20)

    def __unicode__(self):
        return self.nombre

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Paises"


class Provincia(models.Model):
    nombre = models.CharField(max_length=20)
    pais = models.ForeignKey(Pais)

    def __unicode__(self):
        return '{0}, {1}'.format(self.nombre, self.pais.__unicode__())


class Localidad(models.Model):
    nombre = models.CharField(max_length=20)
    provincia = models.ForeignKey(Provincia)

    def __unicode__(self):
        return '{0}, {1}'.format(self.nombre, self.provincia.__unicode__())

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Localidades"


class Localizacion(models.Model):
    barrio = models.CharField(max_length=20)
    calle = models.CharField(max_length=20)
    numero = models.IntegerField()
    numero_local = models.IntegerField()
    localidad = models.ForeignKey(Localidad)

    def __unicode__(self):
        return '{0} {1} {2}, {3} '.format(self.barrio, self.calle, self.numero,
            self.localidad.__unicode__())

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Localizaciones"


class TipoNotificacion(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Tipos de Notiticacion"


class Notificacion(models.Model):
    usuario = models.ForeignKey(User, related_name="notif_recibidas")
    descripcion = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoNotificacion)
    leido = models.BooleanField()
    resumen = models.CharField(default=False, max_length=50)

    def __unicode__(self):
        return self.resumen

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Notificaciones"
