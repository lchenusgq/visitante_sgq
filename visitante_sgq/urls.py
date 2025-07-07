"""
URL configuration for visitante_sgq project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from registro_visitantes.views import verificar_cedula, registro_visitante
from registro_visitantes import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registro_visitantes.urls')),
    path('api/verificar_cedula/', views.verificar_cedula, name='verificar_cedula'),
] 

#
# visitante_sgq/views.py
#from django.http import HttpResponse
#
#def verificar_cedula(request):
#    return HttpResponse("Verificando cédula...")
#
#def registro_visitante(request):
#    return HttpResponse("Registro de visitante...")