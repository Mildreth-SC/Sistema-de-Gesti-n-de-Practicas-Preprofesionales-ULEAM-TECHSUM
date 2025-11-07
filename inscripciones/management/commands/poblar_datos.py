# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inscripciones.models import (
    Carrera, Estudiante, Empresa, Practica, Inscripcion,
    Facultad, PracticaInterna, InscripcionInterna, DocumentoInscripcion
)
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de prueba'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("INICIANDO POBLACION DE DATOS DE PRUEBA"))
        self.stdout.write("=" * 60)

        # 1. CREAR CARRERAS
        self.stdout.write("\n[1/9] Creando Carreras...")
        carreras_data = [
            {"nombre": "Ingenieria en Sistemas", "codigo": "IS001", "descripcion": "Formacion de profesionales en desarrollo de software"},
            {"nombre": "Ingenieria Civil", "codigo": "IC002", "descripcion": "Formacion de profesionales en construccion"},
            {"nombre": "Medicina", "codigo": "MED003", "descripcion": "Formacion de medicos generales"},
            {"nombre": "Derecho", "codigo": "DER004", "descripcion": "Formacion de abogados"},
            {"nombre": "Administracion de Empresas", "codigo": "AE005", "descripcion": "Formacion de administradores"},
            {"nombre": "Psicologia", "codigo": "PSI006", "descripcion": "Formacion de psicologos"},
            {"nombre": "Contabilidad y Auditoria", "codigo": "CA007", "descripcion": "Formacion de contadores"},
            {"nombre": "Marketing", "codigo": "MKT008", "descripcion": "Formacion de especialistas en marketing"},
        ]

        carreras = []
        for data in carreras_data:
            carrera, created = Carrera.objects.get_or_create(
                codigo=data["codigo"],
                defaults={"nombre": data["nombre"], "descripcion": data["descripcion"], "activa": True}
            )
            carreras.append(carrera)
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Creada: {carrera.nombre}"))

        # 2. CREAR EMPRESAS
        self.stdout.write("\n[2/9] Creando Empresas...")
        empresas_data = [
            {"nombre": "Tech Solutions Ecuador", "ruc": "1790123456001", "sector": "Tecnologia", "telefono": "0987654321", "email": "contacto@techsolutions.ec", "contacto": "Juan Perez"},
            {"nombre": "Constructora del Pacifico S.A.", "ruc": "1790234567001", "sector": "Construccion", "telefono": "0987654322", "email": "info@construpac.com", "contacto": "Maria Gonzalez"},
            {"nombre": "Banco Nacional del Ecuador", "ruc": "1790345678001", "sector": "Financiero", "telefono": "0987654323", "email": "rrhh@banconacional.ec", "contacto": "Carlos Ramirez"},
            {"nombre": "Hospital Metropolitano", "ruc": "1790456789001", "sector": "Salud", "telefono": "0987654324", "email": "practicas@hosmetro.com", "contacto": "Ana Rodriguez"},
            {"nombre": "Estudio Juridico Asociados", "ruc": "1790567890001", "sector": "Legal", "telefono": "0987654325", "email": "contacto@estudiojuridico.ec", "contacto": "Luis Fernandez"},
            {"nombre": "Marketing Digital Pro", "ruc": "1790678901001", "sector": "Marketing", "telefono": "0987654326", "email": "info@marketingpro.ec", "contacto": "Patricia Morales"},
            {"nombre": "Grupo Empresarial Costa", "ruc": "1790789012001", "sector": "Comercio", "telefono": "0987654327", "email": "practicas@grupocosta.com", "contacto": "Roberto Silva"},
            {"nombre": "Consultoria y Auditoria CPA", "ruc": "1790890123001", "sector": "Consultoria", "telefono": "0987654328", "email": "rrhh@cpa-ec.com", "contacto": "Sandra Lopez"},
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
                    "descripcion": f"Empresa lider en el sector de {data['sector']}.",
                    "activa": True
                }
            )
            empresas.append(empresa)
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Creada: {empresa.nombre}"))

        # 3. CREAR FACULTADES
        self.stdout.write("\n[3/9] Creando Facultades...")
        facultades_data = [
            {"nombre": "Facultad de Ciencias Informaticas", "codigo": "FCI", "decano": "Dr. Miguel Torres"},
            {"nombre": "Facultad de Ingenieria", "codigo": "FING", "decano": "Dr. Roberto Mendoza"},
            {"nombre": "Facultad de Ciencias Medicas", "codigo": "FCM", "decano": "Dra. Elena Vargas"},
            {"nombre": "Facultad de Ciencias Sociales", "codigo": "FCSD", "decano": "Dr. Fernando Castro"},
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
                    "descripcion": "Facultad dedicada a la formacion academica de excelencia.",
                    "activa": True
                }
            )
            facultades.append(facultad)
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Creada: {facultad.nombre}"))

        # 4. CREAR ESTUDIANTES
        self.stdout.write("\n[4/9] Creando Estudiantes...")
        estudiantes_data = [
            {"username": "estudiante1", "nombres": "Diego", "apellidos": "Martinez", "codigo": "2021001", "ciclo": 8},
            {"username": "estudiante2", "nombres": "Laura", "apellidos": "Sanchez", "codigo": "2021002", "ciclo": 7},
            {"username": "estudiante3", "nombres": "Carlos", "apellidos": "Ramirez", "codigo": "2021003", "ciclo": 9},
            {"username": "estudiante4", "nombres": "Maria", "apellidos": "Flores", "codigo": "2021004", "ciclo": 8},
            {"username": "estudiante5", "nombres": "Andres", "apellidos": "Torres", "codigo": "2021005", "ciclo": 6},
            {"username": "estudiante6", "nombres": "Sofia", "apellidos": "Valencia", "codigo": "2021006", "ciclo": 7},
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
                self.stdout.write(self.style.SUCCESS(f"  Creado: {estudiante.user.get_full_name()}"))

        # 5. CREAR PRACTICAS
        self.stdout.write("\n[5/9] Creando Practicas...")
        practicas_data = [
            {"titulo": "Desarrollo Web Full Stack", "empresa_idx": 0, "duracion": 12, "horas": 40, "cupos": 3},
            {"titulo": "Asistente de Construccion", "empresa_idx": 1, "duracion": 16, "horas": 40, "cupos": 2},
            {"titulo": "Analista Financiero Junior", "empresa_idx": 2, "duracion": 12, "horas": 35, "cupos": 4},
            {"titulo": "Asistente Medico", "empresa_idx": 3, "duracion": 20, "horas": 30, "cupos": 2},
            {"titulo": "Asistente Legal", "empresa_idx": 4, "duracion": 12, "horas": 40, "cupos": 3},
            {"titulo": "Community Manager", "empresa_idx": 5, "duracion": 10, "horas": 30, "cupos": 2},
            {"titulo": "Asistente de Ventas", "empresa_idx": 6, "duracion": 12, "horas": 40, "cupos": 5},
            {"titulo": "Auditor Junior", "empresa_idx": 7, "duracion": 16, "horas": 40, "cupos": 2},
        ]

        practicas = []
        for data in practicas_data:
            fecha_inicio = timezone.now().date() + timedelta(days=random.randint(30, 60))
            fecha_limite = timezone.now() + timedelta(days=random.randint(5, 25))
            
            practica, created = Practica.objects.get_or_create(
                titulo=data["titulo"],
                empresa=empresas[data["empresa_idx"]],
                defaults={
                    "descripcion": f"Oportunidad de practica profesional en {data['titulo']}.",
                    "requisitos": "Estudiante regular\nPromedio minimo 80/100\nDisponibilidad tiempo completo",
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
                self.stdout.write(self.style.SUCCESS(f"  Creada: {practica.titulo}"))

        # 6. CREAR PRACTICAS INTERNAS
        self.stdout.write("\n[6/9] Creando Practicas Internas...")
        practicas_internas_data = [
            {"titulo": "Asistente de Investigacion en IA", "facultad_idx": 0, "tipo": "investigacion", "duracion": 12, "cupos": 2},
            {"titulo": "Tutor de Programacion", "facultad_idx": 0, "tipo": "docencia", "duracion": 16, "cupos": 3},
            {"titulo": "Asistente de Laboratorio", "facultad_idx": 1, "tipo": "tecnico", "duracion": 12, "cupos": 2},
            {"titulo": "Apoyo en Consulta Medica", "facultad_idx": 2, "tipo": "social", "duracion": 20, "cupos": 4},
            {"titulo": "Asistente Administrativo", "facultad_idx": 4, "tipo": "administrativo", "duracion": 12, "cupos": 3},
        ]

        practicas_internas = []
        for data in practicas_internas_data:
            fecha_inicio = timezone.now().date() + timedelta(days=random.randint(20, 50))
            fecha_limite = timezone.now() + timedelta(days=random.randint(5, 20))
            
            practica, created = PracticaInterna.objects.get_or_create(
                titulo=data["titulo"],
                facultad=facultades[data["facultad_idx"]],
                defaults={
                    "descripcion": f"Practica interna en {data['titulo']}.",
                    "tipo_servicio": data["tipo"],
                    "requisitos": "Estudiante regular\nPromedio minimo 75/100",
                    "duracion_semanas": data["duracion"],
                    "horas_semana": 20,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_inicio + timedelta(weeks=data["duracion"]),
                    "cupos_disponibles": data["cupos"],
                    "cupos_totales": data["cupos"],
                    "estado": "disponible",
                    "fecha_limite_inscripcion": fecha_limite,
                    "activa": True,
                    "beneficios": "Certificado de practicas, experiencia profesional"
                }
            )
            practicas_internas.append(practica)
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Creada: {practica.titulo}"))

        # 7. CREAR INSCRIPCIONES
        self.stdout.write("\n[7/9] Creando Inscripciones...")
        estados = ['pendiente', 'aprobada', 'rechazada']
        inscripciones_count = 0

        for estudiante in estudiantes[:8]:
            num_inscripciones = random.randint(1, 2)
            practicas_seleccionadas = random.sample(practicas, min(num_inscripciones, len(practicas)))
            
            for practica in practicas_seleccionadas:
                inscripcion, created = Inscripcion.objects.get_or_create(
                    estudiante=estudiante,
                    practica=practica,
                    defaults={
                        "estado": random.choice(estados),
                        "observaciones": "Inscripcion de prueba."
                    }
                )
                if created:
                    inscripciones_count += 1

        self.stdout.write(self.style.SUCCESS(f"  Creadas {inscripciones_count} inscripciones"))

        # 8. CREAR INSCRIPCIONES INTERNAS
        self.stdout.write("\n[8/9] Creando Inscripciones Internas...")
        inscripciones_internas_count = 0

        for estudiante in estudiantes[5:10]:
            if random.choice([True, False]):
                practica_interna = random.choice(practicas_internas)
                inscripcion, created = InscripcionInterna.objects.get_or_create(
                    estudiante=estudiante,
                    practica_interna=practica_interna,
                    defaults={
                        "estado": random.choice(estados),
                        "observaciones": "Inscripcion interna de prueba."
                    }
                )
                if created:
                    inscripciones_internas_count += 1

        self.stdout.write(self.style.SUCCESS(f"  Creadas {inscripciones_internas_count} inscripciones internas"))

        # 9. CREAR DOCUMENTOS
        self.stdout.write("\n[9/9] Creando Documentos de Inscripcion...")
        tipos_documentos = ['cv', 'carta_presentacion', 'certificado_notas']
        documentos_count = 0

        inscripciones_con_docs = Inscripcion.objects.filter(estado__in=['pendiente', 'aprobada'])[:5]
        for inscripcion in inscripciones_con_docs:
            for tipo in random.sample(tipos_documentos, 2):
                nombre_doc = f"{tipo} - {inscripcion.estudiante.codigo_estudiante}"
                doc, created = DocumentoInscripcion.objects.get_or_create(
                    inscripcion=inscripcion,
                    tipo=tipo,
                    defaults={
                        "nombre": nombre_doc,
                        "archivo": f"documentos_inscripcion/dummy_{tipo}.pdf"
                    }
                )
                if created:
                    documentos_count += 1

        self.stdout.write(self.style.SUCCESS(f"  Creados {documentos_count} documentos"))

        # RESUMEN FINAL
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("POBLACION COMPLETADA"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"\nResumen:")
        self.stdout.write(f"  Carreras: {Carrera.objects.count()}")
        self.stdout.write(f"  Empresas: {Empresa.objects.count()}")
        self.stdout.write(f"  Facultades: {Facultad.objects.count()}")
        self.stdout.write(f"  Estudiantes: {Estudiante.objects.count()}")
        self.stdout.write(f"  Practicas: {Practica.objects.count()}")
        self.stdout.write(f"  Practicas Internas: {PracticaInterna.objects.count()}")
        self.stdout.write(f"  Inscripciones: {Inscripcion.objects.count()}")
        self.stdout.write(f"  Inscripciones Internas: {InscripcionInterna.objects.count()}")
        self.stdout.write(f"  Documentos: {DocumentoInscripcion.objects.count()}")
        self.stdout.write("\nAcceso admin: http://127.0.0.1:8000/admin/")
        self.stdout.write("Usuario: admin | Password: admin123")
        self.stdout.write("Estudiantes: estudiante1-10 | Password: estudiante123")
        self.stdout.write("=" * 60)
