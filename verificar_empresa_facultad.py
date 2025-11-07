# -*- coding: utf-8 -*-
"""
Script de verificación: Empresas y Facultades
"""
from django.contrib.auth.models import User
from inscripciones.models import Empresa, Facultad, Practica, PracticaInterna

print("\n" + "="*70)
print("VERIFICACIÓN DE CONFIGURACIÓN: EMPRESAS Y FACULTADES")
print("="*70)

# Verificar empresas
print("\n📊 EMPRESAS:")
print("-" * 70)
empresas = Empresa.objects.all()
empresas_con_user = Empresa.objects.filter(user__isnull=False)
print(f"Total empresas: {empresas.count()}")
print(f"Empresas con usuario: {empresas_con_user.count()}")

for empresa in empresas_con_user[:3]:  # Mostrar solo 3 de ejemplo
    print(f"\n  ✅ {empresa.nombre}")
    print(f"     Username: {empresa.user.username}")
    print(f"     Email: {empresa.email}")
    print(f"     Prácticas publicadas: {Practica.objects.filter(empresa=empresa).count()}")

# Verificar facultades
print("\n\n🎓 FACULTADES:")
print("-" * 70)
facultades = Facultad.objects.all()
facultades_con_user = Facultad.objects.filter(user__isnull=False)
print(f"Total facultades: {facultades.count()}")
print(f"Facultades con usuario: {facultades_con_user.count()}")

for facultad in facultades_con_user[:3]:  # Mostrar solo 3 de ejemplo
    print(f"\n  ✅ {facultad.nombre}")
    print(f"     Username: {facultad.user.username}")
    print(f"     Email: {facultad.email}")
    print(f"     Prácticas internas: {PracticaInterna.objects.filter(facultad=facultad).count()}")

# Verificar prácticas existentes
print("\n\n💼 PRÁCTICAS:")
print("-" * 70)
total_practicas = Practica.objects.count()
total_practicas_internas = PracticaInterna.objects.count()
print(f"Total prácticas externas: {total_practicas}")
print(f"Total prácticas internas: {total_practicas_internas}")

# Verificar que las relaciones funcionan
print("\n\n🔗 VERIFICACIÓN DE RELACIONES:")
print("-" * 70)

# Probar acceso desde User a Empresa
try:
    test_empresa_user = User.objects.filter(empresa__isnull=False).first()
    if test_empresa_user:
        empresa = test_empresa_user.empresa
        print(f"✅ User -> Empresa: {test_empresa_user.username} es de {empresa.nombre}")
    else:
        print("⚠️  No hay usuarios de empresa para probar")
except Exception as e:
    print(f"❌ Error User -> Empresa: {e}")

# Probar acceso desde User a Facultad
try:
    test_facultad_user = User.objects.filter(facultad__isnull=False).first()
    if test_facultad_user:
        facultad = test_facultad_user.facultad
        print(f"✅ User -> Facultad: {test_facultad_user.username} es de {facultad.nombre}")
    else:
        print("⚠️  No hay usuarios de facultad para probar")
except Exception as e:
    print(f"❌ Error User -> Facultad: {e}")

# Verificar que estudiantes no tienen relación con empresa/facultad
try:
    test_estudiante = User.objects.filter(estudiante__isnull=False).first()
    if test_estudiante:
        tiene_empresa = hasattr(test_estudiante, 'empresa')
        tiene_facultad = hasattr(test_estudiante, 'facultad')
        if not tiene_empresa and not tiene_facultad:
            print(f"✅ Estudiante sin empresa/facultad: {test_estudiante.username}")
        else:
            print(f"⚠️  Estudiante con relaciones inesperadas")
except Exception as e:
    print(f"⚠️  Error verificando estudiante: {e}")

# Resumen de URLs disponibles
print("\n\n🌐 URLS DISPONIBLES:")
print("-" * 70)
print("\nPara Empresas:")
print("  • /empresa/panel/ - Panel de control")
print("  • /empresa/practicas/ - Mis prácticas")
print("  • /empresa/practicas/crear/ - Crear práctica")
print("  • /empresa/practicas/<id>/postulantes/ - Ver postulantes")

print("\nPara Facultades:")
print("  • /facultad/panel/ - Panel de control")
print("  • /facultad/practicas/ - Mis prácticas internas")
print("  • /facultad/practicas/crear/ - Crear práctica interna")
print("  • /facultad/practicas/<id>/postulantes/ - Ver postulantes")

print("\n\n" + "="*70)
print("✨ VERIFICACIÓN COMPLETADA")
print("="*70)

print("\n📋 CREDENCIALES DE PRUEBA:")
print("\nEmpresa:")
print("  Username: empresa_1790123456001")
print("  Password: empresa123")

print("\nFacultad:")
print("  Username: facultad_fci")
print("  Password: facultad123")

print("\nEstudiante:")
print("  Username: estudiante1")
print("  Password: estudiante123")

print("\n" + "="*70 + "\n")
