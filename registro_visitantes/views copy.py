# Create your views here.
#import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, FileResponse
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, TA_CENTER
from reportlab.platypus import BaseDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageTemplate, Frame
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

import os
import json
import base64
import pytz

from io import BytesIO

from datetime import datetime

from .forms import ReporteForm
from .forms import RegistroVisitanteForm
from .models import Oficina, Visitante, RegistroVisita 



def reporte_visitas_pdf(request):
    ruta_pdf = os.path.join(settings.MEDIA_ROOT, 'visitas', 'visitas.pdf')

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            messages.error(request, "Debe ingresar las fechas de inicio y fin")
            return render(request, 'formulario_reporte.html')

        try:
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
            datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            messages.error(request, "Formato de fecha inválido. Debe ser en formato YYYY-MM-DD")
            return render(request, 'formulario_reporte.html')

        visitas = RegistroVisita.objects.filter(fecha_hora__date__range=[fecha_inicio, fecha_fin]).order_by('fecha_hora')

        buffer = BytesIO()

        #doc = SimpleDocTemplate(
        doc = BaseDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=50,
            rightMargin=50,
            topMargin=100,   # Aumentamos margen superior para dejar espacio al encabezado
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        styles['Title'].fontSize = 18
        styles['Title'].alignment = TA_CENTER
        estilo_parrafo = styles["Normal"]
        elementos = []

        logo_path = os.path.join(settings.BASE_DIR, 'registro_visitantes', 'static', 'images', 'logoSGQ.png')

        # HEADER para cada página
        def header(canvas, doc):
            canvas.saveState()

            ancho_pagina = letter[0]  # 612 puntos para tamaño carta
            ancho_logo = 330
            x_centrado = (ancho_pagina - ancho_logo) / 2
            canvas.drawImage(logo_path, x_centrado, 720, width=ancho_logo, height=60, mask='auto')

            #canvas.drawImage(logo_path, 20, 740, width=330, height=60)
            canvas.setFont("Helvetica-Bold", 14)
            canvas.drawString(180, 710, "Reporte de Visitas a Oficinas de la SGQ")
            canvas.restoreState()



        # Frame para evitar que el contenido toque el encabezado
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        plantilla = PageTemplate(id='header_template', frames=[frame], onPage=header)
        doc.addPageTemplates([plantilla])

        data = [['FECHA', 'HORA', 'NOMBRE', 'CEDULA', 'OFICINA', 'MOTIVO VISITA']]
        for visita in visitas:
            visitante = visita.visitante
            fecha_hora_local = visita.fecha_hora.astimezone(pytz.timezone(settings.TIME_ZONE))
            data.append([
                fecha_hora_local.strftime('%d/%m/%Y'),
                fecha_hora_local.strftime('%H:%M'),
                f"{visitante.nombres} {visitante.apellidos}",
                f"{int(visitante.cedula):,}".replace(",", "."),
                Paragraph(visita.oficina.nombre) if visita.oficina else '',
                Paragraph(visita.motivo_visita, estilo_parrafo)
            ])

        
        # Preparar la tabla con columnas proporcionales
        ancho_disponible = letter[0] - doc.leftMargin - doc.rightMargin
        proporciones = [0.15, 0.10, 0.25, 0.15, 0.15, 0.20]
        col_widths = [ancho_disponible * p for p in proporciones]
        
        #tabla = Table(data, colWidths=[100, 50, 150, 100, 100, 150])
        tabla = Table(data, colWidths=col_widths)
        tabla.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ]))

        elementos.append(tabla)
        doc.build(elementos)

        with open(ruta_pdf, 'wb') as f:
            f.write(buffer.getvalue())

        request.session['pdf_path'] = ruta_pdf
        pdf_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return render(request, 'registro_visitantes/visor_pdf.html', {'pdf_base64': pdf_base64})

    return render(request, 'formulario_reporte.html')




def descargar_pdf(request):
    # Construir la ruta del archivo
    ruta_pdf = os.path.join(settings.MEDIA_ROOT, 'visitas', 'visitas.pdf')
    print(f"Ruta del archivo: {ruta_pdf}")

    # Verificar si el archivo existe
    if not os.path.isfile(ruta_pdf):
        return HttpResponse("El archivo no existe.", status=404)

    try:
        # Abrir el archivo sin usar 'with'
        f = open(ruta_pdf, 'rb')
        response = FileResponse(f, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_visitas.pdf"'
        return response
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return HttpResponse(f"Error al intentar descargar el archivo: {e}", status=500)



def formulario_reporte(request):
    return render(request, 'formulario_reporte.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('registro_visitante')
        else:
            messages.error(request, 'Usuario o contraseña incorrecta. Por favor, ingrese los datos correctamente.')
    return render(request, 'registro_visitantes/login.html')

    
def registro_visitante(request):
    oficinas = Oficina.objects.all()

    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        oficina_id = request.POST.get('oficina')
        motivo_visita = request.POST.get('motivo_visita')

        print(f"Cédula: {cedula}")
        print(f"Nombre: {nombres}")
        print(f"Apellido: {apellidos}")
        print(f"Oficina: {oficina_id}")
       
        if not motivo_visita:
            messages.error(request, "El motivo de la visita es obligatorio.")
            return redirect('registro_visitante')

        # Buscar o crear visitante
        visitante, creado = Visitante.objects.get_or_create(
            cedula=cedula,
            defaults={'nombres': nombres, 'apellidos': apellidos}
        )

        # Buscar la oficina seleccionada
        oficina = get_object_or_404(Oficina, id=oficina_id)

        # Crear el registro de la visita
        RegistroVisita.objects.create(
            visitante=visitante,
            oficina=oficina,
            motivo_visita=motivo_visita
            # No asignamos fecha_hora, Django lo hace automático
        )

        messages.success(request, f"Visita registrada con éxito para {visitante.nombres} {visitante.apellidos}.")
        return redirect('registro_visitante')

    # Para solicitud GET, enviar oficinas y fecha/hora actual (opcional)
    fecha_hora_actual = timezone.now()
    return render(request, 'registro_visitantes/registro_visitante.html', {'oficinas': oficinas, 'fecha_hora': fecha_hora_actual})




@csrf_exempt  # Solo si no tenés el CSRF configurado correctamente desde JS
def verificar_cedula(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cedula = data.get('cedula')

            print(f"🔎 Cédula recibida: {cedula}")  # Agregado

            if not cedula:
                return JsonResponse({'exists': False, 'error': 'Cédula no proporcionada'}, status=400)

            try:
                visitante = Visitante.objects.get(cedula=cedula)
                return JsonResponse({
                    'exists': True,
                    'nombres': visitante.nombres,
                    'apellidos': visitante.apellidos
                })
            except Visitante.DoesNotExist:
                return JsonResponse({'exists': False})
        except json.JSONDecodeError:
            return JsonResponse({'exists': False, 'error': 'Error al procesar JSON'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
        

