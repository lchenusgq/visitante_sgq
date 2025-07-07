from django import forms
from .models import Visitante
from .models import RegistroVisita
from datetime import date

class RegistroVisitanteForm(forms.ModelForm):
    class Meta:
        model = RegistroVisita
        fields = ['visitante', 'oficina', 'motivo_visita']


    cedula = forms.CharField(max_length=10, min_length=1, required=True, label="Cédula")

    #def clean_cedula(self):
    #    cedula = self.cleaned_data['cedula']
    #    if not cedula.isdigit():
    #        raise forms.ValidationError('La cédula debe contener solo números')
    #    if len(cedula) > 10:
    #        raise forms.ValidationError('La cédula no debe sobrepasar los 8 caracteres')
    #    return cedula

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha > date.today():
            raise forms.ValidationError("La fecha no puede ser mayor a la del sistema")
        return fecha

class ReporteForm(forms.Form):
    fecha_inicio = forms.DateField(input_formats=['%Y-%m-%d'])
    fecha_fin = forms.DateField(input_formats=['%Y-%m-%d'])
