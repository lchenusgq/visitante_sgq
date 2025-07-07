
from django.views.generic.base import RedirectView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views  # Importa las vistas desde la aplicación registro_visitantes

urlpatterns = [
    path('', RedirectView.as_view(url='/login/'), name='root'),
    path('login/', views.login, name='login'),
    path('registro_visitante/', views.registro_visitante, name='registro_visitante'),
    path('reporte_visitas_pdf/', views.reporte_visitas_pdf, name='reporte_visitas_pdf'),
    path('formulario_reporte/', views.formulario_reporte, name='formulario_reporte'),
    path('reporte_visitas_pdf/', views.reporte_visitas_pdf, name='reporte_visitas_pdf'),
    path('descargar_pdf/', views.descargar_pdf, name='descargar_pdf'),
    #path('verificar_cedula/', views.verificar_cedula, name='verificar_cedula'),
    path('ver_pdf/', views.ver_pdf, name='ver_pdf'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])





