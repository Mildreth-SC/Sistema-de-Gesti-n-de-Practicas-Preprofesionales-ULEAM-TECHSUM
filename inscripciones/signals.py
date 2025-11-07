# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Inscripcion, InscripcionInterna, Practica, PracticaInterna


@receiver(pre_save, sender=Inscripcion)
def inscripcion_cambio_estado(sender, instance, **kwargs):
    """
    Signal para manejar cambios de estado en inscripciones
    y ajustar cupos cuando se aprueba/rechaza desde el admin
    """
    if instance.pk:  # Si ya existe (no es nueva)
        try:
            old_instance = Inscripcion.objects.get(pk=instance.pk)
            
            # Si cambió de estado
            if old_instance.estado != instance.estado:
                # Registrar evaluación
                if instance.estado in ['aprobada', 'rechazada'] and not instance.fecha_evaluacion:
                    instance.fecha_evaluacion = timezone.now()
                
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
    """
    if instance.pk:
        try:
            old_instance = InscripcionInterna.objects.get(pk=instance.pk)
            
            if old_instance.estado != instance.estado:
                if instance.estado in ['aprobada', 'rechazada'] and not instance.fecha_evaluacion:
                    instance.fecha_evaluacion = timezone.now()
                
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
