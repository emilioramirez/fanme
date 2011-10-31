from django.db import models
from fanme.segmentation.models import Topico
from django.contrib.auth.models import User


class Item(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=300)
    topico = models.ForeignKey(Topico, null=True, blank=True)
    users_are_comment = models.ManyToManyField(User, through='Comentario')
    cantidad_fans = models.IntegerField(null=True, blank=True)
    #cantidad_recomendacion = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.nombre


class Marca(models.Model):
    pass


class Comentario(models.Model):
    comentario = models.TextField(max_length=300)
    fecha = models.DateTimeField()
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    me_gusta = models.IntegerField(null=True, blank=True)
    denuncias = models.IntegerField(null=True, blank=True)


class Recomendacion(models.Model):
    item = models.ForeignKey(Item)
    user_destino = models.ForeignKey(User,
        related_name="recomendaciones_recibidas")
    fecha = models.DateTimeField()
    user_origen = models.ForeignKey(User,
        related_name="recomendaciones_enviadas")

    def __unicode__(self):
        return u'{0} para {1} sobre {2}'.format(self.user_origen,
            self.user_destino, self.item)

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Recomendaciones"


class ItemImagen(models.Model):
    item = models.ForeignKey(Item, related_name='mis_imagenes')
    imagen = models.ImageField(
        #ImageWithThumbsField(
        upload_to='items',
#    avatar = models.ImageField(upload_to='avatares',
        default='avatares/default.png',
#        sizes=((50, 50), (100, 100)),
        null=True, blank=True)
