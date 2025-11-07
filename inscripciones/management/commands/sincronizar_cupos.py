# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from inscripciones.models import Practica, Inscripcion, PracticaInterna, InscripcionInterna


class Command(BaseCommand):
    help = 'Sincronizar cupos de prácticas con inscripciones activas'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("SINCRONIZANDO CUPOS"))
        self.stdout.write("=" * 60)

        # Sincronizar prácticas externas
        self.stdout.write("\n[1/2] Sincronizando prácticas externas...")
        for practica in Practica.objects.all():
            inscripciones_activas = Inscripcion.objects.filter(
                practica=practica,
                estado__in=['pendiente', 'aprobada']
            ).count()
            
            cupos_correctos = practica.cupos_totales - inscripciones_activas
            
            # Ajustar cupos totales si hay más inscripciones que cupos
            if cupos_correctos < 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠ {practica.titulo}: Más inscripciones ({inscripciones_activas}) "
                        f"que cupos totales ({practica.cupos_totales}). Ajustando cupos totales."
                    )
                )
                practica.cupos_totales = inscripciones_activas
                cupos_correctos = 0
            
            if practica.cupos_disponibles != cupos_correctos:
                self.stdout.write(
                    f"  Corrigiendo {practica.titulo}: "
                    f"{practica.cupos_disponibles} -> {cupos_correctos}"
                )
                practica.cupos_disponibles = cupos_correctos
                # Usar update sin triggear validaciones full_clean
                Practica.objects.filter(pk=practica.pk).update(
                    cupos_disponibles=cupos_correctos,
                    cupos_totales=practica.cupos_totales
                )

        # Sincronizar prácticas internas
        self.stdout.write("\n[2/2] Sincronizando prácticas internas...")
        for practica in PracticaInterna.objects.all():
            inscripciones_activas = InscripcionInterna.objects.filter(
                practica_interna=practica,
                estado__in=['pendiente', 'aprobada']
            ).count()
            
            cupos_correctos = practica.cupos_totales - inscripciones_activas
            
            # Ajustar cupos totales si hay más inscripciones que cupos
            if cupos_correctos < 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠ {practica.titulo}: Más inscripciones ({inscripciones_activas}) "
                        f"que cupos totales ({practica.cupos_totales}). Ajustando cupos totales."
                    )
                )
                practica.cupos_totales = inscripciones_activas
                cupos_correctos = 0
            
            if practica.cupos_disponibles != cupos_correctos:
                self.stdout.write(
                    f"  Corrigiendo {practica.titulo}: "
                    f"{practica.cupos_disponibles} -> {cupos_correctos}"
                )
                # Usar update sin triggear validaciones full_clean
                PracticaInterna.objects.filter(pk=practica.pk).update(
                    cupos_disponibles=cupos_correctos,
                    cupos_totales=practica.cupos_totales
                )

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✓ SINCRONIZACIÓN COMPLETADA"))
        self.stdout.write("=" * 60)
