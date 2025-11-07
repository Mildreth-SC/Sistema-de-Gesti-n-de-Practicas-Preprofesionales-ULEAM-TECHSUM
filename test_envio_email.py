"""
Script para probar la configuración de email
Permite enviar un email de prueba para verificar que todo funciona
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_config():
    """Prueba la configuración de email"""
    print("=" * 60)
    print("🧪 TEST DE CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    print()
    
    # Mostrar configuración actual
    print("📋 Configuración actual:")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER if settings.EMAIL_HOST_USER else '(no configurado)'}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    # Verificar modo
    if 'console' in settings.EMAIL_BACKEND:
        print("⚠️  MODO CONSOLA ACTIVADO")
        print("   Los emails se mostrarán aquí en la terminal, no se enviarán realmente.")
        print()
    else:
        print("✅ MODO SMTP ACTIVADO")
        
        if not settings.EMAIL_HOST_USER:
            print("❌ ERROR: EMAIL_HOST_USER no está configurado")
            print("   Por favor, configura las variables de entorno en .env")
            print()
            return False
        
        print("   Los emails se enviarán realmente.")
        print()
    
    # Preguntar si desea enviar un email de prueba
    print("=" * 60)
    respuesta = input("¿Deseas enviar un email de prueba? (s/n): ").lower()
    
    if respuesta != 's':
        print("❌ Prueba cancelada")
        return False
    
    print()
    email_destino = input("📧 Ingresa el email de destino: ").strip()
    
    if not email_destino or '@' not in email_destino:
        print("❌ Email inválido")
        return False
    
    print()
    print("📤 Enviando email de prueba...")
    print()
    
    try:
        resultado = send_mail(
            subject='🧪 Prueba de Email - Sistema de Prácticas ULEAM',
            message='''
Hola!

Este es un email de prueba del Sistema de Gestión de Prácticas Preprofesionales de la ULEAM.

Si recibes este mensaje, significa que la configuración de email está funcionando correctamente.

Características configuradas:
✅ Verificación de email al registrarse
✅ Recuperación de contraseña por email
✅ Notificaciones del sistema

Saludos,
Sistema de Prácticas ULEAM
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_destino],
            fail_silently=False,
        )
        
        if 'console' in settings.EMAIL_BACKEND:
            print("=" * 60)
            print("⚠️  El email anterior se mostró en consola (no se envió realmente)")
            print()
            print("Para enviar emails reales, configura:")
            print("1. SendGrid (recomendado): Lee CONFIGURAR_EMAIL_PRODUCCION.md")
            print("2. Gmail (alternativa): Lee GUIA_RAPIDA_EMAIL.md")
            print("=" * 60)
        else:
            print("=" * 60)
            print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
            print()
            print(f"📬 Email enviado a: {email_destino}")
            print(f"📨 Desde: {settings.DEFAULT_FROM_EMAIL}")
            print()
            print("Por favor, revisa:")
            print("1. Bandeja de entrada")
            print("2. Carpeta de spam/correo no deseado")
            print()
            
            if 'sendgrid' in settings.EMAIL_HOST:
                print("💡 Monitorea en SendGrid:")
                print("   https://app.sendgrid.com/email_activity")
            
            print("=" * 60)
        
        return True
        
    except Exception as e:
        print("=" * 60)
        print("❌ ERROR AL ENVIAR EMAIL")
        print()
        print(f"Error: {str(e)}")
        print()
        
        if 'SMTPAuthenticationError' in str(type(e).__name__):
            print("🔧 Solución:")
            print("   1. Verifica EMAIL_HOST_USER y EMAIL_HOST_PASSWORD")
            print("   2. Para SendGrid: EMAIL_HOST_USER debe ser 'apikey'")
            print("   3. Para Gmail: Usa contraseña de aplicación")
            print()
            print("📖 Guía completa: CONFIGURAR_EMAIL_PRODUCCION.md")
        
        elif 'Connection' in str(e):
            print("🔧 Solución:")
            print("   1. Verifica tu conexión a internet")
            print("   2. Revisa si el firewall bloquea el puerto 587")
            print("   3. Prueba cambiar a EMAIL_PORT=465 y EMAIL_USE_SSL=True")
        
        print("=" * 60)
        return False

if __name__ == '__main__':
    test_email_config()
