from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from support.models import Rubro
from segmentation.models import Topico, AnalisisDenuncia, EstadoAnalisisDenuncia
from items.models import Item, ItemDenuncias
from fanmelegacy.thumbs import ImageWithThumbsField
from rathings.models import dislike_created, Dislike
from django.db.models.signals import post_save


# Create your models here.
class AbstractProfile(models.Model):
    #Mandatory field
    user = models.OneToOneField(User, related_name='%(class)s',
        verbose_name=u'Django user', unique=True,)
    #Common fields
    #rol = models.TextField()
    #credibilidad = models.OneToOneField(Credibilidad)
    topicos = models.ManyToManyField(Topico, null=True, blank=True)
    is_first_time = models.BooleanField()
    avatar = ImageWithThumbsField(upload_to='avatares',
#    avatar = models.ImageField(upload_to='avatares',
        default='',
        sizes=((50, 50), (100, 100)),
        null=True, blank=True)

    class Meta:
        abstract = True
#        verbose_name = ''
#        verbose_name_plural = "stories"

    def __unicode__(self):
        return u'{0} {1} <{2}>'.format(self.user.first_name,
            self.user.last_name, self.user.username)

    def cantidad_estrellas(self):
        """
        La cantidad de estrellas se define por:
            - 2 * cantidad de items de los cuales es fan
            - 2 * cantidad de me gustas a comentarios
            - 1 * cantidad de topicos creados
            - 5 * cantidad de analisis de denuncias con accion borrado de un comentario relacionado con el user
            -10 * cantidad de analisis de denuncias con accion borrado de un item relacionado con el usuario
            - 
        """
        cantidad_items_fan = self.items.all().count()

        comment_ctype = ContentType.objects.get(app_label='comments', model="comment")
        cantidad_me_gusta_comentarios = self.user.like_likes.filter(content_type=comment_ctype).count()

        # estado_analisis_denuncia_borrado = EstadoAnalisisDenuncia.objects.get_or_create(estado="borrado")
        # cantidad_analisis_denuncia_borrado_comentario = ""
        
        v = settings.PUNTAJES
        e = settings.ESTRELLAS
        puntaje = v["item_fan"] * cantidad_items_fan + v["comment_like"] * cantidad_me_gusta_comentarios
        estrellas = 0
        if puntaje <= e["1"]:
            estrellas = 1
        elif puntaje <= e["2"]:
            estrellas = 2
        elif puntaje <= e["3"]:
            estrellas = 3
        elif puntaje <= e["4"]:
            estrellas = 4
        else:
            estrellas = 5
        return range(estrellas)


class Persona(AbstractProfile):
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=20)
    items = models.ManyToManyField(Item, null=True, blank=True)
    following = models.ManyToManyField(User, null=True, blank=True,
        related_name='followers')

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Personas"


class Empresa(AbstractProfile):
    razon_social = models.CharField(max_length=40)
    rubros = models.ManyToManyField(Rubro)
    site = models.URLField()

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Empresas"


def analisis_denuncias(sender, **kwargs):
    """
    Crear analisis de denuncia si:
        si cantidad de denuncias es mayor o igual a la configuracion
    Datos:
        fecha_creacion - se instancia automaticamente
        fecha_resolucion - se instancia automaticamente
        moderador - Deberia se uno random
        descripcion - vacia
        estado - creado
        content_type - el contenttype que represena al objeto referenciado
        object_id - el id del objeto
    """
    ctype = kwargs['instance'].content_type
    object_id = kwargs['instance'].object_id
    qs = Dislike.objects.filter(content_type=ctype, object_id=object_id)
    cant_denuncias = qs.count()
    if cant_denuncias >= settings.CANTIDAD_DENUNCIAS:
        estado, created_e = EstadoAnalisisDenuncia.objects.get_or_create(
            estado="creado", descripcion="Denuncia creada")
        a_denuncia = AnalisisDenuncia()
        a_denuncia.estado = estado
        a_denuncia.content_type = ctype
        a_denuncia.object_id = object_id
        a_denuncia.save()


# def analisis_denuncias_viejo(sender, instance, created, raw, using, update_fields, **kwargs):
#     ctype = ContentType.objects.get(app_label="items", model="item")
#     object_id = instance.item.pk
#     qs = ItemDenuncias.objects.filter(item=instance.item)
#     cant_denuncias = qs.count()
#     if cant_denuncias >= settings.CANTIDAD_DENUNCIAS:
#         estado, created_e = EstadoAnalisisDenuncia.objects.get_or_create(
#             estado="creado", descripcion="Denuncia creada")
#         a_denuncia = AnalisisDenuncia()
#         a_denuncia.estado = estado
#         a_denuncia.content_type = ctype
#         a_denuncia.object_id = object_id
#         a_denuncia.save()

dislike_created.connect(analisis_denuncias)
# post_save.connect(analisis_denuncias_viejo, sender=ItemDenuncias)