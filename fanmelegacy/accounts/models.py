from django.db import models
from django.contrib.auth.models import User
from support.models import Rubro
from segmentation.models import Topico
from items.models import Item
from fanmelegacy.thumbs import ImageWithThumbsField


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
