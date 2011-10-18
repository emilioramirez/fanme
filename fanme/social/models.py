from django.db import models
from django.contrib.auth.models import User
from fanme.support.models import Localizacion


class Eventos(models.Model):
    creador = models.OneToOneField(User)

    def __unicode__(self):
        return self.creador.username


class Evento(models.Model):
    invitados = models.ManyToManyField(User, null=True, blank=True,
        related_name="eventos_invitado")
    descripcion = models.TextField(max_length=300)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_creacion = models.DateField()
    localizacion = models.ForeignKey(Localizacion)
    creador = models.ForeignKey(User, related_name="eventos_creados")

    def __unicode__(self):
        return self.descripcion


class Mensaje(models.Model):
    user_to = models.ForeignKey(User, related_name='mensajes_recibidos')
    user_from = models.ForeignKey(User, related_name='mensajes_enviados')
    mensaje = models.TextField(max_length=300)
    fecha = models.DateTimeField()

    def __unicode__(self):
        return self.mensaje


class Notificacion(models.Model):
    empresa = models.ForeignKey(User, related_name='notificaciones_enviadas')
    usuarios_to = models.ManyToManyField(User, null=True, blank=True,
        related_name='notificaciones_recibidas')
    fecha_expiracion = models.DateTimeField()
    fecha_creacion = models.DateTimeField()
    #estado -> Estado_Noficiacion
