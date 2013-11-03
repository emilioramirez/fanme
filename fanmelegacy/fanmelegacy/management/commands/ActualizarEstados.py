from django.core.management.base import NoArgsCommand
from social.models import Evento, Notificacion
from datetime import date


class Command(NoArgsCommand):
    #help = "Print a cliche to the console."

    def handle_noargs(self, **options):
        #Actualiza todos los eventos al estado ocurrido
        eventos = Evento.objects.all()
        for evento in eventos:
            if date.today() > evento.fecha_fin:
                evento.estado = 'finalizado'
                evento.save()
        #Actualiza todas las notificaciones al estado ocurrido
        notificaciones = Notificacion.objects.all()
        for notificacion in notificaciones:
            if date.today() > evento.fecha_fin:
                notificacion.estado = 'finalizado'
                notificacion.save()
