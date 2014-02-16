from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from segmentation.views import AnalisisDenunciaList, AnalisisDenunciaUpdate

urlpatterns = patterns('',
    url(r'^analisisdenuncias/$',
        permission_required('segmentation.change_analisisdenuncia')(AnalisisDenunciaList.as_view()),
        name="analisisdenuncias"),
    url(r'^analisisdenuncia/(?P<pk>\d+)/$',
        permission_required('segmentation.change_analisisdenuncia')(AnalisisDenunciaUpdate.as_view()),
        name='analisisdenuncia'),
)