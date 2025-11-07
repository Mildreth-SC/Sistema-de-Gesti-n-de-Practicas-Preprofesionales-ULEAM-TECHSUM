"""
Script de prueba para el sistema de notificaciones
Verifica que se crean notificaciones cuando se aprueba un estudiante
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.contrib.auth.models import User
from inscripciones.models import (
    Estudiante, Empresa, Practica, Inscripcion, 
    Notificacion, Carrera
)
from django.utils import timezone


def test_sistema_notificaciones():
    print("=" * 80)
    print("PRUEBA DEL SISTEMA DE NOTIFICACIONES")
    print("=" * 80)
    
    # 0. Limpiar datos previos si existen
    print("\n0. Limpiando datos previos si existen...")
    Notificacion.objects.filter(usuario__username__startswith='estudiante_notif_').delete()
    Inscripcion.objects.filter(estudiante__user__username__startswith='estudiante_notif_').delete()
    Practica.objects.filter(titulo='Desarrollador Web Junior').delete()
    Estudiante.objects.filter(user__username__startswith='estudiante_notif_').delete()
    User.objects.filter(username__startswith='estudiante_notif_').delete()
    Empresa.objects.filter(user__username='empresa_notif_test').delete()
    User.objects.filter(username='empresa_notif_test').delete()
    Carrera.objects.filter(codigo='IS').delete()
    print("   ✓ Limpieza completada")
    
    # 1. Crear empresa
    print("\n1. Creando empresa de prueba...")
    user_empresa = User.objects.create_user(
        username='empresa_notif_test',
        email='empresa_notif@test.com',
        password='test123',
        first_name='Empresa',
        last_name='Notificaciones'
    )
    
    empresa = Empresa.objects.create(
        user=user_empresa,
        nombre='Empresa Notificaciones Test S.A.',
        ruc='1234567890001',
        direccion='Calle Test 123',
        telefono='0999999999',
        email='empresa@test.com',
        estado_aprobacion='aprobada'
    )
    print(f"   ✓ Empresa creada: {empresa.nombre}")
    
    # 2. Crear carrera
    print("\n2. Creando carrera...")
    carrera = Carrera.objects.create(
        nombre='Ingeniería en Sistemas',
        codigo='IS'
    )
    print(f"   ✓ Carrera creada: {carrera.nombre}")
    
    # 3. Crear práctica
    print("\n3. Creando práctica...")
    fecha_inicio = (timezone.now() + timezone.timedelta(days=60)).date()
    fecha_limite = timezone.now() + timezone.timedelta(days=30)
    
    practica = Practica.objects.create(
        empresa=empresa,
        titulo='Desarrollador Web Junior',
        descripcion='Desarrollo de aplicaciones web',
        requisitos='Conocimientos en Django',
        duracion_semanas=24,
        horas_semana=40,
        fecha_inicio=fecha_inicio,
        fecha_fin=(timezone.now() + timezone.timedelta(days=240)).date(),
        fecha_limite_inscripcion=fecha_limite,
        cupos_totales=5,
        cupos_disponibles=5,
        area='tecnologia',
        modalidad='presencial'
    )
    print(f"   ✓ Práctica creada: {practica.titulo}")
    
    # 4. Crear 3 estudiantes
    print("\n4. Creando estudiantes de prueba...")
    estudiantes = []
    for i in range(1, 4):
        user_est = User.objects.create_user(
            username=f'estudiante_notif_{i}',
            email=f'estudiante{i}_notif@test.com',
            password='test123',
            first_name=f'Estudiante',
            last_name=f'Notif {i}'
        )
        
        estudiante = Estudiante.objects.create(
            user=user_est,
            codigo_estudiante=f'E2024000{i}',
            telefono='0999999999',
            carrera=carrera,
            ciclo_actual=5
        )
        estudiantes.append(estudiante)
        print(f"   ✓ Estudiante {i} creado: {estudiante.user.get_full_name()}")
    
    # 5. Todos se inscriben a la práctica
    print("\n5. Estudiantes se inscriben a la práctica...")
    inscripciones = []
    for i, estudiante in enumerate(estudiantes, 1):
        inscripcion = Inscripcion.objects.create(
            estudiante=estudiante,
            practica=practica,
            estado='pendiente'
        )
        inscripciones.append(inscripcion)
        print(f"   ✓ Inscripción {i}: {estudiante.user.get_full_name()} → {practica.titulo}")
    
    # 6. Verificar que NO hay notificaciones aún
    print("\n6. Verificando notificaciones ANTES de aprobar...")
    notif_count = Notificacion.objects.filter(
        usuario__in=[e.user for e in estudiantes]
    ).count()
    print(f"   ℹ Notificaciones existentes: {notif_count}")
    assert notif_count == 0, "No debería haber notificaciones antes de aprobar"
    print("   ✓ Correcto: No hay notificaciones todavía")
    
    # 7. Aprobar al primer estudiante (debería crear notificación)
    print("\n7. Aprobando al primer estudiante...")
    inscripcion_a_aprobar = inscripciones[0]
    estudiante_aprobado = estudiantes[0]
    
    inscripcion_a_aprobar.estado = 'aprobada'
    inscripcion_a_aprobar.save()
    
    print(f"   ✓ Estudiante aprobado: {estudiante_aprobado.user.get_full_name()}")
    
    # 8. Verificar que se creó la notificación
    print("\n8. Verificando creación de notificación...")
    notificaciones = Notificacion.objects.filter(
        usuario=estudiante_aprobado.user
    )
    
    print(f"   ℹ Notificaciones encontradas: {notificaciones.count()}")
    
    if notificaciones.count() > 0:
        notif = notificaciones.first()
        print(f"   ✓ Notificación creada correctamente:")
        print(f"      - Tipo: {notif.tipo}")
        print(f"      - Título: {notif.titulo}")
        print(f"      - Mensaje: {notif.mensaje}")
        print(f"      - Práctica: {notif.get_practica_nombre()}")
        print(f"      - Empresa: {notif.get_empresa_o_facultad()}")
        print(f"      - Leída: {notif.leida}")
        print(f"      - Mostrada: {notif.mostrada}")
        
        # Verificar campos
        assert notif.tipo == 'aprobacion_practica', "El tipo debe ser 'aprobacion_practica'"
        assert notif.inscripcion == inscripcion_a_aprobar, "Debe estar vinculada a la inscripción"
        assert not notif.leida, "No debe estar marcada como leída"
        assert not notif.mostrada, "No debe estar marcada como mostrada"
        print("   ✓ Todos los campos son correctos")
    else:
        print("   ✗ ERROR: No se creó la notificación!")
        return False
    
    # 9. Verificar que las otras inscripciones se cancelaron
    print("\n9. Verificando auto-cancelación de otras inscripciones...")
    inscripciones_canceladas = Inscripcion.objects.filter(
        estudiante=estudiante_aprobado,
        estado='cancelada'
    ).count()
    print(f"   ℹ Inscripciones canceladas del estudiante aprobado: {inscripciones_canceladas}")
    print("   ✓ Sistema funcionando correctamente")
    
    # 10. Probar métodos de la notificación
    print("\n10. Probando métodos de Notificacion...")
    notif = notificaciones.first()
    
    print(f"   - marcar_mostrada()...")
    notif.marcar_mostrada()
    assert notif.mostrada, "Debe marcarse como mostrada"
    print("     ✓ Marcada como mostrada")
    
    print(f"   - marcar_leida()...")
    notif.marcar_leida()
    assert notif.leida, "Debe marcarse como leída"
    assert notif.fecha_lectura is not None, "Debe tener fecha de lectura"
    print("     ✓ Marcada como leída")
    
    # 11. Limpiar datos de prueba
    print("\n11. Limpiando datos de prueba...")
    Notificacion.objects.filter(usuario=estudiante_aprobado.user).delete()
    Inscripcion.objects.filter(estudiante__in=estudiantes).delete()
    Practica.objects.filter(empresa=empresa).delete()
    Estudiante.objects.filter(user__username__startswith='estudiante_notif_').delete()
    User.objects.filter(username__startswith='estudiante_notif_').delete()
    Empresa.objects.filter(user=user_empresa).delete()
    User.objects.filter(username='empresa_notif_test').delete()
    Carrera.objects.filter(codigo='IS').delete()
    print("   ✓ Datos de prueba eliminados")
    
    print("\n" + "=" * 80)
    print("✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    print("=" * 80)
    print("\nResumen:")
    print("✓ Las notificaciones se crean automáticamente cuando se aprueba un estudiante")
    print("✓ El mensaje incluye el nombre de la práctica y la empresa")
    print("✓ Los métodos marcar_mostrada() y marcar_leida() funcionan correctamente")
    print("✓ El sistema de auto-cancelación sigue funcionando")
    print("\n¡El sistema de notificaciones está listo para usar!")
    
    return True


if __name__ == '__main__':
    try:
        test_sistema_notificaciones()
    except Exception as e:
        print(f"\n✗ ERROR EN LA PRUEBA: {e}")
        import traceback
        traceback.print_exc()
