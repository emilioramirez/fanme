from django.db import models
from fanme.segmentation.models import Topico
from django.contrib.auth.models import User


class Item(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=300)
    topico = models.ForeignKey(Topico, null=True, blank=True)
    users_are_comment = models.ManyToManyField(User, through='Comentario')
    users_recomendation = models.ManyToManyField(User, through='Recomendacion',
        related_name='recomendaciones_recibidas')

    def __unicode__(self):
        return self.nombre


class Marca(models.Model):
    pass


class Comentario(models.Model):
    comentario = models.TextField(max_length=300)
    fecha = models.DateTimeField()
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)


class Recomendaciones(models.Model):
    user_origen = models.OneToOneField(User)

    def __unicode__(self):
        return u'De {0}'.format(self.user_origen)

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Recomendaciones por usuario"


class Recomendacion(models.Model):
    item = models.ForeignKey(Item)
    user_destino = models.ForeignKey(User)
    fecha = models.DateTimeField()
    user_origen = models.ForeignKey(Recomendaciones)

    def __unicode__(self):
        return u'{0} para {1} sobre {2}'.format(self.user_origen,
            self.user_destino, self.item)

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Recomendaciones"
