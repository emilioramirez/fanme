from django.db import models
from django.contrib.auth.models import User
from .thumbs import ImageWithThumbsField


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


#TODO: Terminar de definir la clase Credibilidad del usuario.
class Credibilidad(models.Model):
    pass

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Credibilidades"


class Denuncia(models.Model):
    fecha_denuncia = models.DateTimeField()
    fecha_resolucion = models.DateTimeField()
    descripcion = models.TextField(max_length=300)


class Item(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=300)
    topico = models.ForeignKey(Topico, null=True, blank=True)
    cantidad_fans = models.IntegerField(default=0, null=True, blank=True)
    #TODO: acordarse de poner las realaciones necesarias para que el Item tenga
    #comentarios.
    #cantidad_recomendacion = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    #Manejo de imagenes
    def first_image_little(self):
        try:
            itemimagen = self.mis_imagenes.latest('imagen')
            return itemimagen.imagen.url_50x50
        except:
            return 'no pibe'

    #Manejo de imagenes
    def first_image(self):
        try:
            itemimagen = self.mis_imagenes.latest('imagen')
            return itemimagen.imagen.url_100x100
        except:
            return 'no pibe'

    #Manejo de imagenes
    def first_image_big(self):
        try:
            itemimagen = self.mis_imagenes.latest('imagen')
            return itemimagen.imagen.url_200x200
        except:
            return 'no pibe'

    def cantidad_recomendaciones(self):
        return self.recomendacion_set.count()


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


class Rubro(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre


class Pais(models.Model):
    nombre = models.CharField(max_length=20)

    def __unicode__(self):
        return self.nombre

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Paises"


class Provincia(models.Model):
    nombre = models.CharField(max_length=20)
    pais = models.ForeignKey(Pais)

    def __unicode__(self):
        return '{0}, {1}'.format(self.nombre, self.pais.__unicode__())


class Localidad(models.Model):
    nombre = models.CharField(max_length=20)
    provincia = models.ForeignKey(Provincia)

    def __unicode__(self):
        return '{0}, {1}'.format(self.nombre, self.provincia.__unicode__())

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Localidades"


class Localizacion(models.Model):
    barrio = models.CharField(max_length=20)
    calle = models.CharField(max_length=20)
    numero = models.IntegerField()
    numero_local = models.IntegerField()
    localidad = models.ForeignKey(Localidad)

    def __unicode__(self):
        return '{0} {1} {2}, {3} '.format(self.barrio, self.calle, self.numero,
            self.localidad.__unicode__())

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Localizaciones"


class TipoNotificacion(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Tipos de Notiticacion"


class Notificacion(models.Model):
    usuario = models.ForeignKey(User, related_name="notif_recibidas")
    descripcion = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoNotificacion)
    leido = models.BooleanField()
    resumen = models.CharField(default=False, max_length=50)

    def __unicode__(self):
        return self.resumen

    class Meta:
#        verbose_name = ''
        verbose_name_plural = "Notificaciones"


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre


class Evento(models.Model):
    invitados = models.ManyToManyField(User, null=True, blank=True,
        related_name="eventos_invitado")
    nombre = models.CharField(default="Nombre", max_length=30)
    descripcion = models.TextField(max_length=300)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_creacion = models.DateField()
    localizacion = models.ForeignKey(Localizacion)
    creador = models.ForeignKey(User, related_name="eventos_creados")
    estado = models.CharField(default="noleido", max_length=30)
    tipo = models.ForeignKey(TipoEvento, default="", null=True, blank=True)
    imagen = models.ImageField(default='images/calendario-default.png',
        upload_to="eventos")

    def __unicode__(self):
        return self.descripcion


class NotificacionEmpresa(models.Model):
    empresa = models.ForeignKey(User, related_name='notificaciones_enviadas')
    usuarios_to = models.ManyToManyField(User, null=True, blank=True,
        related_name='notificaciones_recibidas')
    fecha_expiracion = models.DateTimeField()
    fecha_creacion = models.DateTimeField()
    fecha_desde = models.DateTimeField()
    descripcion = models.TextField(max_length=300)
    nombre = models.CharField(max_length=30)
    estado = models.CharField(default="noleido", max_length=30)

    def __unicode__(self):
        return self.descripcion


class Consulta(models.Model):
    user_to = models.ForeignKey(User, related_name='consultas_recibidas')
    user_from = models.ForeignKey(User, related_name='consultas_enviadas')
    mensaje = models.TextField(max_length=300)
    fecha = models.DateTimeField()
    estado = models.CharField(default="noleido", max_length=30)
    item = models.ForeignKey(Item, related_name='mis_consultas')

    def __unicode__(self):
        return self.mensaje


class Actividad(models.Model):
    item = models.ForeignKey(Item, related_name="act_item", default="",
        blank=True, null=True)
    recomendacion = models.ForeignKey(Recomendacion, related_name="act_recom",
        default="", blank=True, null=True)
    #comentario = models.ForeignKey(Comentario, related_name="act_coment",
     #   default="", blank=True, null=True)
    usuario_origen = models.ForeignKey(User, related_name="act_origen",
        default="", blank=True, null=True)
    usuario_destino = models.ForeignKey(User, related_name="act_destino",
        default="", blank=True, null=True)
    fecha = models.DateTimeField()
    descripcion = models.CharField(default="", max_length=60)
    tipo = models.CharField(default="", max_length=30)


class Plan(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=300)
    cant_items = models.IntegerField()
    fecha_creacion = models.DateField()
    fecha_inicio_vigencia = models.DateField()
    fecha_fin_vigencia = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.nombre
