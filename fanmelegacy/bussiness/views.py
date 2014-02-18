from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from models import PlanXEmpresa, Plan
from items.models import Item
import datetime
import calendar
from django.contrib import messages
import os
import mercadopago


@login_required(login_url='/accounts/user/')
def dash_planes(request):
    message = ''
    planes = request.user.plan_empresa.all().order_by('-fecha_fin_vigencia')
    consultas_noleidas = request.user.consultas_recibidas.filter(
            estado="noleido").count()
    posee_plan = False
    if not planes:
        message = 'No posee planes. Por favor seleccione un plan.'
        plan = None
    else:
        plan = planes[0]
        posee_plan = True
    return render_to_response('bussiness/dash_planes.html', {
        'message': message, 'plan': plan, 'posee_plan': posee_plan,
        'consultas_noleidas': consultas_noleidas,
        'breadcrumb': ["Planes", "Vigentes"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def elegir_plan(request):
    if request.method == 'POST':
        plan_id = request.POST.get("planIdSeleccionado", "")
        plan_elegido = Plan.objects.get(pk=plan_id)
        plan = PlanXEmpresa()
        plan.plan = plan_elegido
        plan.empresa = request.user
        plan.fecha_inicio_vigencia = datetime.datetime.now()
        plan.fecha_fin_vigencia = add_months(plan.fecha_inicio_vigencia, 1)
        plan.save()

        CLIENT_ID = os.environ.setdefault("CLIENT_ID", "")
        CLIENT_SECRET = os.environ.setdefault("CLIENT_SECRET", "")
        preference = {
          "items": [
            {
              "title": plan.plan.nombre,
              "quantity": 1,
              "currency_id": "ARS",
              "unit_price": float(plan.plan.precio)
            }
          ]
        }
        # import ipdb; ipdb.set_trace()
        mp = mercadopago.MP(CLIENT_ID, CLIENT_SECRET)

        preferenceResult = mp.create_preference(preference)

        url = preferenceResult["response"]["sandbox_init_point"]

        return render_to_response('bussiness/pago_plan.html',
                        {'url': url,
                        'plan': plan.plan,
                        'breadcrumb': ["Pago", "Plan"]},
                        context_instance=RequestContext(request))
    else:
        planes = Plan.objects.all()
    return render_to_response('bussiness/elegir_plan.html',
        {'planes': planes, 'breadcrumb': ["Planes", "Elegir plan"]},
        context_instance=RequestContext(request))


def new_notificacion(request):
    pass


@login_required(login_url='/accounts/user/')
def dash_empresa(request):
    consultas_noleidas = request.user.consultas_recibidas.filter(
            estado="noleido").count()
    followers = request.user.followers.filter(user__is_active=True)
    return render_to_response('bussiness/dash_empresa.html',
        {'consultas_noleidas': consultas_noleidas,
        'followers': followers,
        'breadcrumb': ["Dashboard"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def registrar_enlace(request, item_id):
    item = Item.objects.get(pk=item_id)
    planes = request.user.plan_empresa.all().order_by('-fecha_fin_vigencia')
    if not planes:
        return HttpResponseRedirect('/bussiness/dash_planes/')
    plan_vigente = planes[0]
    plan_vigente.item.add(item)
    plan_vigente.save()
    redirect_uri = '/items/item/' + item_id
    messages.add_message(request, messages.SUCCESS, 'Se ha registrado el enlace correctamente.')
    return HttpResponseRedirect(redirect_uri)


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


@login_required
def pago_plan(request):
    import mercadopago
    CLIENT_ID = os.environ.setdefault("CLIENT_ID", "")
    CLIENT_SECRET = os.environ.setdefault("CLIENT_SECRET", "")
    preference = {
      "items": [
        {
          "title": "sdk-python",
          "quantity": 1,
          "currency_id": "ARS",
          "unit_price": 10.5
        }
      ]
    }
    mp = mercadopago.MP(CLIENT_ID, CLIENT_SECRET)

    preferenceResult = mp.create_preference(preference)

    url = preferenceResult["response"]["sandbox_init_point"]

    return render_to_response('bussiness/pago_plan.html',
        {'url': url,
        'breadcrumb': ["Pago", "Plan"]},
        context_instance=RequestContext(request))
