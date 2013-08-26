from django.contrib.auth.decorators import login_required
from dash.forms import SearchBox
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from models import PlanXEmpresa, Plan
from items.models import Item
import datetime
import calendar


@login_required(login_url='/accounts/user/')
def dash_planes(request):
    searchbox = SearchBox()
    message = ''
    planes = request.user.plan_empresa.all().order_by('-fecha_fin_vigencia')
    posee_plan = False
    if not planes:
        message = 'No posee planes. Por favor seleccione un plan.'
        plan = None
    else:
        plan = planes[0]
        posee_plan = True
    return render_to_response('bussiness/dash_planes.html', {'form_search': searchbox,
        'message': message, 'plan': plan, 'posee_plan': posee_plan},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def elegir_plan(request):
    searchbox = SearchBox()
    messages = ['']
    if request.method == 'POST':
        plan_id = request.POST.get("planIdSeleccionado", "")
        plan_elegido = Plan.objects.get(pk=plan_id)
        plan = PlanXEmpresa()
        plan.plan = plan_elegido
        plan.empresa = request.user
        plan.fecha_inicio_vigencia = datetime.datetime.now()
        plan.fecha_fin_vigencia = add_months(plan.fecha_inicio_vigencia, 1)
        plan.save()
        return HttpResponseRedirect('/bussiness/dash_planes/')
    else:
        planes = Plan.objects.all()
    return render_to_response('bussiness/elegir_plan.html',
        {'form_search': searchbox,
        'planes': planes, 'messages': messages},
        context_instance=RequestContext(request))


def new_notificacion(request):
    pass


@login_required(login_url='/accounts/user/')
def dash_empresa(request):
    messages = ['']
    searchbox = SearchBox()
    return render_to_response('bussiness/dash_empresa.html', {'form_search': searchbox,
        'messages': messages},
        context_instance=RequestContext(request))

@login_required(login_url='/accounts/user/')
def registrar_enlace(request, item_id):
    item = Item.objects.get(pk=item_id)
    planes = request.user.plan_empresa.all().order_by('-fecha_fin_vigencia')
    plan_vigente = planes[0]
    plan_vigente.item.add(item)
    plan_vigente.save()
    return HttpResponseRedirect('/bussiness/dash_planes/')

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
