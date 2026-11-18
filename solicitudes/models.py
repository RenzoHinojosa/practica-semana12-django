from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
codigo_validator = RegexValidator(r'^[A-Z]{3}-[0-9]{4}$', 'Usa el formato SOL-0001.')
class Solicitud(models.Model):
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=8, unique=True, validators=[codigo_validator])
    titulo = models.CharField(max_length=100, validators=[MinLengthValidator(5)])
    descripcion = models.TextField(validators=[MinLengthValidator(15)])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=12, choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada')], default='pendiente')
    creada = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-creada']
        permissions = [('gestionar_solicitudes', 'Puede consultar todas las solicitudes')]
    def clean(self):
        super().clean()
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({'fecha_fin': 'La fecha final no puede ser anterior a la inicial.'})
    def __str__(self):
        return f'{self.codigo}: {self.titulo}'
