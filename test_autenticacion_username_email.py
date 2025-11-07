"""
Script de prueba para el sistema de autenticación con username o email
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from inscripciones.models import Estudiante, Carrera


def test_autenticacion_username_email():
    print("=" * 80)
    print("PRUEBA DE AUTENTICACIÓN CON USERNAME Y EMAIL")
    print("=" * 80)
    
    # 1. Limpiar datos previos
    print("\n1. Limpiando datos previos...")
    User.objects.filter(username__in=['testuser', 'test@example.com']).delete()
    Carrera.objects.filter(codigo='TEST').delete()
    print("   ✓ Limpieza completada")
    
    # 2. Crear carrera de prueba
    print("\n2. Creando carrera de prueba...")
    carrera = Carrera.objects.create(
        nombre='Ingeniería de Prueba',
        codigo='TEST'
    )
    print(f"   ✓ Carrera creada: {carrera.nombre}")
    
    # 3. Crear usuario de prueba
    print("\n3. Creando usuario de prueba...")
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
    
    # Crear perfil de estudiante
    estudiante = Estudiante.objects.create(
        user=user,
        codigo_estudiante='E2024TEST',
        carrera=carrera,
        ciclo_actual=5
    )
    
    print(f"   ✓ Usuario creado:")
    print(f"      - Username: {user.username}")
    print(f"      - Email: {user.email}")
    print(f"      - Nombre: {user.get_full_name()}")
    
    # 4. Probar autenticación con USERNAME
    print("\n4. Probando autenticación con USERNAME...")
    auth_user = authenticate(username='testuser', password='testpass123')
    
    if auth_user is not None:
        print(f"   ✓ Autenticación exitosa con username")
        print(f"      - Usuario autenticado: {auth_user.username}")
        print(f"      - Email: {auth_user.email}")
    else:
        print(f"   ✗ ERROR: Fallo la autenticación con username")
        return False
    
    # 5. Probar autenticación con EMAIL
    print("\n5. Probando autenticación con EMAIL...")
    auth_user = authenticate(username='test@example.com', password='testpass123')
    
    if auth_user is not None:
        print(f"   ✓ Autenticación exitosa con email")
        print(f"      - Usuario autenticado: {auth_user.username}")
        print(f"      - Email: {auth_user.email}")
    else:
        print(f"   ✗ ERROR: Fallo la autenticación con email")
        return False
    
    # 6. Probar con contraseña incorrecta
    print("\n6. Probando con contraseña incorrecta...")
    auth_user = authenticate(username='testuser', password='wrongpassword')
    
    if auth_user is None:
        print(f"   ✓ Correcto: No se autenticó con contraseña incorrecta")
    else:
        print(f"   ✗ ERROR: Se autenticó con contraseña incorrecta!")
        return False
    
    # 7. Probar con usuario inexistente
    print("\n7. Probando con usuario inexistente...")
    auth_user = authenticate(username='noexiste', password='testpass123')
    
    if auth_user is None:
        print(f"   ✓ Correcto: No se autenticó con usuario inexistente")
    else:
        print(f"   ✗ ERROR: Se autenticó con usuario inexistente!")
        return False
    
    # 8. Probar con email inexistente
    print("\n8. Probando con email inexistente...")
    auth_user = authenticate(username='noexiste@example.com', password='testpass123')
    
    if auth_user is None:
        print(f"   ✓ Correcto: No se autenticó con email inexistente")
    else:
        print(f"   ✗ ERROR: Se autenticó con email inexistente!")
        return False
    
    # 9. Probar case-insensitive
    print("\n9. Probando case-insensitive (mayúsculas/minúsculas)...")
    
    # Con username en mayúsculas
    auth_user = authenticate(username='TESTUSER', password='testpass123')
    if auth_user is not None:
        print(f"   ✓ Autenticación exitosa con username en MAYÚSCULAS")
    else:
        print(f"   ✗ ERROR: Fallo con username en mayúsculas")
        return False
    
    # Con email en mayúsculas
    auth_user = authenticate(username='TEST@EXAMPLE.COM', password='testpass123')
    if auth_user is not None:
        print(f"   ✓ Autenticación exitosa con email en MAYÚSCULAS")
    else:
        print(f"   ✗ ERROR: Fallo con email en mayúsculas")
        return False
    
    # 10. Limpiar datos de prueba
    print("\n10. Limpiando datos de prueba...")
    Estudiante.objects.filter(user=user).delete()
    User.objects.filter(username='testuser').delete()
    Carrera.objects.filter(codigo='TEST').delete()
    print("   ✓ Datos de prueba eliminados")
    
    print("\n" + "=" * 80)
    print("✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    print("=" * 80)
    print("\nResumen:")
    print("✓ Autenticación con username funciona correctamente")
    print("✓ Autenticación con email funciona correctamente")
    print("✓ Contraseñas incorrectas son rechazadas")
    print("✓ Usuarios inexistentes son rechazados")
    print("✓ Sistema es case-insensitive (no distingue mayúsculas/minúsculas)")
    print("\n¡El sistema de autenticación está listo para usar!")
    
    return True


if __name__ == '__main__':
    try:
        test_autenticacion_username_email()
    except Exception as e:
        print(f"\n✗ ERROR EN LA PRUEBA: {e}")
        import traceback
        traceback.print_exc()
