from django.db import models


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
