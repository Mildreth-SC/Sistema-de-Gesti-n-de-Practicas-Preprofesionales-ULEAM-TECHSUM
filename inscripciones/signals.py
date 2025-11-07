# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Inscripcion, InscripcionInterna, Practica, PracticaInterna, Notificacion


@receiver(pre_save, sender=Inscripcion)
def inscripcion_cambio_estado(sender, instance, **kwargs):
    """
    Signal para manejar cambios de estado en inscripciones
    y ajustar cupos cuando se aprueba/rechaza desde el admin
    
    IMPORTANTE: Cuando un estudiante es APROBADO:
    - Cancela automáticamente todas sus otras postulaciones pendientes
    - Evita que pueda postular a otras prácticas mientras tenga una aprobada
    """
    if instance.pk:  # Si ya existe (no es nueva)
        try:
            old_instance = Inscripcion.objects.get(pk=instance.pk)
            
            # Si cambió de estado
            if old_instance.estado != instance.estado:
                # Registrar evaluación
                if instance.estado in ['aprobada', 'rechazada'] and not instance.fecha_evaluacion:
                    instance.fecha_evaluacion = timezone.now()
                
                # ✅ NUEVO: Si se aprueba a un estudiante, cancelar sus otras postulaciones
                if old_instance.estado == 'pendiente' and instance.estado == 'aprobada':
                    # Crear notificación de aprobación
                    Notificacion.objects.create(
                        usuario=instance.estudiante.user,
                        tipo='aprobacion_practica',
                        titulo='¡Felicidades! Has sido seleccionado',
                        mensaje=f'Has sido aceptado en la práctica "{instance.practica.titulo}" en {instance.practica.empresa.nombre}. ¡Mucho éxito!',
                        inscripcion=instance
                    )
                    
                    # Cancelar todas las otras inscripciones pendientes del mismo estudiante (EXTERNAS)
                    otras_inscripciones = Inscripcion.objects.filter(
                        estudiante=instance.estudiante,
                        estado='pendiente'
                    ).exclude(pk=instance.pk)
                    
                    # Restaurar cupos para cada práctica cancelada
                    from django.db.models import F
                    for inscripcion in otras_inscripciones:
                        # Restaurar cupo de la práctica
                        Practica.objects.filter(pk=inscripcion.practica.pk).update(
                            cupos_disponibles=F('cupos_disponibles') + 1
                        )
                    
                    # Cancelar las inscripciones usando update (no dispara signal)
                    otras_inscripciones.update(
                        estado='cancelada',
                        fecha_evaluacion=timezone.now()
                    )
                    
                    # También cancelar inscripciones INTERNAS pendientes
                    from .models import InscripcionInterna, PracticaInterna
                    otras_internas = InscripcionInterna.objects.filter(
                        estudiante=instance.estudiante,
                        estado='pendiente'
                    )
                    
                    for insc_interna in otras_internas:
                        PracticaInterna.objects.filter(pk=insc_interna.practica_interna.pk).update(
                            cupos_disponibles=F('cupos_disponibles') + 1
                        )
                    
                    otras_internas.update(
                        estado='cancelada',
                        fecha_evaluacion=timezone.now()
                    )
                
                # Ajustar cupos si se rechaza o cancela una inscripción que estaba pendiente/aprobada
                if old_instance.estado in ['pendiente', 'aprobada'] and instance.estado in ['rechazada', 'cancelada']:
                    # Restaurar cupo
                    practica = instance.practica
                    practica.cupos_disponibles += 1
                    practica.save(update_fields=['cupos_disponibles'])
                
                # Reducir cupos si se aprueba una que estaba rechazada (caso raro pero posible)
                if old_instance.estado == 'rechazada' and instance.estado == 'aprobada':
                    practica = instance.practica
                    if practica.cupos_disponibles > 0:
                        practica.cupos_disponibles -= 1
                        practica.save(update_fields=['cupos_disponibles'])
        
        except Inscripcion.DoesNotExist:
            pass


@receiver(pre_save, sender=InscripcionInterna)
def inscripcion_interna_cambio_estado(sender, instance, **kwargs):
    """
    Signal para manejar cambios de estado en inscripciones internas
    
    IMPORTANTE: Cuando un estudiante es APROBADO:
    - Cancela automáticamente todas sus otras postulaciones pendientes
    - Evita que pueda postular a otras prácticas mientras tenga una aprobada
    """
    if instance.pk:
        try:
            old_instance = InscripcionInterna.objects.get(pk=instance.pk)
            
            if old_instance.estado != instance.estado:
                if instance.estado in ['aprobada', 'rechazada'] and not instance.fecha_evaluacion:
                    instance.fecha_evaluacion = timezone.now()
                
                # ✅ NUEVO: Si se aprueba a un estudiante, cancelar sus otras postulaciones
                if old_instance.estado == 'pendiente' and instance.estado == 'aprobada':
                    # Crear notificación de aprobación
                    Notificacion.objects.create(
                        usuario=instance.estudiante.user,
                        tipo='aprobacion_practica',
                        titulo='¡Felicidades! Has sido seleccionado',
                        mensaje=f'Has sido aceptado en la práctica interna "{instance.practica_interna.titulo}" en la facultad {instance.practica_interna.facultad.nombre}. ¡Mucho éxito!',
                        inscripcion_interna=instance
                    )
                    
                    # Cancelar todas las otras inscripciones pendientes del mismo estudiante (INTERNAS)
                    otras_inscripciones = InscripcionInterna.objects.filter(
                        estudiante=instance.estudiante,
                        estado='pendiente'
                    ).exclude(pk=instance.pk)
                    
                    # Restaurar cupos para cada práctica cancelada
                    from django.db.models import F
                    for inscripcion in otras_inscripciones:
                        # Restaurar cupo de la práctica interna
                        PracticaInterna.objects.filter(pk=inscripcion.practica_interna.pk).update(
                            cupos_disponibles=F('cupos_disponibles') + 1
                        )
                    
                    # Cancelar las inscripciones usando update (no dispara signal)
                    otras_inscripciones.update(
                        estado='cancelada',
                        fecha_evaluacion=timezone.now()
                    )
                    
                    # También cancelar inscripciones EXTERNAS pendientes
                    otras_externas = Inscripcion.objects.filter(
                        estudiante=instance.estudiante,
                        estado='pendiente'
                    )
                    
                    for insc_externa in otras_externas:
                        Practica.objects.filter(pk=insc_externa.practica.pk).update(
                            cupos_disponibles=F('cupos_disponibles') + 1
                        )
                    
                    otras_externas.update(
                        estado='cancelada',
                        fecha_evaluacion=timezone.now()
                    )
                
                if old_instance.estado in ['pendiente', 'aprobada'] and instance.estado in ['rechazada', 'cancelada']:
                    practica = instance.practica_interna
                    practica.cupos_disponibles += 1
                    practica.save(update_fields=['cupos_disponibles'])
                
                if old_instance.estado == 'rechazada' and instance.estado == 'aprobada':
                    practica = instance.practica_interna
                    if practica.cupos_disponibles > 0:
                        practica.cupos_disponibles -= 1
                        practica.save(update_fields=['cupos_disponibles'])
        
        except InscripcionInterna.DoesNotExist:
            pass


@receiver(pre_save, sender=Practica)
def practica_validar_cupos(sender, instance, **kwargs):
    """
    Validar que los cupos no sean negativos
    """
    if instance.cupos_disponibles < 0:
        instance.cupos_disponibles = 0


@receiver(pre_save, sender=PracticaInterna)
def practica_interna_validar_cupos(sender, instance, **kwargs):
    """
    Validar que los cupos no sean negativos
    """
    if instance.cupos_disponibles < 0:
        instance.cupos_disponibles = 0
