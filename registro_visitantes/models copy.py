from django.db import models
from django.utils import timezone
# Create your models here.

def get_current_date():
    return timezone.now().date()

def get_current_time():
    return timezone.now().time()

class Visitante(models.Model):
    cedula = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    #######
    OFICINAS_CHOICES = [
        ('Primer Turno', 'Primer Turno'),
        ('Segundo Turno', 'Segundo Turno'),
        ('Tercer Turno', 'Tercer Turno'),
        ('Cuarto Turno', 'Cuarto Turno'),
        ('Quinto Turno', 'Quinto Turno'),
        ('Sexto Turno', 'Sexto Turno'),
        ('Informática', 'Informática'),
        ('UOC', 'UOC'),
        ('Control Interno', 'Control Interno'),
        ('Servicios Logísticos', 'Servicios Logísticos'),
        ('DIGEAF', 'DIGEAF'),
        ('Dirección Administrativa', 'Dirección Administrativa'),
        ('Dirección Financiera', 'Dirección Financiera'),
        ('Dirección de Asuntos Jurídicos', 'Dirección de Asuntos Jurídicos'),
        ('Síndico General de Quiebras', 'Síndico General de Quiebras'),
        ('Mesa de Entrada', 'Mesa de Entrada'),
        ('Secretaría General', 'Secretaría General'),
        ('Presupuesto', 'Presupuesto'),
        ('Contabilidad', 'Contabilidad'),
        ('Rendición de Cuentas', 'Rendición de Cuentas'),
        ('Talento Humano', 'Talento Humano'),
        ('Auditoría Interna', 'Auditoría Interna'),
        ('Auditoria Contable Jurisdiccional', 'Auditoria Contable Jurisdiccional'),
        ('Digitalización', 'Digitalización'),
        ('Servicios Generales', 'Servicios Generales'),
        ('MECIP', 'MECIP'),
        ('Patrimonio', 'Patrimonio'),
    ]
    oficina = models.CharField(max_length=100, choices=OFICINAS_CHOICES)
    motivo_visita = models.CharField(max_length=200)
    fecha = models.DateField(default=get_current_date)
    hora = models.TimeField(default=get_current_time)
    #fecha = models.DateField(default=timezone.now().date())
    #hora = models.TimeField(default=get_current_time)
    #fecha = models.DateField(default=timezone.now().date())
    #hora = models.TimeField(default=timezone.now().time())
    #fecha = models.DateField()
    #hora = models.TimeField()