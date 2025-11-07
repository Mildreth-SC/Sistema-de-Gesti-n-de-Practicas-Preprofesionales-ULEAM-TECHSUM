"""
Script para crear un superusuario administrador para el sistema de prácticas ULEAM
Ejecutar con: python manage.py shell < crear_superusuario.py
"""

from django.contrib.auth.models import User

# Datos del superusuario
username = 'admin'
email = 'admin@uleam.edu.ec'
password = 'admin123'  # CAMBIAR EN PRODUCCIÓN
first_name = 'Administrador'
last_name = 'Sistema'

# Verificar si ya existe
if User.objects.filter(username=username).exists():
    print(f"❌ El usuario '{username}' ya existe.")
    user = User.objects.get(username=username)
    print(f"✅ Usuario existente: {user.username} ({user.email})")
    print(f"   - Es superusuario: {user.is_superuser}")
    print(f"   - Es staff: {user.is_staff}")
else:
    # Crear el superusuario
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    print(f"✅ Superusuario creado exitosamente!")
    print(f"   - Usuario: {username}")
    print(f"   - Email: {email}")
    print(f"   - Contraseña: {password}")
    print(f"   - Nombre: {first_name} {last_name}")
    print()
    print("🔐 IMPORTANTE: Cambia la contraseña después del primer inicio de sesión")
    print()
    print("📋 Accede al panel de administración en:")
    print("   http://127.0.0.1:8000/admin/")
    print()
    print("🎯 Credenciales:")
    print(f"   Usuario: {username}")
    print(f"   Contraseña: {password}")
