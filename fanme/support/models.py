from django.db import models


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


class Provincia(models.Model):
    nombre = models.CharField(max_length=20)
    pais = models.ForeignKey(Pais)

    def __unicode__(self):
        return self.nombre


class Localidad(models.Model):
    nombre = models.CharField(max_length=20)
    provincia = models.ForeignKey(Provincia)

    def __unicode__(self):
        return self.nombre


class Localizacion(models.Model):
    barrio = models.CharField(max_length=20)
    calle = models.CharField(max_length=20)
    numero = models.IntegerField()
    numero_local = models.IntegerField()
    localidad = models.ForeignKey(Localidad)

    def __unicode__(self):
        return self.barrio
