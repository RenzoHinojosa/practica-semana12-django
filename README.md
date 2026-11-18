# Práctica Semana 12 — Django

Autor: RenzoHinojosa · hinojosayarangasebastian@gmail.com

Aplicación de solicitudes para la guía de Desarrollo de Aplicaciones Web. Incluye formularios clásico y ModelForm, validación de campos y fechas, registro, login/logout, sesiones, permisos, administración y auditoría. El formulario de contacto valida datos y muestra confirmación; no envía correo.

## Ejecutar en Visual Studio Code en Windows

Necesitas Python 3.11 o superior, Git y VS Code instalados. Descomprime el ZIP y abre **la carpeta que contiene manage.py** en VS Code (Archivo → Abrir carpeta). Abre Terminal → Nueva terminal y ejecuta:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py crear_roles
.\.venv\Scripts\python.exe manage.py createsuperuser --username RenzoHinojosa --email hinojosayarangasebastian@gmail.com
.\.venv\Scripts\python.exe manage.py runserver
```

El comando createsuperuser solicita una contraseña elegida por ti; al escribirla no se muestra en pantalla. No hay credenciales predeterminadas. Abre http://127.0.0.1:8000/ y el admin en http://127.0.0.1:8000/admin/. Detén el servidor con Ctrl+C.

No es necesario activar el entorno virtual ni cambiar la política de PowerShell. Si `py` no existe, instala Python con el lanzador de Windows y vuelve a abrir VS Code. En VS Code selecciona `.venv\Scripts\python.exe` mediante “Python: Select Interpreter”. Después de preparar la base, también puedes usar F5 con la configuración Django incluida.

En las siguientes ejecuciones:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Opcionalmente, `powershell -ExecutionPolicy Bypass -File .\iniciar.ps1` prepara dependencias, migraciones y roles e inicia el servidor. La excepción de política solo afecta ese proceso. El script no crea superusuarios.

## Usuarios y roles

Registra una cuenta normal desde `/registro/`. Esta cuenta solo ve sus propias solicitudes. El superusuario puede acceder a todo y aprobar solicitudes en el admin. Para demostrar permisos con una cuenta normal, regístrala como `gestor` y ejecuta, en otra terminal:

```powershell
.\.venv\Scripts\python.exe manage.py crear_roles --usuario gestor
```

El grupo Gestor permite consultar `/gestion/` con todas las solicitudes. No concede acceso al admin ni cambia `is_staff`. El admin excluye la administración de usuarios y grupos para no exponer contraseñas o privilegios. La asignación del rol se realiza mediante el comando anterior.

## Probar la práctica y tomar evidencias

1. Registra una cuenta e inicia sesión. Captura la pantalla de registro e inicio.
2. Crea `SOL-0001`, título de al menos 5 caracteres, descripción de al menos 15 y fechas válidas. Captura el listado.
3. Prueba código inválido, código duplicado, fecha final anterior a la inicial y descripción idéntica al título. Captura errores por campo y errores generales. No se guardan formularios inválidos.
4. Abre Contacto; prueba correo inválido y luego uno válido. Captura el resultado.
5. Sin rol, visita `/gestion/` para observar el 403. Asigna el rol, recarga y captura la vista de gestión.
6. Ingresa al admin con el superusuario: prueba búsqueda, filtros, duración calculada y la acción “Aprobar solicitudes seleccionadas”.
7. En DevTools → Network, inspecciona `Content-Security-Policy`, `X-Frame-Options`, `X-Request-ID` y `X-Content-Type-Options`. En Storage/Application inspecciona `sessionid` (HttpOnly, SameSite=Lax) y `csrftoken`. En HTTP local las cookies no llevan Secure; en producción sí.
8. Observa los logs en la terminal: método, ruta sin query string, estado, id de usuario y duración. No se registran contraseñas, cuerpo POST ni cookies.
9. Pulsa Salir y comprueba que una ruta privada vuelve al login. Logout usa POST y token CSRF.
10. Toma capturas reales de tu ejecución y añade el enlace de tu repositorio a tu entrega. Este paquete no incluye capturas inventadas ni un repositorio publicado.

## Validaciones automáticas

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py shell_plus
```

Los tests comprueban CSRF real, login/logout, permisos, aislamiento entre usuarios, registro sin elevación de privilegios, escape HTML, validación y cabeceras.

## GitHub con tus datos

Ejecuta estos comandos **dentro de la carpeta del proyecto**. La identidad se configura solo para este repositorio:

```powershell
git init
git config user.name "RenzoHinojosa"
git config user.email "hinojosayarangasebastian@gmail.com"
git add .
git commit -m "Implementa practica semana 12 con Django"
git branch -M main
```

Crea en GitHub un repositorio vacío llamado `practica-semana12-django`, sin README, licencia ni .gitignore. Luego:

```powershell
git remote add origin https://github.com/RenzoHinojosa/practica-semana12-django.git
git push -u origin main
```

Git puede abrir el navegador para autenticarte. `user.name` y `user.email` identifican los commits; no inician sesión. Si ya existe un remoto `origin`, usa `git remote set-url origin https://github.com/RenzoHinojosa/practica-semana12-django.git`. El enlace esperado, una vez publicado, es https://github.com/RenzoHinojosa/practica-semana12-django (no se ha creado desde este paquete).

Alternativa si tienes GitHub CLI instalado y prefieres crear el repositorio desde terminal, después del commit y **en lugar** de añadir el remoto manualmente:

```powershell
gh auth login
gh repo create RenzoHinojosa/practica-semana12-django --private --source=. --remote=origin --push
```

Para cambios posteriores:

```powershell
git add .
git commit -m "Actualiza la practica"
git push
```

`.gitignore` excluye la base de datos, entorno virtual, secretos y archivos temporales. No subas contraseñas ni tokens. El correo indicado quedará en los metadatos de tus commits.

## Seguridad y precisiones de la guía

Esta entrega contiene código generado con asistencia de IA. La guía exige escribir manualmente el 80% de la lógica de validación, middleware y configuración de seguridad: recibir este proyecto no acredita ese requisito. Revisa, comprende y reimplementa lo exigido para tu evaluación. Los comentarios `# IA:` documentan decisiones técnicas; no afirman que tú las hayas escrito manualmente.

Precisiones aplicadas al código:

- `Form.clean()` se ejecuta incluso si fallan campos. Se usa `cleaned_data.get()` para manejar datos ausentes.
- `strip()` y `lower()` normalizan entradas; no previenen por sí solos XSS o SQL injection. Se usa autoescape de plantillas y ORM con parámetros. No se marca texto del usuario como seguro ni se usa SQL crudo. Escapar antes de persistir produciría doble escape.
- El middleware recorre las solicitudes en el orden configurado y las respuestas en orden inverso. Este middleware retorna siempre una respuesta.
- Asignar una clave de sesión ya marca la sesión como modificada. `modified=True` es necesario si se mutan estructuras anidadas sin reasignarlas.
- Con sesiones DB, la cookie contiene un identificador opaco; los datos de sesión se guardan en el servidor, no en una cookie con todos sus datos.
- Un campo readonly del admin no se edita mediante ese formulario; un campo real como `creada` sí se almacena en la base de datos. `duracion` es un método calculado.

## Comprobación de configuración de producción

El modo local usa DEBUG para servir estáticos y HTTP. `check --deploy` en ese modo muestra advertencias esperadas. Para revisar la configuración de producción en una terminal aparte:

```powershell
$env:DJANGO_DEBUG = "0"
$env:DJANGO_SECRET_KEY = (.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(64))")
$env:DJANGO_ALLOWED_HOSTS = "tu-dominio.example"
.\.venv\Scripts\python.exe manage.py check --deploy
Remove-Item Env:DJANGO_DEBUG
Remove-Item Env:DJANGO_SECRET_KEY
Remove-Item Env:DJANGO_ALLOWED_HOSTS
```

Esto comprueba ajustes; no despliega la aplicación. Para una publicación real necesitas HTTPS, servidor WSGI/ASGI de producción, servicio de estáticos y persistir una clave secreta estable fuera de Git. `runserver` es para desarrollo. Rotar la clave invalida sesiones y firmas existentes.

Documentación oficial de referencia: https://docs.djangoproject.com/en/5.2/topics/forms/ · https://docs.djangoproject.com/en/5.2/topics/http/middleware/ · https://docs.djangoproject.com/en/5.2/topics/http/sessions/ · https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
