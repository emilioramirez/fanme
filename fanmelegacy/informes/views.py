from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from datetime import date
from segmentation.models import Topico
from items.models import Item
from collections import defaultdict
from django.utils.datastructures import SortedDict
from accounts.models import Persona
import collections

@staff_member_required
def my_admin_view(request):
    active_users = User.objects.filter(is_active=True)
    inactive_users = User.objects.filter(is_active=False)
    return render_to_response('informes/my_template.html',
        {'active_users': active_users.count(),
        'inactive_users': inactive_users.count()},
        context_instance=RequestContext(request))


@staff_member_required
def fans_por_topicos(request):
    topicos = Topico.objects.filter(padre=None)
    dict_topico = {}
    category_dict = defaultdict()
    for topico in topicos:
        item_dict = {}
        items_por_topico = Item.objects.filter(topico=topico)
        cant_fans = 0
        for item in items_por_topico:
            cant_fans = cant_fans + item.cantidad_fans
            item_dict[item] = item.cantidad_fans
        dict_topico[topico] = cant_fans
        category_dict[topico] = collections.Counter(item_dict).most_common(10)
    length = len(dict_topico)
    return render_to_response('informes/fans_por_topico.html',
        {'fans_por_topicos': dict_topico, 'length': length,
        'items_dict': category_dict},
        context_instance=RequestContext(request))


@staff_member_required
def fans_por_sub_topicos(request):
    nombre_padre_topico = request.GET.get('topico')
    topico = Topico.objects.get(nombre=nombre_padre_topico)
    topico_padre = topico.get_all_children()
    print topico_padre
    dict_topico = {}
    category_dict = defaultdict()
    for topico in topico_padre:
        item_dict = {}
        items_por_topico = Item.objects.filter(topico=topico)
        cant_fans = 0
        for item in items_por_topico:
            cant_fans = cant_fans + item.cantidad_fans
            item_dict[item] = item.cantidad_fans
        dict_topico[topico] = cant_fans
        category_dict[topico] = collections.Counter(item_dict).most_common(10)
    length = len(dict_topico)
    return render_to_response('informes/fans_por_subtopico.html',
        {'fans_por_topicos': dict_topico, 'length': length,
        'items_dict': category_dict},
        context_instance=RequestContext(request))


@staff_member_required
def item_fans(request):
    mostrar_form = True
    return render_to_response('informes/ranking_items.html',
        {'mostrar_form': mostrar_form},
        context_instance=RequestContext(request))


@staff_member_required
def cant_items_fans(request, cant_items):
    mostrar_form = False
    if cant_items != 0:
        top_items = Item.objects.order_by('-cantidad_fans')[:cant_items]
        dict = {}
        for item in top_items:
            dict[item] = item.cantidad_fans
    return render_to_response('informes/ranking_items.html',
        {'fans_por_item': dict, 'mostrar_form': mostrar_form},
        context_instance=RequestContext(request))


@staff_member_required
def progreso(request):
    mostrar_form = True
    return render_to_response('informes/progreso.html',
        {'fans_por_item': dict, 'mostrar_form': mostrar_form},
        context_instance=RequestContext(request))


@staff_member_required
def progreso_anios(request, cant_anios):
    mostrar_form = False
    current_year = date.today().year
    anios_a_restar = int(cant_anios)
    year_base = current_year - anios_a_restar
    anios = range(year_base, current_year + 1)
    dict = {}
    for year in anios:
        dict_cant = SortedDict()
        dict_cant['enero'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=1).count()
        dict_cant['febrero'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=2).count()
        dict_cant['marzo'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=3).count()
        dict_cant['abril'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=4).count()
        dict_cant['mayo'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=5).count()
        dict_cant['junio'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=6).count()
        dict_cant['julio'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=7).count()
        dict_cant['agosto'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=8).count()
        dict_cant['septiembre'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=9).count()
        dict_cant['octubre'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=10).count()
        dict_cant['noviembre'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=11).count()
        dict_cant['diciembre'] = Persona.objects.filter(user__date_joined__year=year).filter(
            user__date_joined__month=12).count()
        dict[year] = dict_cant
    return render_to_response('informes/progreso.html',
        {'dict': dict, 'mostrar_form': mostrar_form},
        context_instance=RequestContext(request))


@staff_member_required
def progreso_filtrado(request):
    anio = int(request.GET.get('anio'))
    mes = request.GET.get('mes')
    if mes == "Ene":
        usuarios = get_usuarios(anio, 1)
    elif mes == "Feb":
        usuarios = get_usuarios(anio, 2)
    elif mes == "Mar":
        usuarios = get_usuarios(anio, 3)
    elif mes == "Abr":
        usuarios = get_usuarios(anio, 4)
    elif mes == "May":
        usuarios = get_usuarios(anio, 5)
    elif mes == "Jun":
        usuarios = get_usuarios(anio, 6)
    elif mes == "Jul":
        usuarios = get_usuarios(anio, 7)
    elif mes == "Ago":
        usuarios = get_usuarios(anio, 8)
    elif mes == "Sep":
        usuarios = get_usuarios(anio, 9)
    elif mes == "Oct":
        usuarios = get_usuarios(anio, 10)
    elif mes == "Nov":
        usuarios = get_usuarios(anio, 11)
    elif mes == "Dec":
        usuarios = get_usuarios(anio, 12)
    sexo_femenino, sexo_masculino = get_sexo_count(usuarios)
    dict_cant = get_usuarios_por_rango_edad(usuarios)
    return render_to_response('informes/progreso_filtro.html',
        {'anio': anio, 'mes': mes,
        'usuarios': usuarios, 'sexo_femenino': sexo_femenino,
        'sexo_masculino': sexo_masculino, 'dict_cant': dict_cant},
        context_instance=RequestContext(request))


def get_usuarios(anio, mes):
    usuarios = Persona.objects.filter(user__date_joined__year=anio).filter(
            user__date_joined__month=mes)
    return usuarios


def informe_item_filtrado(request):
    item_id = int(request.GET.get('item_id'))
    item_seleccionado = Item.objects.get(pk=item_id)
    usuarios = item_seleccionado.fans_por_item.all()
    sexo_femenino, sexo_masculino = get_sexo_count(usuarios)
    dict_cant = get_usuarios_por_rango_edad(usuarios)
    return render_to_response('informes/ranking_items_detalle.html',
        {'usuarios': usuarios, 'sexo_femenino': sexo_femenino,
        'sexo_masculino': sexo_masculino, 'dict_cant': dict_cant},
        context_instance=RequestContext(request))



def get_sexo_count(usuarios):
    sexo_femenino = 0
    sexo_masculino = 0
    for persona in usuarios:
        try:
            persona = Persona.objects.get(pk=persona.id)
        except:
            print 'edad no es una persona'
        if persona.sexo == "F":
            sexo_femenino = sexo_femenino + 1
        else:
            sexo_masculino = sexo_masculino + 1
    return sexo_femenino, sexo_masculino


def get_usuarios_por_rango_edad(usuarios):
    current_year = date.today().year
    primer_rango = 0
    segundo_rango = 0
    tercer_rango = 0
    cuarto_rango = 0
    quinto_rango = 0
    sexto_rango = 0
    septimo_rango = 0
    octavo_rango = 0
    noveno_rango = 0
    decimo_rango = 0
    undecimo_rango = 0
    for usuario in usuarios:
        try:
            persona = Persona.objects.get(pk=usuario.id)
            edad = current_year - persona.fecha_nacimiento.year
            if edad >= 15 and edad < 20:
                primer_rango = primer_rango + 1
            if edad >= 20 and edad < 25:
                segundo_rango = segundo_rango + 1
            if edad >= 25 and edad < 30:
                tercer_rango = tercer_rango + 1
            if edad >= 30 and edad < 35:
                cuarto_rango = cuarto_rango + 1
            if edad >= 35 and edad < 40:
                quinto_rango = quinto_rango + 1
            if edad >= 40 and edad < 45:
                sexto_rango = sexto_rango + 1
            if edad >= 45 and edad < 50:
                septimo_rango = septimo_rango + 1
            if edad >= 50 and edad < 55:
                octavo_rango = octavo_rango + 1
            if edad >= 55 and edad < 60:
                noveno_rango = noveno_rango + 1
            if edad >= 60 and edad < 65:
                decimo_rango = decimo_rango + 1
            if edad >= 65 and edad < 70:
                undecimo_rango = undecimo_rango + 1
            if edad < 15 or edad > 69:
                print 'no entro'
        except:
            print 'es empresa'
    dict_cant = SortedDict()
    dict_cant["15-20"] = primer_rango
    dict_cant["20-25"] = segundo_rango
    dict_cant["25-30"] = tercer_rango
    dict_cant["30-35"] = cuarto_rango
    dict_cant["35-40"] = quinto_rango
    dict_cant["40-45"] = sexto_rango
    dict_cant["45-50"] = septimo_rango
    dict_cant["50-55"] = octavo_rango
    dict_cant["55-60"] = noveno_rango
    dict_cant["60-65"] = decimo_rango
    dict_cant["65-70"] = undecimo_rango
    return dict_cant