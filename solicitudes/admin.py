from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Solicitud
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'titulo', 'propietario', 'estado', 'duracion', 'creada']
    list_filter = ['estado', 'fecha_inicio']
    search_fields = ['codigo', 'titulo', 'propietario__username']
    readonly_fields = ['creada', 'duracion']
    fields = ['propietario', 'codigo', 'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado', 'creada', 'duracion']
    list_select_related = ['propietario']
    actions = ['aprobar']
    @admin.display(description='Duración en días')
    def duracion(self, obj):
        return (obj.fecha_fin - obj.fecha_inicio).days if obj.fecha_fin and obj.fecha_inicio else '—'
    @admin.action(description='Aprobar solicitudes seleccionadas', permissions=['change'])
    def aprobar(self, request, queryset):
        count = queryset.update(estado='aprobada')
        self.message_user(request, f'{count} solicitudes aprobadas.')
# El admin de este laboratorio no permite administrar usuarios ni privilegios.
from django.contrib.auth.models import User
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.site_header = 'Semana 12 · Administración'
