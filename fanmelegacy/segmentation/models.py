from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Topico(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    padre = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        if (self.padre != None):
            return '{0} | {1}'.format(self.padre.__unicode__(), self.nombre)
        else:
            return self.nombre

        return self.nombre

# delete begins
class Tag(models.Model):
    pass


class Credibilidad(models.Model):
    pass

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Credibilidades"


class Denuncia(models.Model):
    fecha_denuncia = models.DateTimeField()
    fecha_resolucion = models.DateTimeField()
    descripcion = models.TextField(max_length=300)
# delete end

class AccionAnalisisDenuncia(models.Model):
    accion = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Accion de analisis de denuncia'
        verbose_name_plural = 'Accion de analisis de denuncias'

    def __unicode__(self):
        return self.accion
    

class EstadoAnalisisDenuncia(models.Model):
    estado = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Estado de analisis de denuncia'
        verbose_name_plural = 'Estado de analisis de denuncias'

    def __unicode__(self):
        return self.estado


class AnalisisDenuncia(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(auto_now=True)
    moderador = models.ForeignKey(User, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.ForeignKey(EstadoAnalisisDenuncia, verbose_name=u'Accion')
    content_type = models.ForeignKey(ContentType,
            verbose_name='Contenido denunciado',
            related_name="content_type_set_for_%(class)s")
    object_id = models.PositiveIntegerField('Id del contenido')
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('fecha_creacion',)
        verbose_name = "Analisis de denuncia"
        verbose_name_plural = "Analisis de denuncias"

    def __unicode__(self):
        return "Analisis de denuncia: {}".format(self.content_type)