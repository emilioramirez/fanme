from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from datetime import date


@staff_member_required
def my_admin_view(request):
    active_users = User.objects.filter(is_active=True)
    inactive_users = User.objects.filter(is_active=False)
    return render_to_response('informes/my_template.html',
        {'active_users': active_users.count(), 'inactive_users': inactive_users.count()},
        context_instance=RequestContext(request))


@staff_member_required
def progreso(request):
    current_year = date.today().year
    current_year = 2011
    usuarios_enero = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=1).count()
    usuarios_febrero = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=2).count()
    usuarios_marzo = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=3).count()
    usuarios_abril = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=4).count()
    usuarios_mayo = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=5).count()
    usuarios_junio = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=6).count()
    usuarios_julio = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=7).count()
    usuarios_agosto = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=8).count()
    usuarios_septiembre = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=9).count()
    usuarios_octubre = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=10).count()
    usuarios_noviembre = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=11).count()
    usuarios_diciembre = User.objects.filter(date_joined__year=current_year).filter(
        date_joined__month=12).count()
    return render_to_response('informes/progreso.html',
        {'usuarios_enero': usuarios_enero, 'usuarios_febrero': usuarios_febrero,
        'usuarios_marzo': usuarios_marzo, 'usuarios_abril': usuarios_abril,
        'usuarios_mayo': usuarios_mayo, 'usuarios_junio': usuarios_junio,
        'usuarios_julio': usuarios_julio, 'usuarios_agosto': usuarios_agosto,
        'usuarios_septiembre': usuarios_septiembre, 'usuarios_octubre': usuarios_octubre,
        'usuarios_noviembre': usuarios_noviembre, 'usuarios_diciembre': usuarios_diciembre},
        context_instance=RequestContext(request))
