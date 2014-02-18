from django.db import models
from segmentation.models import Topico
from django.contrib.auth.models import User
from fanmelegacy.thumbs import ImageWithThumbsField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^fanmelegacy\.thumbs\.ImageWithThumbsField"])


class Item(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=300)
    topico = models.ForeignKey(Topico, null=True, blank=True)
    users_are_comment = models.ManyToManyField(User, through='Comentario',
        related_name="items_comentados")
    cantidad_fans = models.IntegerField(default=0, null=True, blank=True)
    #cantidad_recomendacion = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def first_image_little(self):
        try:
            itemimagen = self.mis_imagenes.latest('imagen')
            return itemimagen.imagen.url_50x50
        except:
            return 'no pibe'

    def first_image(self):
        try:
            itemimagen = self.mis_imagenes.latest('imagen')
            return itemimagen.imagen.url_100x100
        except:
            return 'no pibe'

    def first_image_big(self):
        try:
            itemimagen = self.mis_imagenes.latest('imagen')
            return itemimagen.imagen.url_200x200
        except:
            return 'no pibe'

    def cantidad_recomendaciones(self):
        return self.recomendacion_set.count()

    def cantidad_fans_from_qs(self):
        return self.fans_por_item.all().count()


class Marca(models.Model):
    pass


class Comentario(models.Model):
    comentario = models.TextField(max_length=300)
    fecha = models.DateTimeField()
    item = models.ForeignKey(Item, related_name="comentarios_recibidos")
    user = models.ForeignKey(User, related_name="comentarios_realizados")
    me_gusta = models.IntegerField(default=0, null=True, blank=True)
    denuncias = models.IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return u'{0} para {1}'.format(self.user,
            self.item)


class Recomendacion(models.Model):
    item = models.ForeignKey(Item)
    user_destino = models.ForeignKey(User,
        related_name="recomendaciones_recibidas")
    fecha = models.DateTimeField()
    user_origen = models.ForeignKey(User,
        related_name="recomendaciones_enviadas")
    estado = models.CharField(default="noleido", max_length=30)

    def __unicode__(self):
        return u'{0} para {1} sobre {2}'.format(self.user_origen,
            self.user_destino, self.item)

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Recomendaciones"


class ItemImagen(models.Model):
    item = models.ForeignKey(Item, related_name='mis_imagenes')
#    imagen = models.ImageField(
    imagen = ImageWithThumbsField(
        upload_to='items',
        default='items/default.png',
        sizes=((50, 50), (100, 100), (200, 200)),
        null=True, blank=True)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.item, self.imagen.name)

    def image_big(self):
        try:
            return self.imagen.url_200x200
        except:
            return 'no pibe'


class ItemDenuncias(models.Model):
    item = models.ForeignKey(Item, related_name="item_denunciado")
    user = models.ForeignKey(User, related_name="usuario_que_denuncia")

    def __unicode__(self):
        return u'{0} para {1}'.format(self.user,
            self.item)
