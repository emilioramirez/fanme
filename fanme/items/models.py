from django.db import models
from fanme.segmentation.models import Topico
from django.contrib.auth.models import User


class Item(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=300)
    topico = models.ForeignKey(Topico, null=True, blank=True)
    users_are_comment = models.ManyToManyField(User, through='Comentario')

    def __unicode__(self):
        return self.nombre


class Marca(models.Model):
    pass


class Comentario(models.Model):
    comentario = models.TextField(max_length=300)
    fecha = models.DateTimeField()
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
