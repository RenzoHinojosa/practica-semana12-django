from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
class Command(BaseCommand):
    help = 'Crea el rol Gestor y opcionalmente lo asigna a un usuario existente.'
    def add_arguments(self, parser):
        parser.add_argument('--usuario')
    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name='Gestor')
        group.permissions.add(Permission.objects.get(codename='gestionar_solicitudes', content_type__app_label='solicitudes'))
        if options['usuario']:
            try:
                user = User.objects.get(username=options['usuario'])
            except User.DoesNotExist:
                from django.core.management.base import CommandError
                raise CommandError('Registra primero ese usuario.')
            user.groups.add(group)
        self.stdout.write(self.style.SUCCESS('Rol Gestor configurado. No concede acceso al admin.'))
