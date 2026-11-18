from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from solicitudes import views
urlpatterns = [path('admin/', admin.site.urls),
    path('cuentas/login/', auth_views.LoginView.as_view(), name='login'),
    path('cuentas/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('', views.inicio, name='inicio'),
    path('solicitudes/nueva/', views.nueva, name='nueva'),
    path('contacto/', views.contacto, name='contacto'),
    path('gestion/', views.GestionView.as_view(), name='gestion')]
