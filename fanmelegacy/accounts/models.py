from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from support.models import Rubro
from segmentation.models import Topico, AnalisisDenuncia, EstadoAnalisisDenuncia, AccionAnalisisDenuncia
from items.models import Item
from fanmelegacy.thumbs import ImageWithThumbsField
from rathings.models import dislike_created


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
        accion_tomada - ninguna
        estado - creado
        content_type - el contenttype que represena al objeto referenciado
        object_id - el id del objeto
    """
    ctype = kwargs['instance'].content_type
    object_id = kwargs['instance'].object_id
    qs = Dislike.objects.filter(content_type=ctype, object_id=object_id)
    cant_denuncias = qs.count()
    import pdb;pdb.set_trace()
    if cant_denuncias >= settings.CANTIDAD_DENUNCIAS:
        estado, created_e = EstadoAnalisisDenuncia.objects.get_or_create(
            estado="creado", descripcion="Denuncia creada")
        accion, created_c = AccionAnalisisDenuncia.objects.get_or_create(
            accion="ninguna", descripcion="No se ha tomado ninguna accion")
        a_denuncia = AnalisisDenuncia()
        a_denuncia.accion_tomada = accion
        a_denuncia.estado = estado
        a_denuncia.content_type = ctype
        a_denuncia.object_id = object_id
        a_denuncia.save()


dislike_created.connect(analisis_denuncias)