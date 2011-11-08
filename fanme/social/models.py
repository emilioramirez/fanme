from django.db import models
from django.contrib.auth.models import User
from fanme.support.models import Localizacion
from fanme.items.models import Item, Comentario, Recomendacion


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


class Mensaje(models.Model):
    user_to = models.ForeignKey(User, related_name='mensajes_recibidos')
    user_from = models.ForeignKey(User, related_name='mensajes_enviados')
    mensaje = models.TextField(max_length=300)
    fecha = models.DateTimeField()
    estado = models.CharField(default="noleido", max_length=30)

    def __unicode__(self):
        return self.mensaje


class Notificacion(models.Model):
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
    comentario = models.ForeignKey(Comentario, related_name="act_coment",
        default="", blank=True, null=True)
    usuario_origen = models.ForeignKey(User, related_name="act_origen",
        default="", blank=True, null=True)
    usuario_destino = models.ForeignKey(User, related_name="act_destino",
        default="", blank=True, null=True)
    fecha = models.DateTimeField()
    descripcion = models.CharField(default="", max_length=60)
    tipo = models.CharField(default="", max_length=30)
