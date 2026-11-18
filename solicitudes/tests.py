from datetime import date
from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse
from .forms import SolicitudForm, ContactoForm
from .models import Solicitud


class FlujosTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('renzo', password='Clave-prueba-98!')
        self.other = User.objects.create_user('otro', password='Clave-prueba-98!')
        self.data = {'codigo': 'SOL-0001', 'titulo': 'Solicitud de laboratorio',
                     'descripcion': 'Necesito acceso al laboratorio de desarrollo.',
                     'fecha_inicio': '2026-11-18', 'fecha_fin': '2026-11-20'}

    def test_anonimo_y_permiso_gestor(self):
        self.assertRedirects(self.client.get('/'), '/cuentas/login/?next=/')
        self.client.force_login(self.user)
        self.assertEqual(self.client.get('/gestion/').status_code, 403)
        call_command('crear_roles', usuario='renzo')
        self.assertEqual(self.client.get('/gestion/').status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)

    def test_guardado_y_aislamiento(self):
        self.client.force_login(self.user)
        response = self.client.post('/solicitudes/nueva/', self.data)
        self.assertRedirects(response, '/')
        self.assertEqual(Solicitud.objects.get().propietario, self.user)
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get('/'), 'SOL-0001')
        call_command('crear_roles', usuario='otro')
        self.assertContains(self.client.get('/gestion/'), 'SOL-0001')

    def test_validacion_cruzada_y_campo_invalido(self):
        data = {**self.data, 'fecha_fin': '2026-11-17'}
        form = SolicitudForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_fin', form.errors)
        form = SolicitudForm({**data, 'fecha_inicio': 'no-es-fecha'})
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_inicio', form.errors)

    def test_codigo_duplicado_y_regex(self):
        self.client.force_login(self.user)
        self.client.post('/solicitudes/nueva/', self.data)
        self.assertFalse(SolicitudForm(self.data).is_valid())
        self.assertFalse(SolicitudForm({**self.data, 'codigo': 'incorrecto'}).is_valid())

    def test_contacto_y_escape_html(self):
        form = ContactoForm({'nombre': '  Renzo  ', 'correo': 'RENZO@EXAMPLE.COM',
                            'mensaje': 'Mensaje de prueba válido.'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['correo'], 'renzo@example.com')
        self.client.force_login(self.user)
        self.client.post('/solicitudes/nueva/', {**self.data, 'titulo': '<script>alert(1)</script>'})
        response = self.client.get('/')
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>')

    def test_csrf_sesion_headers_logout(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/registro/', {}).status_code, 403)
        response = client.get('/cuentas/login/')
        token = client.cookies['csrftoken'].value
        response = client.post('/cuentas/login/', {'username': 'renzo',
            'password': 'Clave-prueba-98!', 'csrfmiddlewaretoken': token})
        self.assertEqual(response.status_code, 302)
        response = client.get('/')
        self.assertEqual(client.session['visitas'], 1)
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        self.assertIn("frame-ancestors 'none'", response['Content-Security-Policy'])
        self.assertIn('X-Request-ID', response)
        self.assertEqual(client.get('/cuentas/logout/').status_code, 405)
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post('/cuentas/logout/', {'csrfmiddlewaretoken': token}).status_code, 302)
        self.assertNotIn('_auth_user_id', client.session)

    def test_registro_sin_privilegios_y_password_cifrada(self):
        response = self.client.post('/registro/', {'username': 'nuevo', 'email': 'NUEVO@EXAMPLE.COM',
            'password1': 'UnaClave-Larga-2035!', 'password2': 'UnaClave-Larga-2035!', 'is_staff': '1'})
        self.assertRedirects(response, '/cuentas/login/')
        user = User.objects.get(username='nuevo')
        self.assertEqual(user.email, 'nuevo@example.com')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password('UnaClave-Larga-2035!'))
