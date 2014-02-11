from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from rathings.models import Like, Dislike, dislike_created


@login_required
def like(request, object_id):
    """
    """
    ctype_id = request.GET.get("ctype", None)
    next = request.GET.get("next", None)

    if ctype_id is None:
        messages.add_message(request, messages.ERROR, _("Error interno"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    object_ctype = ContentType.objects.get_for_id(ctype_id)    
    obj, created = Like.objects.get_or_create(content_type=object_ctype, object_id=object_id, user=request.user)
    if not created:
        messages.add_message(request, messages.INFO, _("Ya te gusta ese comentario"))
    else:
        messages.add_message(request, messages.SUCCESS, _("Ahora te gusta este comentario"))

    if next is not None:
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike(request, object_id):
    """
    """
    ctype_id = request.GET.get("ctype", None)
    next = request.GET.get("next", None)

    if ctype_id is None:
        messages.add_message(request, messages.ERROR, _("Missing ctype_id"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    object_ctype = ContentType.objects.get_for_id(ctype_id)    
    obj, created = Dislike.objects.get_or_create(content_type=object_ctype, object_id=object_id, user=request.user)
    if not created:
        messages.add_message(request, messages.INFO, _("Ya denunciaste este  {}".format(object_ctype.model)))
    else:
        messages.add_message(request, messages.SUCCESS, _("Acabas de denunciar el {}".format(object_ctype.model)))
        dislike_created.send(sender=Dislike, instance=obj)

    if next is not None:
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

