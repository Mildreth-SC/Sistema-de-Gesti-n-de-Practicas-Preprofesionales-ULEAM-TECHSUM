"""
Script de prueba para verificar la integración de Supabase Auth
Ejecutar con: python test_supabase_auth_integration.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from inscripciones.supabase_client import supabase_auth
from django.contrib.auth.models import User
from inscripciones.models import Estudiante, Carrera
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_configuration():
    """Verifica que Supabase Auth está configurado"""
    print("\n" + "="*70)
    print("🔍 VERIFICANDO CONFIGURACIÓN")
    print("="*70)
    
    if supabase_auth.is_available():
        print("✅ Supabase Auth cliente está disponible")
        print(f"   URL: {supabase_auth.supabase_url}")
    else:
        print("❌ Supabase Auth NO está configurado")
        print("   Verifica SUPABASE_URL y SUPABASE_KEY en .env")
        return False
    
    if supabase_auth.is_admin_available():
        print("✅ Supabase Auth admin cliente está disponible")
    else:
        print("⚠️  Supabase Auth admin NO está disponible")
        print("   Verifica SUPABASE_SERVICE_ROLE_KEY en .env")
    
    return True


def test_signup():
    """Prueba el registro de un usuario"""
    print("\n" + "="*70)
    print("📝 PROBANDO REGISTRO (SIGNUP)")
    print("="*70)
    
    test_email = "test.supabase@ejemplo.com"
    test_password = "TestPassword123"
    
    print(f"Intentando registrar usuario: {test_email}")
    
    result = supabase_auth.signup(
        email=test_email,
        password=test_password,
        user_metadata={
            "nombre": "Test",
            "apellido": "Supabase",
            "rol": "estudiante"
        }
    )
    
    if result['success']:
        print(f"✅ Usuario registrado exitosamente")
        print(f"   User ID: {result['user'].id}")
        print(f"   Email: {result['user'].email}")
        print(f"   Email confirmado: {result['user'].email_confirmed_at or 'Pendiente'}")
        print(f"   📧 Email de confirmación enviado: {result['email_sent']}")
        
        if result['session']:
            print(f"   Session ID: {result['session'].access_token[:20]}...")
        else:
            print("   ⚠️  No hay sesión (normal si requiere confirmación de email)")
        
        return True
    else:
        print(f"❌ Error al registrar: {result['message']}")
        
        # Si el error es que ya existe, no es crítico
        if "already registered" in result['message'].lower():
            print("   ℹ️  El usuario ya existe (esto es OK para pruebas)")
            return True
        
        return False


def test_signin():
    """Prueba el inicio de sesión"""
    print("\n" + "="*70)
    print("🔐 PROBANDO LOGIN (SIGNIN)")
    print("="*70)
    
    test_email = "test.supabase@ejemplo.com"
    test_password = "TestPassword123"
    
    print(f"Intentando login con: {test_email}")
    
    result = supabase_auth.signin(
        email=test_email,
        password=test_password
    )
    
    if result['success']:
        print(f"✅ Login exitoso")
        print(f"   User ID: {result['user'].id}")
        print(f"   Email: {result['user'].email}")
        print(f"   Access Token: {result['access_token'][:30]}...")
        print(f"   Refresh Token: {result['refresh_token'][:30]}...")
        
        # Guardar tokens para otras pruebas
        return {
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token']
        }
    else:
        print(f"❌ Error al hacer login: {result['message']}")
        
        # Si el error es email no confirmado, es normal
        if "email" in result['message'].lower() and "confirm" in result['message'].lower():
            print("   ℹ️  Email no confirmado (esto es normal si no has confirmado el email)")
            print("   📧 Revisa tu bandeja de entrada para confirmar el email")
        
        return None


def test_password_reset():
    """Prueba el restablecimiento de contraseña"""
    print("\n" + "="*70)
    print("🔑 PROBANDO RESTABLECIMIENTO DE CONTRASEÑA")
    print("="*70)
    
    test_email = "test.supabase@ejemplo.com"
    
    print(f"Enviando email de recuperación a: {test_email}")
    
    result = supabase_auth.send_password_reset_email(test_email)
    
    if result['success']:
        print(f"✅ Email de recuperación enviado")
        print(f"   Mensaje: {result['message']}")
        print("   📧 Revisa tu bandeja de entrada")
        return True
    else:
        print(f"❌ Error: {result['message']}")
        return False


def test_get_user(access_token):
    """Prueba obtener información del usuario"""
    print("\n" + "="*70)
    print("👤 PROBANDO GET USER")
    print("="*70)
    
    if not access_token:
        print("⚠️  No hay access_token disponible, saltando prueba")
        return False
    
    print("Obteniendo información del usuario...")
    
    user = supabase_auth.get_user(access_token)
    
    if user:
        print(f"✅ Usuario obtenido")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Metadata: {user.user_metadata}")
        return True
    else:
        print("❌ No se pudo obtener el usuario")
        return False


def test_refresh_session(refresh_token):
    """Prueba refrescar la sesión"""
    print("\n" + "="*70)
    print("🔄 PROBANDO REFRESH SESSION")
    print("="*70)
    
    if not refresh_token:
        print("⚠️  No hay refresh_token disponible, saltando prueba")
        return False
    
    print("Refrescando sesión...")
    
    result = supabase_auth.refresh_session(refresh_token)
    
    if result['success']:
        print(f"✅ Sesión refrescada")
        print(f"   Nuevo Access Token: {result['access_token'][:30]}...")
        return True
    else:
        print(f"❌ Error al refrescar: {result['message']}")
        return False


def test_django_integration():
    """Verifica la integración con Django"""
    print("\n" + "="*70)
    print("🔗 VERIFICANDO INTEGRACIÓN CON DJANGO")
    print("="*70)
    
    test_email = "test.supabase@ejemplo.com"
    
    # Verificar si el usuario de Django existe
    try:
        django_user = User.objects.get(email=test_email)
        print(f"✅ Usuario Django encontrado")
        print(f"   Username: {django_user.username}")
        print(f"   Email: {django_user.email}")
        print(f"   Is Active: {django_user.is_active}")
        print(f"   Is Staff: {django_user.is_staff}")
        
        # Verificar perfil de estudiante
        if hasattr(django_user, 'estudiante'):
            print(f"✅ Perfil de Estudiante encontrado")
            print(f"   Cédula: {django_user.estudiante.cedula or 'No especificada'}")
            print(f"   Carrera: {django_user.estudiante.carrera or 'No especificada'}")
        else:
            print("   ℹ️  No tiene perfil de Estudiante")
        
        return True
        
    except User.DoesNotExist:
        print(f"⚠️  Usuario Django NO encontrado para {test_email}")
        print("   Esto es normal si el usuario no ha confirmado su email")
        print("   El usuario se creará automáticamente al confirmar el email")
        return False


def main():
    """Función principal"""
    print("\n" + "="*70)
    print(" 🧪 TEST DE INTEGRACIÓN SUPABASE AUTH")
    print("="*70)
    print()
    
    # 1. Verificar configuración
    if not test_configuration():
        print("\n❌ Configuración incorrecta. Abortando pruebas.")
        return
    
    # 2. Probar registro
    test_signup()
    
    # 3. Probar login
    tokens = test_signin()
    
    # 4. Probar obtener usuario (si hay tokens)
    if tokens:
        test_get_user(tokens['access_token'])
        test_refresh_session(tokens['refresh_token'])
    
    # 5. Probar restablecimiento de contraseña
    test_password_reset()
    
    # 6. Verificar integración con Django
    test_django_integration()
    
    # Resumen final
    print("\n" + "="*70)
    print(" 📋 RESUMEN")
    print("="*70)
    print()
    print("Si ves errores de 'Email not confirmed':")
    print("  ✅ Es NORMAL - significa que Supabase está funcionando correctamente")
    print("  📧 Revisa tu bandeja de entrada para confirmar el email")
    print("  🔗 Después de confirmar, vuelve a ejecutar este script")
    print()
    print("Próximos pasos:")
    print("  1. Configura el Dashboard de Supabase (ver PASO_1_CONFIGURAR_SUPABASE_AUTH.md)")
    print("  2. Confirma tu email de prueba")
    print("  3. Vuelve a ejecutar este script")
    print("  4. Prueba el flujo completo en el navegador")
    print()
    print("="*70)


if __name__ == '__main__':
    main()
