from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Modelo Oficina
class Oficina(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# Modelo Visitante
class Visitante(models.Model):
    cedula = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    #def save(self, *args, **kwargs):
    #    # Validar cédula antes de guardar
    #    if not self.cedula.isdigit():
    #        raise ValueError('La cédula debe contener solo números.')
    #    if len(self.cedula) > 10:
    #        raise ValueError('La cédula no debe sobrepasar los 10 dígitos.')
    #    super(Visitante, self).save(*args, **kwargs)    

    def clean(self):
        if not self.cedula.isdigit():
            raise ValidationError({'cedula': 'La cédula debe contener solo números'})
        if len(self.cedula) > 10:
            raise ValidationError({'cedula': 'La cédula no debe sobrepasar los 10 caracteres'})

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# Modelo RegistroVisita
class RegistroVisita(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE)
    oficina = models.ForeignKey(Oficina, on_delete=models.PROTECT)
    motivo_visita = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visita de {self.visitante} a {self.oficina} el {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"
