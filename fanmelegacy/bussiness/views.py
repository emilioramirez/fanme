from django.contrib.auth.decorators import login_required
from dash.forms import SearchBox
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required(login_url='/accounts/user/')
def dash_planes(request):
    searchbox = SearchBox()
    messages = ['']
    posee_plan = False
    planes = request.user.plan_empresa.all().order_by(
            'fecha_fin_vigencia')
    print planes
    if not planes:
        messages = ['No posee planes. Por favor seleccione un plan.']
    else:
        posee_plan = True
        print planes
    return render_to_response('bussiness/dash_planes.html', {'form_search': searchbox,
        'messages': messages, 'posee_plan': posee_plan},
        context_instance=RequestContext(request))


def new_notificacion(request):
    pass
