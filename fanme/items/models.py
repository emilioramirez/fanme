from django.db import models
from fanme.segmentation.models import Topico


class Item(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=300)
    topico = models.ForeignKey(Topico, null=True, blank=True)

    def __unicode__(self):
        return self.nombre


class Marca(models.Model):
    pass


class Comentario(models.Model):
    pass
