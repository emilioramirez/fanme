from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from support.models import Rubro
from segmentation.models import Topico, AnalisisDenuncia, EstadoAnalisisDenuncia
from items.models import Item
from fanmelegacy.thumbs import ImageWithThumbsField
from rathings.models import dislike_created, Dislike, Like


# Create your models here.
class AbstractProfile(models.Model):
    #Mandatory field
    user = models.OneToOneField(User, related_name='%(class)s',
        verbose_name=u'Django user', unique=True,)
    #Common fields
    topicos = models.ManyToManyField(Topico, null=True, blank=True)
    is_first_time = models.BooleanField()
    avatar = ImageWithThumbsField(upload_to='avatares',
        default='',
        sizes=((50, 50), (100, 100)),
        null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{0} {1} <{2}>'.format(self.user.first_name,
            self.user.last_name, self.user.username)

    def active_comments_count(self):
        return self.user.comment_comments.exclude(is_removed=True).count()



class Persona(AbstractProfile):
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=20)
    items = models.ManyToManyField(Item, null=True, blank=True)
    following = models.ManyToManyField(User, null=True, blank=True,
        related_name='followers')
    puntaje = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = "Personas"

    def cantidad_estrellas(self):
        cant_estrellas = self.get_cant_estrellas()
        return range(cant_estrellas)

    def get_cant_estrellas(self):
        """
        La cantidad de estrellas se define por:
            - 2 * cantidad de items de los cuales es fan
            - 2 * cantidad de me gustas que tienen mis comentarios
            - 1 * cantidad de topicos creados (no esta en uso)
            - 5 * cantidad de analisis de denuncias con accion borrado de un comentario relacionado con el user
            -10 * cantidad de analisis de denuncias con accion borrado de un item relacionado con el usuario
            -
        """
        e = settings.ESTRELLAS
        estrellas = 0
        if self.puntaje <= e["1"]:
            estrellas = 1
        elif self.puntaje <= e["2"]:
            estrellas = 2
        elif self.puntaje <= e["3"]:
            estrellas = 3
        elif self.puntaje <= e["4"]:
            estrellas = 4
        else:
            estrellas = 5
        return estrellas

    def set_puntaje(self):
        # Contar todos los items a los cuales estoy asociado mediante un fanme
        cantidad_items_fan = self.items.all().count()

        # De todos mis comentarios, cuantos likes suman en total
        mis_comentarios = self.user.comment_comments.all()
        cantidad_likes_comentarios = 0
        cantidad_analisdenuncias_borrados = 0
        estado, created_e = EstadoAnalisisDenuncia.objects.get_or_create(
            estado="borrado", descripcion="Se ha borrado el contenido asociado")
        for comentario in mis_comentarios:
            cantidad_likes_comentarios += Like.objects.get_for_obj(comentario).count()
            cantidad_analisdenuncias_borrados += AnalisisDenuncia.objects.filter(
            estado=estado, # es accion que se toma para esta denuncia
            content_type=ContentType.objects.get_for_model(comentario),
            object_id=comentario.pk,
            ).count()

        item_fan, comment_like, comment_denuncias = settings.PUNTAJES["item_fan"], settings.PUNTAJES["comment_like"], settings.PUNTAJES["comment_denuncias"]
        self.puntaje = ((item_fan * cantidad_items_fan) + (comment_like * cantidad_likes_comentarios) - (cantidad_analisdenuncias_borrados * comment_denuncias))
        self.save()

        return self.puntaje


class Empresa(AbstractProfile):
    razon_social = models.CharField(max_length=40)
    direccion = models.CharField(max_length=40, default="Sin direccion")
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

dislike_created.connect(analisis_denuncias)
