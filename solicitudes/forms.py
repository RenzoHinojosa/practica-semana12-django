from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Solicitud

def sanitize_input(value):
    # Normaliza texto plano; el autoescape de plantillas protege la salida HTML.
    # El ORM parametriza SQL. strip/escape NO sustituyen esa protección.
    return value.strip()

class RegistroForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['codigo', 'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
                   'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
                   'descripcion': forms.Textarea(attrs={'rows': 4})}
    def clean_codigo(self):
        return sanitize_input(self.cleaned_data['codigo'])
    def clean_titulo(self):
        value = sanitize_input(self.cleaned_data['titulo'])
        if len(value) < 5:
            raise ValidationError('Escribe al menos cinco caracteres.')
        return value
    def clean_descripcion(self):
        return sanitize_input(self.cleaned_data['descripcion'])
    def clean(self):
        # IA: validación cruzada con campos inválidos → Solución manual: usar get(),
        # porque clean() se ejecuta aunque otro campo haya fallado.
        data = super().clean()
        inicio, fin = data.get('fecha_inicio'), data.get('fecha_fin')
        if inicio and fin and fin < inicio:
            self.add_error('fecha_fin', 'La fecha final debe ser igual o posterior a la inicial.')
        if data.get('titulo') and data.get('descripcion') and data['titulo'].lower() == data['descripcion'].lower():
            raise ValidationError('La descripción debe aportar información adicional al título.')
        return data

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=80, min_length=3)
    correo = forms.EmailField()
    mensaje = forms.CharField(min_length=15, max_length=2000, widget=forms.Textarea(attrs={'rows': 4}))
    def clean_nombre(self):
        return sanitize_input(self.cleaned_data['nombre'])
    def clean_correo(self):
        return self.cleaned_data['correo'].strip().lower()
    def clean_mensaje(self):
        return sanitize_input(self.cleaned_data['mensaje'])
