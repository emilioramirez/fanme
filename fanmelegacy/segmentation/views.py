# Create your views here.
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from segmentation.models import AnalisisDenuncia
from segmentation.forms import AnalisisDenunciaForm


class AnalisisDenunciaList(ListView):
    model = AnalisisDenuncia
    context_object_name = 'mis_denuncias_asignadas'

    def get_queryset(self):
        return AnalisisDenuncia.objects.filter(moderador=self.request.user)


class AnalisisDenunciaUpdate(UpdateView):
    model = AnalisisDenuncia
    form_class = AnalisisDenunciaForm

    def get_context_data(self, **kwargs):
        context = super(AnalisisDenunciaUpdate, self).get_context_data(**kwargs)
        context['object'] = self.object
        return context

    def form_valid(self, form):
        messages.success(self.request, "Se ha guardado correctamente")
        return super(AnalisisDenunciaUpdate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "NO se ha guardado correctamente, intente nuevamente.")
        return super(AnalisisDenunciaUpdate, self).form_valid(form)