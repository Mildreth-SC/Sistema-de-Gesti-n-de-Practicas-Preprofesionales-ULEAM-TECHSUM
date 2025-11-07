"""
Script para poblar la base de datos con datos de prueba
Ejecutar con: python manage.py shell < poblar_datos_prueba.py
"""

from django.contrib.auth.models import User
from inscripciones.models import (
    Carrera, Estudiante, Empresa, Practica, Inscripcion,
    Facultad, PracticaInterna, InscripcionInterna, DocumentoInscripcion
)
from django.utils import timezone
from datetime import timedelta
import random

print("=" * 60)
print("INICIANDO POBLACIÓN DE DATOS DE PRUEBA")
print("=" * 60)

# 1. CREAR CARRERAS
print("\n[1/9] Creando Carreras...")
carreras_data = [
    {"nombre": "Ingeniería en Sistemas", "codigo": "IS001", "descripcion": "Formación de profesionales en desarrollo de software y sistemas informáticos"},
    {"nombre": "Ingeniería Civil", "codigo": "IC002", "descripcion": "Formación de profesionales en diseño y construcción de infraestructuras"},
    {"nombre": "Medicina", "codigo": "MED003", "descripcion": "Formación de médicos generales y especialistas"},
    {"nombre": "Derecho", "codigo": "DER004", "descripcion": "Formación de abogados y profesionales del derecho"},
    {"nombre": "Administración de Empresas", "codigo": "AE005", "descripcion": "Formación de administradores y gestores empresariales"},
    {"nombre": "Psicología", "codigo": "PSI006", "descripcion": "Formación de psicólogos clínicos y organizacionales"},
    {"nombre": "Contabilidad y Auditoría", "codigo": "CA007", "descripcion": "Formación de contadores y auditores profesionales"},
    {"nombre": "Marketing", "codigo": "MKT008", "descripcion": "Formación de especialistas en marketing y ventas"},
]

carreras = []
for data in carreras_data:
    carrera, created = Carrera.objects.get_or_create(
        codigo=data["codigo"],
        defaults={"nombre": data["nombre"], "descripcion": data["descripcion"], "activa": True}
    )
    carreras.append(carrera)
    if created:
        print(f"  ✓ Creada: {carrera.nombre}")
    else:
        print(f"  → Existente: {carrera.nombre}")

# 2. CREAR EMPRESAS
print("\n[2/9] Creando Empresas...")
empresas_data = [
    {"nombre": "Tech Solutions Ecuador", "ruc": "1790123456001", "sector": "Tecnología", "telefono": "0987654321", "email": "contacto@techsolutions.ec", "contacto": "Juan Pérez"},
    {"nombre": "Constructora del Pacífico S.A.", "ruc": "1790234567001", "sector": "Construcción", "telefono": "0987654322", "email": "info@construpac.com", "contacto": "María González"},
    {"nombre": "Banco Nacional del Ecuador", "ruc": "1790345678001", "sector": "Financiero", "telefono": "0987654323", "email": "rrhh@banconacional.ec", "contacto": "Carlos Ramírez"},
    {"nombre": "Hospital Metropolitano", "ruc": "1790456789001", "sector": "Salud", "telefono": "0987654324", "email": "practicas@hosmetro.com", "contacto": "Ana Rodríguez"},
    {"nombre": "Estudio Jurídico Asociados", "ruc": "1790567890001", "sector": "Legal", "telefono": "0987654325", "email": "contacto@estudiojuridico.ec", "contacto": "Luis Fernández"},
    {"nombre": "Marketing Digital Pro", "ruc": "1790678901001", "sector": "Marketing", "telefono": "0987654326", "email": "info@marketingpro.ec", "contacto": "Patricia Morales"},
    {"nombre": "Grupo Empresarial Costa", "ruc": "1790789012001", "sector": "Comercio", "telefono": "0987654327", "email": "practicas@grupocosta.com", "contacto": "Roberto Silva"},
    {"nombre": "Consultoría y Auditoría CPA", "ruc": "1790890123001", "sector": "Consultoría", "telefono": "0987654328", "email": "rrhh@cpa-ec.com", "contacto": "Sandra López"},
]

empresas = []
for data in empresas_data:
    empresa, created = Empresa.objects.get_or_create(
        ruc=data["ruc"],
        defaults={
            "nombre": data["nombre"],
            "sector": data["sector"],
            "direccion": f"Av. Principal #{random.randint(100, 999)}, Manta, Ecuador",
            "telefono": data["telefono"],
            "email": data["email"],
            "contacto_responsable": data["contacto"],
            "descripcion": f"Empresa líder en el sector de {data['sector']} con más de 10 años de experiencia.",
            "activa": True
        }
    )
    empresas.append(empresa)
    if created:
        print(f"  ✓ Creada: {empresa.nombre}")
    else:
        print(f"  → Existente: {empresa.nombre}")

# 3. CREAR FACULTADES
print("\n[3/9] Creando Facultades...")
facultades_data = [
    {"nombre": "Facultad de Ciencias Informáticas", "codigo": "FCI", "decano": "Dr. Miguel Torres"},
    {"nombre": "Facultad de Ingeniería", "codigo": "FING", "decano": "Dr. Roberto Mendoza"},
    {"nombre": "Facultad de Ciencias Médicas", "codigo": "FCM", "decano": "Dra. Elena Vargas"},
    {"nombre": "Facultad de Ciencias Sociales y Derecho", "codigo": "FCSD", "decano": "Dr. Fernando Castro"},
    {"nombre": "Facultad de Ciencias Administrativas", "codigo": "FCA", "decano": "Msc. Andrea Salazar"},
]

facultades = []
for data in facultades_data:
    facultad, created = Facultad.objects.get_or_create(
        codigo=data["codigo"],
        defaults={
            "nombre": data["nombre"],
            "decano": data["decano"],
            "direccion": f"Campus Universitario, Edificio {data['codigo']}, Manta",
            "telefono": f"052{random.randint(100000, 999999)}",
            "email": f"{data['codigo'].lower()}@uleam.edu.ec",
            "contacto_responsable": data["decano"],
            "descripcion": f"Facultad dedicada a la formación académica y profesional de excelencia.",
            "activa": True
        }
    )
    facultades.append(facultad)
    if created:
        print(f"  ✓ Creada: {facultad.nombre}")
    else:
        print(f"  → Existente: {facultad.nombre}")

# 4. CREAR ESTUDIANTES
print("\n[4/9] Creando Estudiantes...")
estudiantes_data = [
    {"username": "estudiante1", "nombres": "Diego", "apellidos": "Martínez", "codigo": "2021001", "ciclo": 8},
    {"username": "estudiante2", "nombres": "Laura", "apellidos": "Sánchez", "codigo": "2021002", "ciclo": 7},
    {"username": "estudiante3", "nombres": "Carlos", "apellidos": "Ramírez", "codigo": "2021003", "ciclo": 9},
    {"username": "estudiante4", "nombres": "María", "apellidos": "Flores", "codigo": "2021004", "ciclo": 8},
    {"username": "estudiante5", "nombres": "Andrés", "apellidos": "Torres", "codigo": "2021005", "ciclo": 6},
    {"username": "estudiante6", "nombres": "Sofía", "apellidos": "Valencia", "codigo": "2021006", "ciclo": 7},
    {"username": "estudiante7", "nombres": "Pedro", "apellidos": "Mendoza", "codigo": "2021007", "ciclo": 8},
    {"username": "estudiante8", "nombres": "Valentina", "apellidos": "Castro", "codigo": "2021008", "ciclo": 9},
    {"username": "estudiante9", "nombres": "Gabriel", "apellidos": "Ruiz", "codigo": "2021009", "ciclo": 7},
    {"username": "estudiante10", "nombres": "Isabella", "apellidos": "Ortiz", "codigo": "2021010", "ciclo": 6},
]

estudiantes = []
for data in estudiantes_data:
    user, user_created = User.objects.get_or_create(
        username=data["username"],
        defaults={
            "first_name": data["nombres"],
            "last_name": data["apellidos"],
            "email": f"{data['username']}@uleam.edu.ec",
            "is_active": True
        }
    )
    if user_created:
        user.set_password("estudiante123")
        user.save()
    
    estudiante, created = Estudiante.objects.get_or_create(
        user=user,
        defaults={
            "codigo_estudiante": data["codigo"],
            "carrera": random.choice(carreras),
            "ciclo_actual": data["ciclo"],
            "telefono": f"09{random.randint(10000000, 99999999)}",
            "direccion": f"Calle {random.randint(1, 50)} y Av. Principal, Manta",
            "fecha_nacimiento": timezone.now().date() - timedelta(days=random.randint(7300, 9125)),
            "activo": True
        }
    )
    estudiantes.append(estudiante)
    if created:
        print(f"  ✓ Creado: {estudiante.user.get_full_name()} ({estudiante.codigo_estudiante})")
    else:
        print(f"  → Existente: {estudiante.user.get_full_name()}")

# 5. CREAR PRÁCTICAS
print("\n[5/9] Creando Prácticas...")
practicas_data = [
    {"titulo": "Desarrollo Web Full Stack", "empresa": 0, "duracion": 12, "horas": 40, "cupos": 3},
    {"titulo": "Asistente de Construcción", "empresa": 1, "duracion": 16, "horas": 40, "cupos": 2},
    {"titulo": "Analista Financiero Junior", "empresa": 2, "duracion": 12, "horas": 35, "cupos": 4},
    {"titulo": "Asistente Médico", "empresa": 3, "duracion": 20, "horas": 30, "cupos": 2},
    {"titulo": "Asistente Legal", "empresa": 4, "duracion": 12, "horas": 40, "cupos": 3},
    {"titulo": "Community Manager", "empresa": 5, "duracion": 10, "horas": 30, "cupos": 2},
    {"titulo": "Asistente de Ventas", "empresa": 6, "duracion": 12, "horas": 40, "cupos": 5},
    {"titulo": "Auditor Junior", "empresa": 7, "duracion": 16, "horas": 40, "cupos": 2},
]

practicas = []
for data in practicas_data:
    fecha_inicio = timezone.now().date() + timedelta(days=random.randint(30, 60))
    fecha_limite = timezone.now() + timedelta(days=random.randint(5, 25))
    
    practica, created = Practica.objects.get_or_create(
        titulo=data["titulo"],
        empresa=empresas[data["empresa"]],
        defaults={
            "descripcion": f"Oportunidad de práctica profesional en {data['titulo']}. El estudiante desarrollará competencias profesionales en un ambiente real de trabajo.",
            "requisitos": "- Estudiante regular de la carrera\n- Promedio mínimo de 80/100\n- Disponibilidad de tiempo completo\n- Proactividad y responsabilidad",
            "duracion_semanas": data["duracion"],
            "horas_semana": data["horas"],
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_inicio + timedelta(weeks=data["duracion"]),
            "cupos_disponibles": data["cupos"],
            "cupos_totales": data["cupos"],
            "estado": "disponible",
            "fecha_limite_inscripcion": fecha_limite,
            "activa": True
        }
    )
    practicas.append(practica)
    if created:
        print(f"  ✓ Creada: {practica.titulo} - {practica.empresa.nombre}")
    else:
        print(f"  → Existente: {practica.titulo}")

# 6. CREAR PRÁCTICAS INTERNAS
print("\n[6/9] Creando Prácticas Internas...")
practicas_internas_data = [
    {"titulo": "Asistente de Investigación en IA", "facultad": 0, "tipo": "investigacion", "duracion": 12, "cupos": 2},
    {"titulo": "Tutor de Programación", "facultad": 0, "tipo": "docencia", "duracion": 16, "cupos": 3},
    {"titulo": "Asistente de Laboratorio", "facultad": 1, "tipo": "tecnico", "duracion": 12, "cupos": 2},
    {"titulo": "Apoyo en Consulta Médica", "facultad": 2, "tipo": "social", "duracion": 20, "cupos": 4},
    {"titulo": "Asistente Administrativo", "facultad": 4, "tipo": "administrativo", "duracion": 12, "cupos": 3},
]

practicas_internas = []
for data in practicas_internas_data:
    fecha_inicio = timezone.now().date() + timedelta(days=random.randint(20, 50))
    fecha_limite = timezone.now() + timedelta(days=random.randint(5, 20))
    
    practica, created = PracticaInterna.objects.get_or_create(
        titulo=data["titulo"],
        facultad=facultades[data["facultad"]],
        defaults={
            "descripcion": f"Práctica interna en {data['titulo']}. Experiencia práctica dentro de la universidad.",
            "tipo_servicio": data["tipo"],
            "requisitos": "- Estudiante regular\n- Promedio mínimo de 75/100\n- Compromiso y responsabilidad",
            "duracion_semanas": data["duracion"],
            "horas_semana": 20,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_inicio + timedelta(weeks=data["duracion"]),
            "cupos_disponibles": data["cupos"],
            "cupos_totales": data["cupos"],
            "estado": "disponible",
            "fecha_limite_inscripcion": fecha_limite,
            "activa": True,
            "beneficios": "Certificado de prácticas, experiencia profesional, networking universitario"
        }
    )
    practicas_internas.append(practica)
    if created:
        print(f"  ✓ Creada: {practica.titulo} - {practica.facultad.nombre}")
    else:
        print(f"  → Existente: {practica.titulo}")

# 7. CREAR INSCRIPCIONES
print("\n[7/9] Creando Inscripciones...")
estados_posibles = ['pendiente', 'aprobada', 'rechazada']
inscripciones_count = 0

for i, estudiante in enumerate(estudiantes[:8]):  # 8 estudiantes con inscripciones
    # Cada estudiante se inscribe en 1-2 prácticas
    num_inscripciones = random.randint(1, 2)
    practicas_disponibles = random.sample(practicas, min(num_inscripciones, len(practicas)))
    
    for practica in practicas_disponibles:
        inscripcion, created = Inscripcion.objects.get_or_create(
            estudiante=estudiante,
            practica=practica,
            defaults={
                "estado": random.choice(estados_posibles),
                "observaciones": "Inscripción de prueba generada automáticamente."
            }
        )
        if created:
            inscripciones_count += 1
            # Reducir cupos si está pendiente o aprobada
            if inscripcion.estado in ['pendiente', 'aprobada'] and practica.cupos_disponibles > 0:
                practica.cupos_disponibles -= 1
                practica.save()

print(f"  ✓ Creadas {inscripciones_count} inscripciones")

# 8. CREAR INSCRIPCIONES INTERNAS
print("\n[8/9] Creando Inscripciones Internas...")
inscripciones_internas_count = 0

for estudiante in estudiantes[5:10]:  # 5 estudiantes con inscripciones internas
    if random.choice([True, False]):  # 50% de probabilidad
        practica_interna = random.choice(practicas_internas)
        inscripcion, created = InscripcionInterna.objects.get_or_create(
            estudiante=estudiante,
            practica_interna=practica_interna,
            defaults={
                "estado": random.choice(estados_posibles),
                "observaciones": "Inscripción interna de prueba."
            }
        )
        if created:
            inscripciones_internas_count += 1
            if inscripcion.estado in ['pendiente', 'aprobada'] and practica_interna.cupos_disponibles > 0:
                practica_interna.cupos_disponibles -= 1
                practica_interna.save()

print(f"  ✓ Creadas {inscripciones_internas_count} inscripciones internas")

# 9. CREAR DOCUMENTOS
print("\n[9/9] Creando Documentos de Inscripción...")
documentos_count = 0
tipos_documentos = ['cv', 'carta_presentacion', 'certificado_notas', 'carta_recomendacion']

inscripciones_con_docs = Inscripcion.objects.filter(estado__in=['pendiente', 'aprobada'])[:5]
for inscripcion in inscripciones_con_docs:
    # Crear 2-3 documentos por inscripción
    num_docs = random.randint(2, 3)
    tipos_elegidos = random.sample(tipos_documentos, num_docs)
    
    for tipo in tipos_elegidos:
        nombre_doc = f"{tipo.replace('_', ' ').title()} - {inscripcion.estudiante.user.get_full_name()}"
        doc, created = DocumentoInscripcion.objects.get_or_create(
            inscripcion=inscripcion,
            tipo=tipo,
            defaults={
                "nombre": nombre_doc,
                "archivo": f"documentos_inscripcion/dummy_{tipo}.pdf"  # Archivo dummy
            }
        )
        if created:
            documentos_count += 1

print(f"  ✓ Creados {documentos_count} documentos")

print("\n" + "=" * 60)
print("✅ POBLACIÓN DE DATOS COMPLETADA")
print("=" * 60)
print(f"\nResumen:")
print(f"  • Carreras: {Carrera.objects.count()}")
print(f"  • Empresas: {Empresa.objects.count()}")
print(f"  • Facultades: {Facultad.objects.count()}")
print(f"  • Estudiantes: {Estudiante.objects.count()}")
print(f"  • Prácticas: {Practica.objects.count()}")
print(f"  • Prácticas Internas: {PracticaInterna.objects.count()}")
print(f"  • Inscripciones: {Inscripcion.objects.count()}")
print(f"  • Inscripciones Internas: {InscripcionInterna.objects.count()}")
print(f"  • Documentos: {DocumentoInscripcion.objects.count()}")
print("\n✓ Puedes acceder al panel de administración en: http://127.0.0.1:8000/admin/")
print("✓ Usuario: admin | Contraseña: admin123")
print("\n✓ Estudiantes de prueba:")
print("  Usuario: estudiante1-10 | Contraseña: estudiante123")
print("=" * 60)
