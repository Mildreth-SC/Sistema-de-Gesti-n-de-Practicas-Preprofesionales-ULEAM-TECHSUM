"""
Script para crear prácticas de prueba con diferentes configuraciones de dirigido_a
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from inscripciones.models import Practica, PracticaInterna, Empresa, Facultad
from django.utils import timezone

print("=" * 70)
print("📋 CREANDO PRÁCTICAS DE PRUEBA CON FILTRADO POR TIPO DE USUARIO")
print("=" * 70)

# Buscar empresa y facultad
empresa = Empresa.objects.filter(estado_aprobacion='aprobada').first()
facultad = Facultad.objects.filter(estado_aprobacion='aprobada').first()

if not empresa:
    print("❌ No hay empresas aprobadas")
    exit(1)

if not facultad:
    print("❌ No hay facultades aprobadas")
    exit(1)

print(f"\n✅ Usando empresa: {empresa.nombre}")
print(f"✅ Usando facultad: {facultad.nombre}")

# Crear práctica para SOLO ESTUDIANTES
practica_estudiantes = Practica.objects.create(
    empresa=empresa,
    titulo="Práctica de Desarrollo Web (Solo Estudiantes)",
    area="tecnologia",
    descripcion="Práctica exclusiva para estudiantes activos de sistemas",
    requisitos="Estar cursando actualmente una carrera universitaria",
    modalidad="hibrido",
    dirigido_a="estudiantes",  # ⭐ Solo estudiantes
    duracion_semanas=12,
    horas_semana=20,
    fecha_inicio=timezone.now().date() + timedelta(days=30),
    fecha_fin=timezone.now().date() + timedelta(days=114),
    cupos_disponibles=5,
    cupos_totales=5,
    fecha_limite_inscripcion=timezone.now() + timedelta(days=20)
)
print(f"\n✅ Práctica creada para ESTUDIANTES: {practica_estudiantes.titulo}")

# Crear práctica para SOLO EGRESADOS
practica_egresados = Practica.objects.create(
    empresa=empresa,
    titulo="Práctica Profesional Senior (Solo Egresados)",
    area="tecnologia",
    descripcion="Práctica exclusiva para profesionales egresados",
    requisitos="Título universitario completo (Licenciatura o Ingeniería)",
    modalidad="presencial",
    dirigido_a="egresados",  # ⭐ Solo egresados
    duracion_semanas=16,
    horas_semana=30,
    fecha_inicio=timezone.now().date() + timedelta(days=30),
    fecha_fin=timezone.now().date() + timedelta(days=142),
    cupos_disponibles=3,
    cupos_totales=3,
    fecha_limite_inscripcion=timezone.now() + timedelta(days=20)
)
print(f"✅ Práctica creada para EGRESADOS: {practica_egresados.titulo}")

# Crear práctica para AMBOS
practica_ambos = Practica.objects.create(
    empresa=empresa,
    titulo="Práctica de Soporte Técnico (Estudiantes y Egresados)",
    area="tecnologia",
    descripcion="Práctica abierta para estudiantes activos y egresados",
    requisitos="Conocimientos básicos de informática",
    modalidad="remoto",
    dirigido_a="ambos",  # ⭐ Ambos
    duracion_semanas=8,
    horas_semana=15,
    fecha_inicio=timezone.now().date() + timedelta(days=30),
    fecha_fin=timezone.now().date() + timedelta(days=86),
    cupos_disponibles=10,
    cupos_totales=10,
    fecha_limite_inscripcion=timezone.now() + timedelta(days=20)
)
print(f"✅ Práctica creada para AMBOS: {practica_ambos.titulo}")

# Crear práctica interna para SOLO ESTUDIANTES
practica_interna_estudiantes = PracticaInterna.objects.create(
    facultad=facultad,
    titulo="Práctica de Investigación (Solo Estudiantes)",
    descripcion="Proyecto de investigación exclusivo para estudiantes activos",
    tipo_servicio="investigacion",
    requisitos="Estar matriculado en la universidad",
    modalidad="presencial",
    dirigido_a="estudiantes",  # ⭐ Solo estudiantes
    duracion_semanas=10,
    horas_semana=12,
    fecha_inicio=timezone.now().date() + timedelta(days=30),
    fecha_fin=timezone.now().date() + timedelta(days=100),
    cupos_disponibles=8,
    cupos_totales=8,
    fecha_limite_inscripcion=timezone.now() + timedelta(days=15)
)
print(f"✅ Práctica interna creada para ESTUDIANTES: {practica_interna_estudiantes.titulo}")

# Crear práctica interna para EGRESADOS
practica_interna_egresados = PracticaInterna.objects.create(
    facultad=facultad,
    titulo="Programa de Docencia (Solo Egresados)",
    descripcion="Programa de formación docente para profesionales egresados",
    tipo_servicio="docencia",
    requisitos="Título universitario completo",
    modalidad="presencial",
    dirigido_a="egresados",  # ⭐ Solo egresados
    duracion_semanas=20,
    horas_semana=25,
    fecha_inicio=timezone.now().date() + timedelta(days=30),
    fecha_fin=timezone.now().date() + timedelta(days=170),
    cupos_disponibles=4,
    cupos_totales=4,
    fecha_limite_inscripcion=timezone.now() + timedelta(days=15)
)
print(f"✅ Práctica interna creada para EGRESADOS: {practica_interna_egresados.titulo}")

print("\n" + "=" * 70)
print("✅ PRÁCTICAS DE PRUEBA CREADAS EXITOSAMENTE")
print("=" * 70)

print("\n📊 RESUMEN:")
print(f"   • 3 Prácticas de empresa creadas")
print(f"   • 2 Prácticas internas creadas")
print(f"   • Total: 5 prácticas con diferentes configuraciones")

print("\n🧪 PRUEBAS A REALIZAR:")
print("   1. Inicia sesión como ESTUDIANTE (estudianteprueba / test123)")
print("      → Debe ver: Práctica de Desarrollo Web, Soporte Técnico, Investigación")
print("      → NO debe ver: Práctica Senior, Programa de Docencia")
print("")
print("   2. Registra un EGRESADO nuevo")
print("      → Debe ver: Práctica Senior, Soporte Técnico, Programa de Docencia")
print("      → NO debe ver: Práctica de Desarrollo Web, Investigación")
print("")
print("   3. Intenta inscribirte en una práctica no permitida")
print("      → Debe mostrar mensaje de error")
