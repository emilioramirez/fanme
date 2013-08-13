from django.db import models
from django.contrib.auth.models import User
from items.models import Item


class Plan(models.Model):
    nombre = models.CharField(max_length=30, default='Empty')
    descripcion = models.CharField(max_length=300, default='Empty')
    cant_items = models.IntegerField(default=0)
    fecha_creacion = models.DateField(default='01/01/1970')
    fecha_inicio_vigencia = models.DateField(default='01/01/1970')
    fecha_fin_vigencia = models.DateField(default='01/01/1970')
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
 #        verbose_name = ''
        verbose_name_plural = "Planes"

    def __unicode__(self):
        return self.nombre


class PlanXEmpresa(models.Model):
    empresa = models.ForeignKey(User)
    plan = models.ForeignKey(Plan, related_name='plan_elegido')
    fecha_inicio_vigencia = models.DateField()
    fecha_fin_vigencia = models.DateField()
    item = models.ManyToManyField(Item, null=True, blank=True,
        related_name="enlaces_externos")

    def __init__(self):
        models.Model.__init__(self)
