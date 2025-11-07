"""
Prueba completa del sistema:
1. Autenticación con Supabase
2. Lógica de inscripción única (un estudiante = una práctica aprobada)

Ejecutar con: python test_sistema_completo.py
"""
import os
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.contrib.auth.models import User
from inscripciones.models import (
    Estudiante, Empresa, Facultad, Carrera, 
    Practica, Inscripcion, PracticaInterna, InscripcionInterna
)
from inscripciones.supabase_client import supabase_auth
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def print_separator(title):
    """Imprime un separador con título"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def test_supabase_config():
    """Verifica la configuración de Supabase"""
    print_separator("🔍 VERIFICANDO CONFIGURACIÓN DE SUPABASE")
    
    if supabase_auth.is_available():
        print("✅ Supabase Auth cliente está disponible")
        print(f"   📍 URL: {supabase_auth.supabase_url}")
        print("✅ SUPABASE_KEY configurada")
    else:
        print("❌ Supabase Auth NO está configurado")
        print("   💡 Asegúrate de que SUPABASE_URL y SUPABASE_KEY están en .env")
        return False
    
    if supabase_auth.is_admin_available():
        print("✅ SUPABASE_SERVICE_ROLE_KEY configurada")
    else:
        print("⚠️  SUPABASE_SERVICE_ROLE_KEY no configurada")
    
    return True


def test_inscripcion_unica():
    """Prueba la lógica de inscripción única por estudiante"""
    print_separator("🎓 PROBANDO LÓGICA DE INSCRIPCIÓN ÚNICA")
    
    # Limpiar datos de prueba previos
    print("\n🧹 Limpiando datos de prueba anteriores...")
    Inscripcion.objects.filter(estudiante__user__email__startswith='test_').delete()
    InscripcionInterna.objects.filter(estudiante__user__email__startswith='test_').delete()
    Practica.objects.filter(titulo__startswith='[TEST]').delete()
    PracticaInterna.objects.filter(titulo__startswith='[TEST]').delete()
    Estudiante.objects.filter(user__email__startswith='test_').delete()
    User.objects.filter(email__startswith='test_').delete()
    Empresa.objects.filter(user__email__startswith='test_empresa_').delete()
    User.objects.filter(email__startswith='test_empresa_').delete()
    Facultad.objects.filter(user__email__startswith='test_facultad_').delete()
    User.objects.filter(email__startswith='test_facultad_').delete()
    
    print("✅ Datos de prueba anteriores eliminados")
    
    # Obtener carrera existente o crear una de prueba
    print("\n📚 Obteniendo carrera de prueba...")
    try:
        # Intentar obtener una carrera existente
        carrera = Carrera.objects.first()
        if not carrera:
            # Si no hay ninguna, crear una con código único
            carrera = Carrera.objects.create(
                nombre='TEST - Ingeniería en Sistemas',
                codigo='TEST_IS'
            )
        print(f"✅ Carrera: {carrera.nombre} (Código: {carrera.codigo})")
    except Exception as e:
        print(f"❌ Error al obtener/crear carrera: {e}")
        return False
    
    # Crear estudiante de prueba
    print("\n👨‍🎓 Creando estudiante de prueba...")
    user_estudiante = User.objects.create_user(
        username='test_estudiante_001',
        email='test_estudiante@test.com',
        password='TestPass123!'
    )
    estudiante = Estudiante.objects.create(
        user=user_estudiante,
        codigo_estudiante='TEST001',
        carrera=carrera,
        ciclo_actual=5,
        telefono='0987654321'
    )
    print(f"✅ Estudiante creado: {estudiante.user.email}")
    
    # Crear empresa de prueba
    print("\n🏢 Creando empresa de prueba...")
    user_empresa = User.objects.create_user(
        username='test_empresa_001',
        email='test_empresa@test.com',
        password='TestPass123!'
    )
    empresa = Empresa.objects.create(
        user=user_empresa,
        nombre='Empresa Test S.A.',
        ruc='0123456789',
        direccion='Calle Test 123',
        telefono='0987654321',
        sector='Tecnología'
    )
    print(f"✅ Empresa creada: {empresa.nombre}")
    
    # Crear facultad de prueba
    print("\n🎓 Creando facultad de prueba...")
    user_facultad = User.objects.create_user(
        username='test_facultad_001',
        email='test_facultad@test.com',
        password='TestPass123!'
    )
    facultad = Facultad.objects.create(
        user=user_facultad,
        nombre='Facultad de Ingeniería',
        codigo='FI',
        telefono='0987654321'
    )
    print(f"✅ Facultad creada: {facultad.nombre}")
    
    # Crear 3 prácticas externas
    print("\n📋 Creando 3 prácticas externas...")
    fecha_inicio = datetime.now().date() + timedelta(days=30)
    fecha_fin = fecha_inicio + timedelta(days=90)
    from django.utils import timezone
    fecha_limite = timezone.now() + timedelta(days=15)
    
    practicas = []
    for i in range(1, 4):
        practica = Practica.objects.create(
            empresa=empresa,
            titulo=f'[TEST] Práctica Externa {i}',
            descripcion=f'Descripción de práctica externa {i}',
            requisitos=f'Requisitos {i}',
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            fecha_limite_inscripcion=fecha_limite,
            cupos_disponibles=5,
            cupos_totales=5,
            duracion_semanas=12,
            horas_semana=20,
            area='tecnologia',
            modalidad='presencial',
            estado='disponible'
        )
        practicas.append(practica)
        print(f"   ✅ Práctica {i}: {practica.titulo}")
    
    # Crear 2 prácticas internas
    print("\n📋 Creando 2 prácticas internas...")
    practicas_internas = []
    for i in range(1, 3):
        practica_interna = PracticaInterna.objects.create(
            facultad=facultad,
            titulo=f'[TEST] Práctica Interna {i}',
            descripcion=f'Descripción de práctica interna {i}',
            tipo_servicio='investigacion',
            requisitos=f'Requisitos internos {i}',
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            fecha_limite_inscripcion=fecha_limite,
            cupos_disponibles=3,
            cupos_totales=3,
            duracion_semanas=12,
            horas_semana=15,
            modalidad='presencial',
            estado='disponible'
        )
        practicas_internas.append(practica_interna)
        print(f"   ✅ Práctica Interna {i}: {practica_interna.titulo}")
    
    # PASO 1: Estudiante se postula a múltiples prácticas
    print("\n" + "="*80)
    print("PASO 1: Estudiante se postula a 3 prácticas externas y 2 internas")
    print("="*80)
    
    inscripciones = []
    for i, practica in enumerate(practicas, 1):
        inscripcion = Inscripcion.objects.create(
            estudiante=estudiante,
            practica=practica,
            estado='pendiente'
        )
        inscripciones.append(inscripcion)
        print(f"   ✅ Inscripción {i}: {practica.titulo} - Estado: {inscripcion.estado}")
    
    inscripciones_internas = []
    for i, practica_interna in enumerate(practicas_internas, 1):
        inscripcion_interna = InscripcionInterna.objects.create(
            estudiante=estudiante,
            practica_interna=practica_interna,
            estado='pendiente'
        )
        inscripciones_internas.append(inscripcion_interna)
        print(f"   ✅ Inscripción Interna {i}: {practica_interna.titulo} - Estado: {inscripcion_interna.estado}")
    
    print(f"\n📊 Total de postulaciones: {len(inscripciones) + len(inscripciones_internas)}")
    
    # PASO 2: Empresa aprueba la primera práctica
    print("\n" + "="*80)
    print("PASO 2: Empresa aprueba la Práctica Externa 1")
    print("="*80)
    
    inscripcion_aprobada = inscripciones[0]
    print(f"🔄 Cambiando estado de '{inscripcion_aprobada.practica.titulo}' a APROBADA...")
    inscripcion_aprobada.estado = 'aprobada'
    inscripcion_aprobada.save()
    
    print(f"✅ Estado actualizado: {inscripcion_aprobada.estado}")
    
    # PASO 3: Verificar auto-cancelación
    print("\n" + "="*80)
    print("PASO 3: Verificar que las demás postulaciones se cancelaron automáticamente")
    print("="*80)
    
    # Refrescar inscripciones desde la BD
    for inscripcion in inscripciones:
        inscripcion.refresh_from_db()
    for inscripcion_interna in inscripciones_internas:
        inscripcion_interna.refresh_from_db()
    
    print("\n📋 Estado de inscripciones EXTERNAS:")
    canceladas_externas = 0
    for i, inscripcion in enumerate(inscripciones, 1):
        estado_icon = "✅" if inscripcion.estado == 'aprobada' else "❌" if inscripcion.estado == 'cancelada' else "⏳"
        print(f"   {estado_icon} Práctica {i}: {inscripcion.estado.upper()}")
        if inscripcion.estado == 'cancelada':
            canceladas_externas += 1
    
    print("\n📋 Estado de inscripciones INTERNAS:")
    canceladas_internas = 0
    for i, inscripcion_interna in enumerate(inscripciones_internas, 1):
        estado_icon = "❌" if inscripcion_interna.estado == 'cancelada' else "⏳"
        print(f"   {estado_icon} Práctica Interna {i}: {inscripcion_interna.estado.upper()}")
        if inscripcion_interna.estado == 'cancelada':
            canceladas_internas += 1
    
    # PASO 4: Verificar cupos restaurados
    print("\n" + "="*80)
    print("PASO 4: Verificar que los cupos se restauraron correctamente")
    print("="*80)
    
    for i, practica in enumerate(practicas, 1):
        practica.refresh_from_db()
        print(f"   📊 Práctica {i}: {practica.cupos_disponibles}/5 cupos disponibles")
    
    for i, practica_interna in enumerate(practicas_internas, 1):
        practica_interna.refresh_from_db()
        print(f"   📊 Práctica Interna {i}: {practica_interna.cupos_disponibles}/3 cupos disponibles")
    
    # PASO 5: Intentar nueva postulación (debe fallar)
    print("\n" + "="*80)
    print("PASO 5: Intentar nueva postulación (debe ser bloqueada)")
    print("="*80)
    
    # Verificar si ya tiene una práctica aprobada
    tiene_aprobada_externa = Inscripcion.objects.filter(
        estudiante=estudiante, 
        estado='aprobada'
    ).exists()
    
    tiene_aprobada_interna = InscripcionInterna.objects.filter(
        estudiante=estudiante, 
        estado='aprobada'
    ).exists()
    
    puede_postular = not (tiene_aprobada_externa or tiene_aprobada_interna)
    
    if puede_postular:
        print("❌ ERROR: El estudiante NO debería poder postular (tiene práctica aprobada)")
    else:
        print("✅ CORRECTO: El sistema bloquea nuevas postulaciones")
        print(f"   📌 Práctica aprobada externa: {tiene_aprobada_externa}")
        print(f"   📌 Práctica aprobada interna: {tiene_aprobada_interna}")
    
    # RESUMEN FINAL
    print("\n" + "="*80)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*80)
    
    total_canceladas = canceladas_externas + canceladas_internas
    esperadas_canceladas = len(inscripciones) + len(inscripciones_internas) - 1
    
    print(f"\n✅ Inscripciones aprobadas: 1")
    print(f"{'✅' if total_canceladas == esperadas_canceladas else '❌'} Inscripciones canceladas: {total_canceladas}/{esperadas_canceladas}")
    print(f"{'✅' if not puede_postular else '❌'} Bloqueo de nuevas postulaciones: {'Activo' if not puede_postular else 'FALLÓ'}")
    
    # Verificación final
    if total_canceladas == esperadas_canceladas and not puede_postular:
        print("\n" + "🎉"*40)
        print("✅ ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("🎉"*40)
        return True
    else:
        print("\n❌ ALGUNAS PRUEBAS FALLARON - Revisar implementación")
        return False


def main():
    """Función principal"""
    print("\n" + "🚀"*40)
    print("SISTEMA DE PRUEBAS COMPLETO")
    print("Sistema de Gestión de Prácticas Preprofesionales")
    print("🚀"*40)
    
    # Test 1: Configuración de Supabase
    if not test_supabase_config():
        print("\n⚠️  Continuando con las pruebas de inscripción...")
    
    # Test 2: Lógica de inscripción única
    resultado = test_inscripcion_unica()
    
    print("\n" + "="*80)
    print("FIN DE LAS PRUEBAS")
    print("="*80)
    
    return resultado


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
