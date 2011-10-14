from django.db import models
from django.contrib.auth.models import User
from fanme.support.models import Localizacion


class Eventos(models.Model):
    creador = models.OneToOneField(User)


class Evento(models.Model):
    invitados = models.ManyToManyField(User, null=True, blank=True)
    descripcion = models.TextField(max_length=300)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    fecha_creacion = models.DateTimeField()
    localizacion = models.ForeignKey(Localizacion)
    creador = models.ForeignKey(Eventos)


class Mensaje(models.Model):
    user_to = models.ForeignKey(User, related_name='mensajes_recibidos')
    user_from = models.ForeignKey(User, related_name='mensajes_enviados')
    mensaje = models.TextField(max_length=300)
    fecha = models.DateTimeField()


class Notificacion(models.Model):
    empresa = models.ForeignKey(User, related_name='notificaciones_enviadas')
    usuarios_to = models.ManyToManyField(User, null=True, blank=True,
        related_name='notificaciones_recibidas')
    fecha_expiracion = models.DateTimeField()
    fecha_creacion = models.DateTimeField()
    #estado -> Estado_Noficiacion
