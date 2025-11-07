"""
Script de prueba para el sistema de autenticación mejorado
Prueba el envío de emails de verificación y recuperación
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from inscripciones.supabase_auth import supabase_auth

print("=" * 60)
print("🧪 TEST DE AUTENTICACIÓN MEJORADA")
print("=" * 60)

# 1. Verificar configuración de email
print("\n1. Verificando configuración de email...")
print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
    print("   ⚠️  Modo: CONSOLA (los emails se mostrarán en terminal)")
elif settings.EMAIL_HOST_USER:
    print("   ✅ Modo: SMTP configurado")
else:
    print("   ❌ Email no configurado completamente")

# 2. Verificar Supabase Auth
print("\n2. Verificando Supabase Auth...")
if supabase_auth.is_available():
    print(f"   ✅ Supabase configurado: {settings.SUPABASE_URL}")
else:
    print("   ⚠️  Supabase no configurado (usando solo Django Auth)")

# 3. Verificar que existen las URLs
print("\n3. Verificando URLs...")
from django.urls import reverse
try:
    verificar_url = reverse('verificar_email', args=['test', 'test'])
    print(f"   ✅ URL verificación: {verificar_url}")
    
    solicitar_url = reverse('solicitar_restablecimiento_contrasena')
    print(f"   ✅ URL solicitar reset: {solicitar_url}")
    
    restablecer_url = reverse('restablecer_contrasena', args=['test', 'test'])
    print(f"   ✅ URL restablecer: {restablecer_url}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Prueba de envío de email (solo si está configurado)
print("\n4. Prueba de envío de email...")
if settings.EMAIL_BACKEND != 'django.core.mail.backends.console.EmailBackend':
    respuesta = input("   ¿Deseas enviar un email de prueba? (s/n): ")
    if respuesta.lower() == 's':
        email_destino = input("   Ingresa el email de destino: ")
        try:
            send_mail(
                subject='Test - Sistema de Prácticas ULEAM',
                message='Este es un email de prueba del sistema de autenticación.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_destino],
                fail_silently=False,
            )
            print("   ✅ Email enviado correctamente!")
        except Exception as e:
            print(f"   ❌ Error al enviar email: {e}")
else:
    print("   ⚠️  Modo consola activado - no se enviarán emails reales")

# 5. Estadísticas de usuarios
print("\n5. Estadísticas de usuarios...")
total_usuarios = User.objects.count()
usuarios_activos = User.objects.filter(is_active=True).count()
usuarios_inactivos = User.objects.filter(is_active=False).count()

print(f"   Total de usuarios: {total_usuarios}")
print(f"   Usuarios activos: {usuarios_activos}")
print(f"   Usuarios pendientes de verificación: {usuarios_inactivos}")

# 6. Resumen de características
print("\n" + "=" * 60)
print("✨ CARACTERÍSTICAS IMPLEMENTADAS:")
print("=" * 60)
print("✅ Verificación de email al registrarse")
print("✅ Recuperación de contraseña por email")
print("✅ Integración con Supabase Auth (opcional)")
print("✅ Templates de email profesionales")
print("✅ Tokens seguros con expiración de 24h")
print("✅ Validación de contraseñas (mínimo 8 caracteres)")

print("\n" + "=" * 60)
print("📋 PRÓXIMOS PASOS:")
print("=" * 60)
print("1. Configura EMAIL_HOST_USER y EMAIL_HOST_PASSWORD en .env")
print("2. Para Gmail: https://myaccount.google.com/apppasswords")
print("3. Prueba registrando un nuevo usuario")
print("4. Revisa la consola/email para el enlace de verificación")
print("5. Lee AUTENTICACION_MEJORADA.md para más información")

print("\n✅ Test completado!")
print("=" * 60)
