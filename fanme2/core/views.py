from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from core.forms import ItemRegisterForm
from core.models import Item, Topico, ItemImagen


@login_required
def item(request):
    return render_to_response('core/item.html',
            context_instance=RequestContext(request))


@login_required
def create_item(request):
    messages = []
    if request.method == 'POST':
        form_register = ItemRegisterForm(request.POST, request.FILES)
        if form_register.is_valid():
            nombre = form_register.cleaned_data['nombre']
            descripcion = form_register.cleaned_data['descripcion']
            topico = form_register.cleaned_data['topico']
            item = Item()
            item.nombre = nombre
            item.descripcion = descripcion
            item.topico = Topico.objects.get(nombre=topico)
            item.cantidad_fans = 0
            item.save()
            try:
                imagen = request.FILES['imagen']
                itemimagen = ItemImagen()
                itemimagen.item = item
                itemimagen.imagen = imagen
                itemimagen.save()
            except KeyError:
                print 'Excepcion en items/view.register_item'
            messages.append("Se creo el Item exitosamente")
            form_register = ItemRegisterForm()
    else:
        form_register = ItemRegisterForm()
    return render_to_response('items/register_item.html',
        {'form_register': form_register,
        'messages': messages},
        context_instance=RequestContext(request))
