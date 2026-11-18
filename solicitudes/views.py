from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView
from .forms import ContactoForm, RegistroForm, SolicitudForm
from .models import Solicitud

def registro(request):
    form = RegistroForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cuenta creada. Ya puedes iniciar sesión.')
        return redirect('login')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Crear cuenta'})

@login_required
def inicio(request):
    # IA: contador de sesión → Solución manual: asignar la clave marca la sesión
    # como modificada; modified=True solo hace falta para cambios anidados.
    request.session['visitas'] = request.session.get('visitas', 0) + 1
    return render(request, 'inicio.html', {'solicitudes': Solicitud.objects.filter(propietario=request.user),
        'visitas': request.session['visitas']})

@login_required
def nueva(request):
    form = SolicitudForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        solicitud = form.save(commit=False)
        solicitud.propietario = request.user
        solicitud.save()
        messages.success(request, 'Solicitud registrada correctamente.')
        return redirect('inicio')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Nueva solicitud'})

@login_required
def contacto(request):
    form = ContactoForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        messages.success(request, f"Mensaje validado de {form.cleaned_data['nombre']}. Demostración sin envío de correo.")
        return redirect('contacto')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Formulario clásico de contacto'})

class GestionView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'solicitudes.gestionar_solicitudes'
    model = Solicitud
    template_name = 'gestion.html'
    context_object_name = 'solicitudes'
    def get_queryset(self):
        return super().get_queryset().select_related('propietario')
