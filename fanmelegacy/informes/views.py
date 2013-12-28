from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from datetime import date
from segmentation.models import Topico
from items.models import Item


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
    dict = {}
    for topico in topicos:
        items_por_topico = Item.objects.filter(topico=topico)
        cant_fans = 0
        for item in items_por_topico:
            cant_fans = cant_fans + item.cantidad_fans
        dict[topico] = cant_fans
    length = len(dict)
    return render_to_response('informes/fans_por_topico.html',
        #{'fans_por_topicos': dict},
        {'fans_por_topicos': dict, 'length': length},
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
        dict_cant = {}
        dict_cant['enero'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=1).count()
        dict_cant['febrero'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=2).count()
        dict_cant['marzo'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=3).count()
        dict_cant['abril'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=4).count()
        dict_cant['mayo'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=5).count()
        dict_cant['junio'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=6).count()
        dict_cant['julio'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=7).count()
        dict_cant['agosto'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=8).count()
        dict_cant['septiembre'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=9).count()
        dict_cant['octubre'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=10).count()
        dict_cant['noviembre'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=11).count()
        dict_cant['diciembre'] = User.objects.filter(date_joined__year=year).filter(
            date_joined__month=12).count()
        dict[year] = dict_cant
    return render_to_response('informes/progreso.html',
        {'dict': dict, 'mostrar_form': mostrar_form},
        context_instance=RequestContext(request))
