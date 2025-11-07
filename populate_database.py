"""
Script para llenar la base de datos con datos de prueba
Ejecutar: python populate_database.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.contrib.auth.models import User
from inscripciones.models import (
    Carrera, Estudiante, Empresa, Practica, Inscripcion,
    Facultad, PracticaInterna, InscripcionInterna, Calificacion
)

def clear_data():
    """Limpiar datos existentes (opcional)"""
    print("🗑️  Limpiando datos existentes...")
    Calificacion.objects.all().delete()
    InscripcionInterna.objects.all().delete()
    Inscripcion.objects.all().delete()
    PracticaInterna.objects.all().delete()
    Practica.objects.all().delete()
    Estudiante.objects.all().delete()
    Empresa.objects.all().delete()
    Facultad.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("   ✅ Datos eliminados")

def create_empresas():
    """Crear empresas de ejemplo"""
    print("\n🏢 Creando empresas...")
    
    empresas_data = [
        {
            'nombre': 'TechSolutions Ecuador',
            'ruc': '09923456780',
            'sector': 'Tecnología',
            'direccion': 'Av. Francisco de Orellana, Edificio Blue Towers, Piso 8, Manta',
            'telefono': '052-123456',
            'email': 'rrhh@techsolutions.ec',
            'contacto_responsable': 'Ing. Roberto Salazar',
            'descripcion': 'Empresa líder en desarrollo de software y soluciones tecnológicas para empresas.',
            'activa': True
        },
        {
            'nombre': 'Hospital del Puerto',
            'ruc': '09912345670',
            'sector': 'Salud',
            'direccion': 'Av. 4 de Noviembre y Calle 15, Manta',
            'telefono': '052-234567',
            'email': 'recursos.humanos@hospitaldelpuerto.ec',
            'contacto_responsable': 'Dra. María López',
            'descripcion': 'Centro médico con más de 20 años de experiencia brindando atención de calidad.',
            'activa': True
        },
        {
            'nombre': 'Banco del Pacífico',
            'ruc': '09901234560',
            'sector': 'Finanzas',
            'direccion': 'Av. 2 y Calle 13, Centro Financiero, Manta',
            'telefono': '052-345678',
            'email': 'talentohumano@bancopacifico.ec',
            'contacto_responsable': 'Lcdo. Carlos Mendoza',
            'descripcion': 'Institución financiera con amplia trayectoria en el mercado ecuatoriano.',
            'activa': True
        },
        {
            'nombre': 'Constructora ManabíBuilders',
            'ruc': '09934567890',
            'sector': 'Construcción',
            'direccion': 'Vía Barbasquillo Km 3.5, Manta',
            'telefono': '052-456789',
            'email': 'rrhh@manabibuilders.com',
            'contacto_responsable': 'Arq. Fernando Castro',
            'descripcion': 'Empresa constructora especializada en proyectos residenciales y comerciales.',
            'activa': True
        },
        {
            'nombre': 'Colegio Particular El Saber',
            'ruc': '09945678900',
            'sector': 'Educación',
            'direccion': 'Av. Universidad y Calle 103, Manta',
            'telefono': '052-567890',
            'email': 'administracion@elsaber.edu.ec',
            'contacto_responsable': 'Lic. Ana Ramírez',
            'descripcion': 'Institución educativa de nivel inicial, básica y bachillerato.',
            'activa': True
        },
        {
            'nombre': 'Atún del Ecuador S.A.',
            'ruc': '09956789010',
            'sector': 'Industria Alimentaria',
            'direccion': 'Puerto Pesquero, Zona Industrial, Manta',
            'telefono': '052-678901',
            'email': 'contrataciones@atunecuador.com',
            'contacto_responsable': 'Ing. Luis Vélez',
            'descripcion': 'Empresa pesquera y procesadora de atún con certificaciones internacionales.',
            'activa': True
        },
        {
            'nombre': 'Hotel Oro Verde',
            'ruc': '09967890120',
            'sector': 'Turismo y Hotelería',
            'direccion': 'Malecón Escénico y Calle 23, Manta',
            'telefono': '052-789012',
            'email': 'rrhh@hoteloroverde.com.ec',
            'contacto_responsable': 'Lic. Patricia Morán',
            'descripcion': 'Hotel 5 estrellas con servicios de primera clase y vistas al océano.',
            'activa': True
        },
        {
            'nombre': 'Marketing Digital Pro',
            'ruc': '09978901230',
            'sector': 'Marketing y Publicidad',
            'direccion': 'Av. Flavio Reyes 123, Edificio Empresarial, Manta',
            'telefono': '052-890123',
            'email': 'contacto@marketingpro.ec',
            'contacto_responsable': 'Ing. Diego Flores',
            'descripcion': 'Agencia de marketing digital especializada en redes sociales y SEO.',
            'activa': True
        }
    ]
    
    empresas_creadas = []
    for empresa_data in empresas_data:
        # Crear usuario para la empresa
        username = empresa_data['nombre'].lower().replace(' ', '_')[:30]
        user = User.objects.create_user(
            username=username,
            email=empresa_data['email'],
            password='empresa123',
            first_name=empresa_data['nombre'][:30],
            last_name='Empresa'
        )
        
        empresa = Empresa.objects.create(
            user=user,
            **empresa_data
        )
        empresas_creadas.append(empresa)
        print(f"   ✅ {empresa.nombre}")
    
    return empresas_creadas

def create_estudiantes():
    """Crear estudiantes de ejemplo"""
    print("\n👨‍🎓 Creando estudiantes...")
    
    # Obtener carreras existentes
    carreras = list(Carrera.objects.all())
    if not carreras:
        print("   ⚠️  No hay carreras. Ejecuta: python manage.py loaddata inscripciones/fixtures/carreras.json")
        return []
    
    estudiantes_data = [
        {'nombres': 'Juan Carlos', 'apellidos': 'Pérez Mora', 'cedula': '1312345678', 'email': 'juan.perez@uleam.edu.ec', 'telefono': '0987654321', 'genero': 'M', 'fecha_nacimiento': '2001-05-15'},
        {'nombres': 'María José', 'apellidos': 'García Luna', 'cedula': '1323456789', 'email': 'maria.garcia@uleam.edu.ec', 'telefono': '0987654322', 'genero': 'F', 'fecha_nacimiento': '2002-03-20'},
        {'nombres': 'Carlos Alberto', 'apellidos': 'Rodríguez Vélez', 'cedula': '1334567890', 'email': 'carlos.rodriguez@uleam.edu.ec', 'telefono': '0987654323', 'genero': 'M', 'fecha_nacimiento': '2001-08-10'},
        {'nombres': 'Ana Lucía', 'apellidos': 'Martínez Castro', 'cedula': '1345678901', 'email': 'ana.martinez@uleam.edu.ec', 'telefono': '0987654324', 'genero': 'F', 'fecha_nacimiento': '2002-11-25'},
        {'nombres': 'Luis Fernando', 'apellidos': 'López Bravo', 'cedula': '1356789012', 'email': 'luis.lopez@uleam.edu.ec', 'telefono': '0987654325', 'genero': 'M', 'fecha_nacimiento': '2001-01-30'},
        {'nombres': 'Sofía Alexandra', 'apellidos': 'Sánchez Mora', 'cedula': '1367890123', 'email': 'sofia.sanchez@uleam.edu.ec', 'telefono': '0987654326', 'genero': 'F', 'fecha_nacimiento': '2002-06-18'},
        {'nombres': 'Diego Andrés', 'apellidos': 'Ramírez Loor', 'cedula': '1378901234', 'email': 'diego.ramirez@uleam.edu.ec', 'telefono': '0987654327', 'genero': 'M', 'fecha_nacimiento': '2001-09-05'},
        {'nombres': 'Valentina Isabel', 'apellidos': 'Torres Cedeño', 'cedula': '1389012345', 'email': 'valentina.torres@uleam.edu.ec', 'telefono': '0987654328', 'genero': 'F', 'fecha_nacimiento': '2002-12-12'},
        {'nombres': 'Andrés Sebastián', 'apellidos': 'Flores Pinargote', 'cedula': '1390123456', 'email': 'andres.flores@uleam.edu.ec', 'telefono': '0987654329', 'genero': 'M', 'fecha_nacimiento': '2001-04-22'},
        {'nombres': 'Camila Fernanda', 'apellidos': 'Mendoza Párraga', 'cedula': '1301234567', 'email': 'camila.mendoza@uleam.edu.ec', 'telefono': '0987654330', 'genero': 'F', 'fecha_nacimiento': '2002-07-08'},
        {'nombres': 'Gabriel Eduardo', 'apellidos': 'Vera Alcívar', 'cedula': '1312346789', 'email': 'gabriel.vera@uleam.edu.ec', 'telefono': '0987654331', 'genero': 'M', 'fecha_nacimiento': '2001-10-15'},
        {'nombres': 'Isabella Nicole', 'apellidos': 'Cruz Moreira', 'cedula': '1323457890', 'email': 'isabella.cruz@uleam.edu.ec', 'telefono': '0987654332', 'genero': 'F', 'fecha_nacimiento': '2002-02-28'},
    ]
    
    estudiantes_creados = []
    for i, est_data in enumerate(estudiantes_data):
        # Crear usuario para el estudiante
        username = f"est{est_data['cedula']}"
        user = User.objects.create_user(
            username=username,
            email=est_data['email'],
            password='estudiante123',
            first_name=est_data['nombres'],
            last_name=est_data['apellidos']
        )
        
        estudiante = Estudiante.objects.create(
            user=user,
            codigo_estudiante=est_data['cedula'],
            carrera=random.choice(carreras),
            ciclo_actual=random.choice([6, 7, 8, 9, 10]),
            telefono=est_data['telefono'],
            direccion=f'Av. Universidad {100 + i}, Manta',
            fecha_nacimiento=est_data['fecha_nacimiento']
        )
        estudiantes_creados.append(estudiante)
        print(f"   ✅ {user.get_full_name()}")
    
    return estudiantes_creados

def create_practicas(empresas):
    """Crear prácticas externas"""
    print("\n💼 Creando prácticas externas...")
    
    practicas_data = [
        {
            'empresa': empresas[0],  # TechSolutions
            'titulo': 'Desarrollador Web Junior',
            'descripcion': 'Desarrollo de aplicaciones web con Django y React. Trabajo en equipo ágil.',
            'requisitos': 'Conocimientos en Python, Django, JavaScript. Inglés básico.',
            'duracion_horas': 320,
            'cupos_disponibles': 3,
            'area': 'Desarrollo de Software'
        },
        {
            'empresa': empresas[0],  # TechSolutions
            'titulo': 'Analista de Datos',
            'descripcion': 'Análisis de datos con Python, SQL y herramientas de BI.',
            'requisitos': 'Python, pandas, SQL, Excel avanzado.',
            'duracion_horas': 280,
            'cupos_disponibles': 2,
            'area': 'Data Science'
        },
        {
            'empresa': empresas[1],  # Hospital
            'titulo': 'Asistente de Administración en Salud',
            'descripcion': 'Apoyo en procesos administrativos del área de salud.',
            'requisitos': 'Estudiante de Administración o carreras afines. Manejo de Office.',
            'duracion_horas': 300,
            'cupos_disponibles': 2,
            'area': 'Administración'
        },
        {
            'empresa': empresas[2],  # Banco
            'titulo': 'Asistente de Atención al Cliente',
            'descripcion': 'Atención y asesoría a clientes del banco.',
            'requisitos': 'Excelente comunicación, manejo de Office, proactivo.',
            'duracion_horas': 320,
            'cupos_disponibles': 4,
            'area': 'Servicio al Cliente'
        },
        {
            'empresa': empresas[3],  # Constructora
            'titulo': 'Asistente de Obra Civil',
            'descripcion': 'Apoyo en supervisión y control de proyectos de construcción.',
            'requisitos': 'Estudiante de Ingeniería Civil. Manejo de AutoCAD.',
            'duracion_horas': 360,
            'cupos_disponibles': 2,
            'area': 'Construcción'
        },
        {
            'empresa': empresas[4],  # Colegio
            'titulo': 'Docente Auxiliar de Matemáticas',
            'descripcion': 'Apoyo en clases de matemáticas para nivel secundario.',
            'requisitos': 'Estudiante de Educación o carreras afines. Vocación docente.',
            'duracion_horas': 240,
            'cupos_disponibles': 2,
            'area': 'Educación'
        },
        {
            'empresa': empresas[5],  # Atunera
            'titulo': 'Asistente de Control de Calidad',
            'descripcion': 'Control de calidad en procesos de producción.',
            'requisitos': 'Estudiante de Ingeniería en Alimentos o afines.',
            'duracion_horas': 320,
            'cupos_disponibles': 3,
            'area': 'Calidad'
        },
        {
            'empresa': empresas[6],  # Hotel
            'titulo': 'Recepcionista y Atención al Huésped',
            'descripcion': 'Atención en recepción y servicios hoteleros.',
            'requisitos': 'Inglés intermedio, buena presentación, atención al cliente.',
            'duracion_horas': 280,
            'cupos_disponibles': 3,
            'area': 'Hotelería'
        },
        {
            'empresa': empresas[7],  # Marketing
            'titulo': 'Community Manager Junior',
            'descripcion': 'Gestión de redes sociales y creación de contenido digital.',
            'requisitos': 'Manejo de redes sociales, Photoshop básico, creatividad.',
            'duracion_horas': 240,
            'cupos_disponibles': 2,
            'area': 'Marketing Digital'
        },
    ]
    
    practicas_creadas = []
    for i, practica_data in enumerate(practicas_data):
        fecha_inicio = datetime.now().date() + timedelta(days=random.randint(10, 30))
        fecha_fin = fecha_inicio + timedelta(days=90)
        
        # Fecha límite debe ser ANTES de la fecha de inicio
        dias_antes = random.randint(1, 7)
        fecha_limite = datetime.combine(
            fecha_inicio - timedelta(days=dias_antes),
            datetime.min.time().replace(hour=23, minute=59, second=59)
        )
        
        # Hacer timezone-aware si USE_TZ está activado
        from django.utils.timezone import make_aware, is_naive
        if is_naive(fecha_limite):
            fecha_limite = make_aware(fecha_limite)
        
        # Calcular duracion_semanas y horas_semana desde duracion_horas
        duracion_horas = practica_data.pop('duracion_horas')
        duracion_semanas = 12  # Aproximadamente 3 meses
        horas_semana = duracion_horas // duracion_semanas
        
        # Quitar campos que no existen en el modelo
        practica_data.pop('area', None)
        
        practica = Practica.objects.create(
            **practica_data,
            duracion_semanas=duracion_semanas,
            horas_semana=horas_semana,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            fecha_limite_inscripcion=fecha_limite,
            cupos_totales=practica_data['cupos_disponibles'],
            estado='disponible',
            activa=True
        )
        practicas_creadas.append(practica)
        print(f"   ✅ {practica.titulo} - {practica.empresa.nombre}")
    
    return practicas_creadas

def create_facultades():
    """Crear facultades"""
    print("\n🏛️  Creando facultades...")
    
    facultades_data = [
        {
            'nombre': 'Facultad de Ciencias Informáticas',
            'codigo': 'FCI',
            'decano': 'Dr. Marco Vinicio Celi Sánchez',
            'direccion': 'Campus Central, Edificio de Ciencias, 3er piso, Manta-Ecuador',
            'telefono': '052-111111',
            'email': 'informatica@uleam.edu.ec',
            'contacto_responsable': 'Ing. Patricia Moreira',
            'descripcion': 'Formación en ingeniería de software, sistemas y tecnologías.'
        },
        {
            'nombre': 'Facultad de Ciencias Administrativas',
            'codigo': 'FCA',
            'decano': 'Dra. María Fernanda Villacreses',
            'direccion': 'Campus Central, Edificio Administrativo, 2do piso, Manta-Ecuador',
            'telefono': '052-222222',
            'email': 'administrativas@uleam.edu.ec',
            'contacto_responsable': 'Lcdo. Jorge Álava',
            'descripcion': 'Formación en administración de empresas y gestión.'
        },
        {
            'nombre': 'Facultad de Ciencias de la Salud',
            'codigo': 'FCS',
            'decano': 'Dr. Luis Alberto Chávez Vera',
            'direccion': 'Campus Salud, Edificio Médico, 1er piso, Manta-Ecuador',
            'telefono': '052-333333',
            'email': 'salud@uleam.edu.ec',
            'contacto_responsable': 'Dra. Ana Cedeño',
            'descripcion': 'Formación en enfermería, medicina y áreas de salud.'
        },
    ]
    
    facultades_creadas = []
    for fac_data in facultades_data:
        # Crear usuario para la facultad
        username = fac_data['codigo'].lower()
        user = User.objects.create_user(
            username=username,
            email=fac_data['email'],
            password='facultad123',
            first_name=fac_data['nombre'][:30],
            last_name='ULEAM'
        )
        
        facultad = Facultad.objects.create(
            user=user,
            **fac_data,
            activa=True
        )
        facultades_creadas.append(facultad)
        print(f"   ✅ {facultad.nombre}")
    
    return facultades_creadas

def create_practicas_internas(facultades):
    """Crear prácticas internas"""
    print("\n🎓 Creando prácticas internas...")
    
    practicas_data = [
        {
            'facultad': facultades[0],
            'titulo': 'Asistente de Laboratorio de Computación',
            'descripcion': 'Apoyo en mantenimiento y administración de laboratorios de cómputo.',
            'tipo_servicio': 'tecnico',
            'requisitos': 'Estudiante regular de FCI con conocimientos básicos de hardware y redes'
        },
        {
            'facultad': facultades[1],
            'titulo': 'Auxiliar de Secretaría Académica',
            'descripcion': 'Apoyo administrativo en procesos académicos y atención a estudiantes.',
            'tipo_servicio': 'administrativo',
            'requisitos': 'Estudiante regular de FCA con buena comunicación y manejo de Office'
        },
        {
            'facultad': facultades[2],
            'titulo': 'Asistente de Investigación en Salud Pública',
            'descripcion': 'Apoyo en proyectos de investigación epidemiológica y salud comunitaria.',
            'tipo_servicio': 'investigacion',
            'requisitos': 'Estudiante regular de FCS cursando desde 5to ciclo, conocimientos de estadística'
        },
    ]
    
    practicas_creadas = []
    for practica_data in practicas_data:
        fecha_inicio = datetime.now().date() + timedelta(days=random.randint(15, 45))
        fecha_fin = fecha_inicio + timedelta(weeks=12)
        
        # Fecha límite debe ser ANTES de la fecha de inicio
        dias_antes = random.randint(1, 7)
        fecha_limite = datetime.combine(
            fecha_inicio - timedelta(days=dias_antes),
            datetime.min.time().replace(hour=23, minute=59, second=59)
        )
        
        # Hacer timezone-aware
        from django.utils.timezone import make_aware, is_naive
        if is_naive(fecha_limite):
            fecha_limite = make_aware(fecha_limite)
        
        practica = PracticaInterna.objects.create(
            **practica_data,
            duracion_semanas=12,
            horas_semana=20,
            cupos_disponibles=2,
            cupos_totales=2,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            fecha_limite_inscripcion=fecha_limite,
            estado='disponible'
        )
        practicas_creadas.append(practica)
        print(f"   ✅ {practica.titulo} - {practica.facultad.nombre}")
    
    return practicas_creadas

def create_inscripciones(estudiantes, practicas):
    """Crear inscripciones"""
    print("\n📝 Creando inscripciones...")
    
    # Crear algunas inscripciones aleatorias
    for i in range(min(8, len(estudiantes))):
        estudiante = estudiantes[i]
        practica = random.choice(practicas)
        
        estado = random.choice(['pendiente', 'aprobada', 'rechazada'])
        
        inscripcion = Inscripcion.objects.create(
            estudiante=estudiante,
            practica=practica,
            estado=estado,
            fecha_inscripcion=datetime.now().date() - timedelta(days=random.randint(1, 20))
        )
        nombre_completo = f"{estudiante.user.first_name} {estudiante.user.last_name}"
        print(f"   ✅ {nombre_completo} → {practica.titulo} ({estado})")
    
    print(f"   Total: {Inscripcion.objects.count()} inscripciones")

def main():
    """Función principal"""
    print("=" * 60)
    print("🎲 LLENANDO BASE DE DATOS CON DATOS DE PRUEBA")
    print("=" * 60)
    
    # Preguntar si desea limpiar datos existentes
    respuesta = input("\n¿Deseas limpiar los datos existentes? (si/no): ").strip().lower()
    if respuesta in ['si', 's', 'yes', 'y']:
        clear_data()
    
    # Crear datos
    empresas = create_empresas()
    estudiantes = create_estudiantes()
    practicas = create_practicas(empresas)
    facultades = create_facultades()
    practicas_internas = create_practicas_internas(facultades)
    create_inscripciones(estudiantes, practicas[:len(practicas)//2])
    
    # Resumen
    print("\n" + "=" * 60)
    print("✅ BASE DE DATOS POBLADA EXITOSAMENTE")
    print("=" * 60)
    print(f"\n📊 RESUMEN:")
    print(f"   🏢 Empresas: {Empresa.objects.count()}")
    print(f"   👨‍🎓 Estudiantes: {Estudiante.objects.count()}")
    print(f"   💼 Prácticas Externas: {Practica.objects.count()}")
    print(f"   🏛️  Facultades: {Facultad.objects.count()}")
    print(f"   🎓 Prácticas Internas: {PracticaInterna.objects.count()}")
    print(f"   📝 Inscripciones: {Inscripcion.objects.count()}")
    print(f"   👤 Usuarios: {User.objects.count()}")
    
    print(f"\n🔐 CREDENCIALES DE PRUEBA:")
    print(f"\n   EMPRESAS:")
    print(f"   Usuario: techsolutions_ecuador")
    print(f"   Contraseña: empresa123")
    
    print(f"\n   ESTUDIANTES:")
    print(f"   Usuario: est1312345678")
    print(f"   Contraseña: estudiante123")
    
    print(f"\n   FACULTADES:")
    print(f"   Usuario: fci")
    print(f"   Contraseña: facultad123")
    
    print("\n" + "=" * 60)
    print("🎉 ¡Listo para usar!")
    print("   Ejecuta: python manage.py runserver")
    print("=" * 60)

if __name__ == "__main__":
    main()
