"""
Script para verificar la configuración de egresados y prácticas
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from inscripciones.models import Estudiante, Practica, Empresa
from django.contrib.auth.models import User

print("=" * 80)
print("🔍 VERIFICACIÓN DE EGRESADOS Y PRÁCTICAS")
print("=" * 80)

# Verificar todos los estudiantes/egresados
print("\n📋 TODOS LOS USUARIOS REGISTRADOS:")
print("-" * 80)
estudiantes = Estudiante.objects.all()
for est in estudiantes:
    tipo = "🎓 ESTUDIANTE" if est.tipo_usuario == 'estudiante' else "👨‍🎓 EGRESADO"
    print(f"{tipo} | {est.user.username} | {est.user.get_full_name()} | {est.user.email}")

# Verificar prácticas dirigidas a egresados
print("\n" + "=" * 80)
print("💼 PRÁCTICAS DIRIGIDAS A EGRESADOS:")
print("-" * 80)
practicas_egresados = Practica.objects.filter(dirigido_a__in=['egresados', 'ambos'], activa=True)
if practicas_egresados.exists():
    for practica in practicas_egresados:
        empresa_nombre = practica.empresa.nombre if practica.empresa else "Sin empresa"
        print(f"• {practica.titulo}")
        print(f"  Empresa: {empresa_nombre}")
        print(f"  Dirigido a: {practica.get_dirigido_a_display()}")
        print(f"  Activa: {'✅ Sí' if practica.activa else '❌ No'}")
        print(f"  Fecha límite: {practica.fecha_limite_inscripcion}")
        print()
else:
    print("❌ No hay prácticas dirigidas a egresados")

# Verificar prácticas dirigidas a estudiantes
print("=" * 80)
print("🎓 PRÁCTICAS DIRIGIDAS A ESTUDIANTES:")
print("-" * 80)
practicas_estudiantes = Practica.objects.filter(dirigido_a__in=['estudiantes', 'ambos'], activa=True)
if practicas_estudiantes.exists():
    for practica in practicas_estudiantes:
        empresa_nombre = practica.empresa.nombre if practica.empresa else "Sin empresa"
        print(f"• {practica.titulo}")
        print(f"  Empresa: {empresa_nombre}")
        print(f"  Dirigido a: {practica.get_dirigido_a_display()}")
        print()
else:
    print("❌ No hay prácticas dirigidas a estudiantes")

# Resumen
print("=" * 80)
print("📊 RESUMEN:")
print("-" * 80)
total_estudiantes = Estudiante.objects.filter(tipo_usuario='estudiante').count()
total_egresados = Estudiante.objects.filter(tipo_usuario='egresado').count()
total_practicas_egresados = Practica.objects.filter(dirigido_a__in=['egresados', 'ambos'], activa=True).count()
total_practicas_estudiantes = Practica.objects.filter(dirigido_a__in=['estudiantes', 'ambos'], activa=True).count()

print(f"👥 Total de estudiantes activos: {total_estudiantes}")
print(f"👨‍🎓 Total de egresados: {total_egresados}")
print(f"💼 Prácticas para egresados: {total_practicas_egresados}")
print(f"🎓 Prácticas para estudiantes: {total_practicas_estudiantes}")
print("=" * 80)

# Verificar si hay campo dirigido_a con valor por defecto
print("\n⚠️  VERIFICANDO PRÁCTICAS SIN CONFIGURACIÓN ESPECÍFICA:")
print("-" * 80)
practicas_sin_config = Practica.objects.filter(activa=True).exclude(dirigido_a__in=['estudiantes', 'egresados', 'ambos'])
if practicas_sin_config.exists():
    print(f"❌ Hay {practicas_sin_config.count()} práctica(s) sin configuración específica de dirigido_a")
    for p in practicas_sin_config:
        print(f"   • {p.titulo} - dirigido_a: '{p.dirigido_a}'")
else:
    print("✅ Todas las prácticas activas tienen configuración específica")
