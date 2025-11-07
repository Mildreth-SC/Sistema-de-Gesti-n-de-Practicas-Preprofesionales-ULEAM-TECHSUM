#!/usr/bin/env python
"""
Script para poblar la base de datos con todas las carreras de la ULEAM
Universidad Laica Eloy Alfaro de Manabí
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from inscripciones.models import Carrera

# Carreras de la ULEAM organizadas por Facultad
CARRERAS_ULEAM = [
    # FACULTAD DE CIENCIAS ADMINISTRATIVAS
    {'nombre': 'Administración de Empresas', 'codigo': 'FADM001', 'descripcion': 'Facultad de Ciencias Administrativas'},
    {'nombre': 'Contabilidad y Auditoría', 'codigo': 'FCONT001', 'descripcion': 'Facultad de Ciencias Administrativas'},
    {'nombre': 'Marketing', 'codigo': 'FMKT001', 'descripcion': 'Facultad de Ciencias Administrativas'},
    {'nombre': 'Comercio Exterior', 'codigo': 'FCOMEX001', 'descripcion': 'Facultad de Ciencias Administrativas'},
    
    # FACULTAD DE CIENCIAS ECONÓMICAS
    {'nombre': 'Economía', 'codigo': 'FECON001', 'descripcion': 'Facultad de Ciencias Económicas'},
    {'nombre': 'Finanzas', 'codigo': 'FFIN001', 'descripcion': 'Facultad de Ciencias Económicas'},
    
    # FACULTAD DE CIENCIAS DE LA EDUCACIÓN
    {'nombre': 'Educación Inicial', 'codigo': 'FEDINI001', 'descripcion': 'Facultad de Ciencias de la Educación'},
    {'nombre': 'Educación Básica', 'codigo': 'FEDBAS001', 'descripcion': 'Facultad de Ciencias de la Educación'},
    {'nombre': 'Pedagogía de los Idiomas Nacionales y Extranjeros', 'codigo': 'FEDIDI001', 'descripcion': 'Facultad de Ciencias de la Educación'},
    {'nombre': 'Pedagogía de las Ciencias Experimentales', 'codigo': 'FEDCIE001', 'descripcion': 'Facultad de Ciencias de la Educación'},
    {'nombre': 'Pedagogía de la Actividad Física y Deporte', 'codigo': 'FEDAF001', 'descripcion': 'Facultad de Ciencias de la Educación'},
    
    # FACULTAD DE CIENCIAS INFORMÁTICAS
    {'nombre': 'Ingeniería en Sistemas', 'codigo': 'FINSIS001', 'descripcion': 'Facultad de Ciencias Informáticas'},
    {'nombre': 'Tecnologías de la Información', 'codigo': 'FINTIC001', 'descripcion': 'Facultad de Ciencias Informáticas'},
    {'nombre': 'Software', 'codigo': 'FINSOFT001', 'descripcion': 'Facultad de Ciencias Informáticas'},
    
    # FACULTAD DE INGENIERÍA
    {'nombre': 'Ingeniería Civil', 'codigo': 'FINGCIV001', 'descripcion': 'Facultad de Ingeniería'},
    {'nombre': 'Ingeniería Eléctrica', 'codigo': 'FINGELEC01', 'descripcion': 'Facultad de Ingeniería'},
    {'nombre': 'Ingeniería Industrial', 'codigo': 'FINGIND001', 'descripcion': 'Facultad de Ingeniería'},
    {'nombre': 'Ingeniería Mecánica', 'codigo': 'FINGMEC001', 'descripcion': 'Facultad de Ingeniería'},
    {'nombre': 'Arquitectura', 'codigo': 'FINGARQ001', 'descripcion': 'Facultad de Ingeniería'},
    
    # FACULTAD DE CIENCIAS MÉDICAS
    {'nombre': 'Medicina', 'codigo': 'FMEDMED001', 'descripcion': 'Facultad de Ciencias Médicas'},
    {'nombre': 'Enfermería', 'codigo': 'FMEDENF001', 'descripcion': 'Facultad de Ciencias Médicas'},
    {'nombre': 'Laboratorio Clínico', 'codigo': 'FMEDLAB001', 'descripcion': 'Facultad de Ciencias Médicas'},
    {'nombre': 'Terapia Física', 'codigo': 'FMEDTER001', 'descripcion': 'Facultad de Ciencias Médicas'},
    {'nombre': 'Nutrición y Dietética', 'codigo': 'FMEDNUT001', 'descripcion': 'Facultad de Ciencias Médicas'},
    
    # FACULTAD DE ODONTOLOGÍA
    {'nombre': 'Odontología', 'codigo': 'FODONT001', 'descripcion': 'Facultad de Odontología'},
    
    # FACULTAD DE PSICOLOGÍA
    {'nombre': 'Psicología', 'codigo': 'FPSIC001', 'descripcion': 'Facultad de Psicología'},
    {'nombre': 'Psicología Clínica', 'codigo': 'FPSICLI001', 'descripcion': 'Facultad de Psicología'},
    
    # FACULTAD DE TRABAJO SOCIAL
    {'nombre': 'Trabajo Social', 'codigo': 'FTRABS001', 'descripcion': 'Facultad de Trabajo Social'},
    
    # FACULTAD DE DERECHO
    {'nombre': 'Derecho', 'codigo': 'FDER001', 'descripcion': 'Facultad de Derecho'},
    
    # FACULTAD DE COMUNICACIÓN
    {'nombre': 'Comunicación', 'codigo': 'FCOM001', 'descripcion': 'Facultad de Comunicación'},
    {'nombre': 'Periodismo', 'codigo': 'FCOMPER001', 'descripcion': 'Facultad de Comunicación'},
    {'nombre': 'Publicidad', 'codigo': 'FCOMPUB001', 'descripcion': 'Facultad de Comunicación'},
    
    # FACULTAD DE HOTELERÍA Y TURISMO
    {'nombre': 'Hotelería', 'codigo': 'FHOT001', 'descripcion': 'Facultad de Hotelería y Turismo'},
    {'nombre': 'Turismo', 'codigo': 'FTUR001', 'descripcion': 'Facultad de Hotelería y Turismo'},
    {'nombre': 'Gastronomía', 'codigo': 'FGAST001', 'descripcion': 'Facultad de Hotelería y Turismo'},
    
    # FACULTAD DE CIENCIAS AGROPECUARIAS
    {'nombre': 'Agronomía', 'codigo': 'FAGRO001', 'descripcion': 'Facultad de Ciencias Agropecuarias'},
    {'nombre': 'Medicina Veterinaria', 'codigo': 'FVET001', 'descripcion': 'Facultad de Ciencias Agropecuarias'},
    {'nombre': 'Ingeniería Agrícola', 'codigo': 'FAGRI001', 'descripcion': 'Facultad de Ciencias Agropecuarias'},
    
    # FACULTAD DE CIENCIAS DEL MAR
    {'nombre': 'Ingeniería Pesquera', 'codigo': 'FPESC001', 'descripcion': 'Facultad de Ciencias del Mar'},
    {'nombre': 'Acuicultura', 'codigo': 'FACUI001', 'descripcion': 'Facultad de Ciencias del Mar'},
    
    # FACULTAD DE CIENCIAS AMBIENTALES
    {'nombre': 'Ingeniería Ambiental', 'codigo': 'FAMB001', 'descripcion': 'Facultad de Ciencias Ambientales'},
    {'nombre': 'Gestión Ambiental', 'codigo': 'FGAMB001', 'descripcion': 'Facultad de Ciencias Ambientales'},
]

def poblar_carreras():
    """Poblar la base de datos con las carreras de la ULEAM"""
    print("=" * 80)
    print("POBLANDO CARRERAS DE LA ULEAM")
    print("=" * 80)
    
    carreras_creadas = 0
    carreras_existentes = 0
    carreras_actualizadas = 0
    
    for carrera_data in CARRERAS_ULEAM:
        try:
            # Intentar obtener por código primero
            carrera, created = Carrera.objects.update_or_create(
                codigo=carrera_data['codigo'],
                defaults={
                    'nombre': carrera_data['nombre'],
                    'descripcion': carrera_data['descripcion'],
                    'activa': True
                }
            )
            
            if created:
                print(f"✅ Creada: {carrera.nombre} ({carrera.codigo})")
                carreras_creadas += 1
            else:
                print(f"🔄 Actualizada: {carrera.nombre} ({carrera.codigo})")
                carreras_actualizadas += 1
        except Exception as e:
            # Si hay error, intentar buscar por nombre y actualizar
            try:
                carrera = Carrera.objects.get(nombre=carrera_data['nombre'])
                carrera.codigo = carrera_data['codigo']
                carrera.descripcion = carrera_data['descripcion']
                carrera.activa = True
                carrera.save()
                print(f"🔄 Actualizada (por nombre): {carrera.nombre} ({carrera.codigo})")
                carreras_actualizadas += 1
            except Carrera.DoesNotExist:
                print(f"❌ Error con {carrera_data['nombre']}: {e}")
                carreras_existentes += 1
    
    print("\n" + "=" * 80)
    print(f"RESUMEN:")
    print(f"  • Carreras creadas: {carreras_creadas}")
    print(f"  • Carreras actualizadas: {carreras_actualizadas}")
    print(f"  • Total en la base de datos: {Carrera.objects.count()}")
    print("=" * 80)

if __name__ == '__main__':
    try:
        poblar_carreras()
        print("\n✅ Proceso completado exitosamente!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
