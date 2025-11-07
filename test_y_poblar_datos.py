"""
Script para probar conexión a Supabase y poblar datos de prueba
"""
import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from inscripciones.models import (
    Carrera, Estudiante, Empresa, Facultad, 
    Practica, PracticaInterna, Inscripcion, InscripcionInterna
)

def test_conexion():
    """Test de conexión a la base de datos"""
    print("\n" + "="*60)
    print("TEST DE CONEXIÓN A SUPABASE")
    print("="*60)
    
    try:
        connection.ensure_connection()
        cursor = connection.cursor()
        
        # Verificar conexión
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"[OK] Conexion exitosa!")
        print(f"   PostgreSQL: {version[0][:50]}...")
        
        # Contar tablas
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        num_tablas = cursor.fetchone()[0]
        print(f"   Tablas en la base de datos: {num_tablas}")
        
        # Listar tablas principales
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'inscripciones_%'
            ORDER BY table_name
        """)
        tablas = cursor.fetchall()
        print(f"   Tablas de la aplicacion: {len(tablas)}")
        for tabla in tablas[:5]:
            print(f"     - {tabla[0]}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error de conexion: {e}")
        return False

def crear_carreras():
    """Crear carreras de prueba"""
    print("\n" + "="*60)
    print("CREANDO CARRERAS")
    print("="*60)
    
    carreras_data = [
        {
            'nombre': 'Ingeniería en Sistemas',
            'codigo': 'SIST',
            'descripcion': 'Carrera de Ingeniería en Sistemas de Información'
        },
        {
            'nombre': 'Ingeniería en Software',
            'codigo': 'SOFT',
            'descripcion': 'Carrera de Ingeniería en Software'
        },
        {
            'nombre': 'Administración de Empresas',
            'codigo': 'ADM',
            'descripcion': 'Carrera de Administración de Empresas'
        },
        {
            'nombre': 'Contabilidad',
            'codigo': 'CONT',
            'descripcion': 'Carrera de Contabilidad y Auditoría'
        },
        {
            'nombre': 'Turismo',
            'codigo': 'TUR',
            'descripcion': 'Carrera de Turismo y Hotelería'
        },
    ]
    
    carreras_creadas = []
    for data in carreras_data:
        carrera, created = Carrera.objects.get_or_create(
            codigo=data['codigo'],
            defaults=data
        )
        if created:
            print(f"[OK] Carrera creada: {carrera.nombre} ({carrera.codigo})")
            carreras_creadas.append(carrera)
        else:
            print(f"[INFO] Carrera ya existe: {carrera.nombre}")
    
    return carreras_creadas

def crear_facultades():
    """Crear facultades de prueba"""
    print("\n" + "="*60)
    print("CREANDO FACULTADES")
    print("="*60)
    
    facultades_data = [
        {
            'nombre': 'Facultad de Ciencias Informáticas',
            'codigo': 'FCI',
            'decano': 'Dr. Juan Pérez',
            'direccion': 'Av. Principal, Campus ULEAM',
            'telefono': '0987654321',
            'email': 'fci@uleam.edu.ec',
            'contacto_responsable': 'Ing. María González',
            'descripcion': 'Facultad especializada en tecnologías de la información'
        },
        {
            'nombre': 'Facultad de Ciencias Administrativas',
            'codigo': 'FCA',
            'decano': 'Dra. Ana Martínez',
            'direccion': 'Av. Principal, Campus ULEAM',
            'telefono': '0987654322',
            'email': 'fca@uleam.edu.ec',
            'contacto_responsable': 'Lic. Carlos Ramírez',
            'descripcion': 'Facultad especializada en administración y negocios'
        },
    ]
    
    facultades_creadas = []
    for data in facultades_data:
        facultad, created = Facultad.objects.get_or_create(
            codigo=data['codigo'],
            defaults=data
        )
        if created:
            print(f"[OK] Facultad creada: {facultad.nombre}")
            facultades_creadas.append(facultad)
        else:
            print(f"[INFO] Facultad ya existe: {facultad.nombre}")
    
    return facultades_creadas

def crear_empresas():
    """Crear empresas de prueba"""
    print("\n" + "="*60)
    print("CREANDO EMPRESAS")
    print("="*60)
    
    empresas_data = [
        {
            'nombre': 'TechSolutions Ecuador',
            'ruc': '17901234560',
            'direccion': 'Av. 9 de Octubre, Guayaquil',
            'telefono': '0987654321',
            'email': 'contacto@techsolutions.ec',
            'contacto_responsable': 'Ing. Roberto Silva',
            'sector': 'Tecnología',
            'descripcion': 'Empresa líder en desarrollo de software'
        },
        {
            'nombre': 'Banco del Pacífico',
            'ruc': '17901234561',
            'direccion': 'Av. Kennedy, Guayaquil',
            'telefono': '0987654322',
            'email': 'practicas@bancodelpacifico.com',
            'contacto_responsable': 'Lic. Patricia López',
            'sector': 'Finanzas',
            'descripcion': 'Institución financiera reconocida'
        },
        {
            'nombre': 'Hotel Oro Verde',
            'ruc': '17901234562',
            'direccion': 'Av. Francisco de Orellana, Guayaquil',
            'telefono': '0987654323',
            'email': 'rrhh@hoteloroverde.com',
            'contacto_responsable': 'Lic. Fernando Torres',
            'sector': 'Turismo y Hotelería',
            'descripcion': 'Cadena hotelera de prestigio'
        },
    ]
    
    empresas_creadas = []
    for data in empresas_data:
        empresa, created = Empresa.objects.get_or_create(
            ruc=data['ruc'],
            defaults=data
        )
        if created:
            print(f"[OK] Empresa creada: {empresa.nombre}")
            empresas_creadas.append(empresa)
        else:
            print(f"[INFO] Empresa ya existe: {empresa.nombre}")
    
    return empresas_creadas

def crear_estudiantes(carreras):
    """Crear estudiantes de prueba"""
    print("\n" + "="*60)
    print("CREANDO ESTUDIANTES")
    print("="*60)
    
    estudiantes_data = [
        {
            'username': 'estudiante1',
            'email': 'estudiante1@uleam.edu.ec',
            'password': 'estudiante123',
            'first_name': 'Carlos',
            'last_name': 'Mendoza',
            'codigo_estudiante': 'EST001',
            'carrera': carreras[0] if carreras else None,
            'ciclo_actual': 7,
            'telefono': '0987654321',
            'direccion': 'Guayaquil, Ecuador'
        },
        {
            'username': 'estudiante2',
            'email': 'estudiante2@uleam.edu.ec',
            'password': 'estudiante123',
            'first_name': 'María',
            'last_name': 'García',
            'codigo_estudiante': 'EST002',
            'carrera': carreras[0] if carreras else None,
            'ciclo_actual': 8,
            'telefono': '0987654322',
            'direccion': 'Manta, Ecuador'
        },
        {
            'username': 'estudiante3',
            'email': 'estudiante3@uleam.edu.ec',
            'password': 'estudiante123',
            'first_name': 'José',
            'last_name': 'Rodríguez',
            'codigo_estudiante': 'EST003',
            'carrera': carreras[1] if len(carreras) > 1 else None,
            'ciclo_actual': 6,
            'telefono': '0987654323',
            'direccion': 'Portoviejo, Ecuador'
        },
    ]
    
    estudiantes_creados = []
    for data in estudiantes_data:
        if not data['carrera']:
            print(f"[INFO] No hay carreras disponibles, saltando estudiantes")
            break
        
        user, user_created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        )
        
        if user_created:
            user.set_password(data['password'])
            user.save()
        
        estudiante, created = Estudiante.objects.get_or_create(
            codigo_estudiante=data['codigo_estudiante'],
            defaults={
                'user': user,
                'carrera': data['carrera'],
                'ciclo_actual': data['ciclo_actual'],
                'telefono': data['telefono'],
                'direccion': data['direccion']
            }
        )
        
        if created:
            print(f"[OK] Estudiante creado: {estudiante}")
            print(f"   Username: {data['username']} | Password: {data['password']}")
            estudiantes_creados.append(estudiante)
        else:
            print(f"[INFO] Estudiante ya existe: {estudiante}")
    
    return estudiantes_creados

def crear_practicas(empresas):
    """Crear prácticas de prueba"""
    print("\n" + "="*60)
    print("CREANDO PRÁCTICAS")
    print("="*60)
    
    if not empresas:
        print("[INFO] No hay empresas disponibles")
        return []
    
    fecha_inicio = timezone.now().date() + timedelta(days=30)
    fecha_fin = fecha_inicio + timedelta(weeks=16)
    fecha_limite = fecha_inicio - timedelta(days=7)
    
    practicas_data = [
        {
            'empresa': empresas[0],
            'titulo': 'Desarrollador Full Stack',
            'descripcion': 'Práctica profesional en desarrollo de aplicaciones web completas',
            'requisitos': 'Conocimientos en Python, Django, JavaScript, React, Base de datos',
            'duracion_semanas': 16,
            'horas_semana': 20,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'cupos_disponibles': 3,
            'cupos_totales': 3,
            'fecha_limite_inscripcion': timezone.make_aware(datetime.combine(fecha_limite, datetime.min.time()))
        },
        {
            'empresa': empresas[1],
            'titulo': 'Análisis de Datos Financieros',
            'descripcion': 'Práctica en análisis de datos y reportes financieros',
            'requisitos': 'Conocimientos en Excel avanzado, SQL, Análisis de datos',
            'duracion_semanas': 12,
            'horas_semana': 15,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'cupos_disponibles': 2,
            'cupos_totales': 2,
            'fecha_limite_inscripcion': timezone.make_aware(datetime.combine(fecha_limite, datetime.min.time()))
        },
    ]
    
    practicas_creadas = []
    for data in practicas_data:
        practica, created = Practica.objects.get_or_create(
            empresa=data['empresa'],
            titulo=data['titulo'],
            defaults=data
        )
        if created:
            print(f"[OK] Practica creada: {practica.titulo}")
            practicas_creadas.append(practica)
        else:
            print(f"[INFO] Practica ya existe: {practica.titulo}")
    
    return practicas_creadas

def crear_practicas_internas(facultades):
    """Crear prácticas internas de prueba"""
    print("\n" + "="*60)
    print("CREANDO PRÁCTICAS INTERNAS")
    print("="*60)
    
    if not facultades:
        print("[INFO] No hay facultades disponibles")
        return []
    
    fecha_inicio = timezone.now().date() + timedelta(days=30)
    fecha_fin = fecha_inicio + timedelta(weeks=12)
    fecha_limite = fecha_inicio - timedelta(days=7)
    
    practicas_data = [
        {
            'facultad': facultades[0],
            'titulo': 'Asistente de Investigación en IA',
            'descripcion': 'Práctica interna en proyectos de investigación sobre inteligencia artificial',
            'tipo_servicio': 'investigacion',
            'requisitos': 'Conocimientos básicos en Python, Machine Learning',
            'duracion_semanas': 12,
            'horas_semana': 15,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'cupos_disponibles': 2,
            'cupos_totales': 2,
            'fecha_limite_inscripcion': timezone.make_aware(datetime.combine(fecha_limite, datetime.min.time())),
            'beneficios': 'Experiencia en investigación, posibilidad de publicación, certificado'
        },
    ]
    
    practicas_creadas = []
    for data in practicas_data:
        practica, created = PracticaInterna.objects.get_or_create(
            facultad=data['facultad'],
            titulo=data['titulo'],
            defaults=data
        )
        if created:
            print(f"[OK] Practica interna creada: {practica.titulo}")
            practicas_creadas.append(practica)
        else:
            print(f"[INFO] Practica interna ya existe: {practica.titulo}")
    
    return practicas_creadas

def crear_inscripciones(estudiantes, practicas):
    """Crear inscripciones de prueba"""
    print("\n" + "="*60)
    print("CREANDO INSCRIPCIONES")
    print("="*60)
    
    if not estudiantes:
        print("[INFO] No hay estudiantes disponibles")
        return []
    
    if not practicas:
        print("[INFO] No hay practicas disponibles")
        return []
    
    inscripciones_creadas = []
    for i, estudiante in enumerate(estudiantes[:min(2, len(practicas))]):
        if i < len(practicas):
            inscripcion, created = Inscripcion.objects.get_or_create(
                estudiante=estudiante,
                practica=practicas[i],
                defaults={
                    'estado': 'pendiente',
                    'observaciones': 'Inscripcion de prueba'
                }
            )
            if created:
                print(f"[OK] Inscripcion creada: {estudiante} -> {practicas[i].titulo}")
                inscripciones_creadas.append(inscripcion)
            else:
                print(f"[INFO] Inscripcion ya existe: {estudiante} -> {practicas[i].titulo}")
    
    return inscripciones_creadas

def crear_inscripciones_internas(estudiantes, practicas_internas):
    """Crear inscripciones internas de prueba"""
    print("\n" + "="*60)
    print("CREANDO INSCRIPCIONES INTERNAS")
    print("="*60)
    
    if not practicas_internas:
        print("[INFO] No hay practicas internas disponibles")
        return []
    
    inscripciones_creadas = []
    if estudiantes:
        inscripcion, created = InscripcionInterna.objects.get_or_create(
            estudiante=estudiantes[0],
            practica_interna=practicas_internas[0],
            defaults={
                'estado': 'pendiente',
                'observaciones': 'Inscripcion interna de prueba'
            }
        )
        if created:
            print(f"[OK] Inscripcion interna creada: {estudiantes[0]} -> {practicas_internas[0].titulo}")
            inscripciones_creadas.append(inscripcion)
        else:
            print(f"[INFO] Inscripcion interna ya existe")
    
    return inscripciones_creadas

def mostrar_resumen():
    """Mostrar resumen de datos"""
    print("\n" + "="*60)
    print("RESUMEN DE DATOS EN SUPABASE")
    print("="*60)
    
    print(f"\nESTADISTICAS:")
    print(f"   Carreras: {Carrera.objects.count()}")
    print(f"   Facultades: {Facultad.objects.count()}")
    print(f"   Empresas: {Empresa.objects.count()}")
    print(f"   Estudiantes: {Estudiante.objects.count()}")
    print(f"   Practicas: {Practica.objects.count()}")
    print(f"   Practicas Internas: {PracticaInterna.objects.count()}")
    print(f"   Inscripciones: {Inscripcion.objects.count()}")
    print(f"   Inscripciones Internas: {InscripcionInterna.objects.count()}")
    print(f"   Usuarios: {User.objects.count()}")
    
    print(f"\nCREDENCIALES DE PRUEBA:")
    print(f"   Admin: admin / admin123")
    estudiantes = Estudiante.objects.all()[:3]
    for est in estudiantes:
        print(f"   Estudiante: {est.user.username} / estudiante123")

if __name__ == '__main__':
    # Test de conexión
    if not test_conexion():
        print("\n[ERROR] No se pudo conectar a la base de datos. Abortando...")
        exit(1)
    
    # Crear datos
    crear_carreras()
    crear_facultades()
    crear_empresas()
    
    # Obtener todas las carreras, facultades y empresas (no solo las recién creadas)
    carreras = list(Carrera.objects.all())
    facultades = list(Facultad.objects.all())
    empresas = list(Empresa.objects.all())
    
    crear_estudiantes(carreras)
    crear_practicas(empresas)
    crear_practicas_internas(facultades)
    
    # Obtener todos los estudiantes y prácticas (no solo las recién creadas)
    estudiantes = list(Estudiante.objects.all())
    practicas = list(Practica.objects.all())
    practicas_internas = list(PracticaInterna.objects.all())
    
    inscripciones = crear_inscripciones(estudiantes, practicas)
    inscripciones_internas = crear_inscripciones_internas(estudiantes, practicas_internas)
    
    # Mostrar resumen
    mostrar_resumen()
    
    print("\n" + "="*60)
    print("[OK] PROCESO COMPLETADO EXITOSAMENTE")
    print("="*60 + "\n")

