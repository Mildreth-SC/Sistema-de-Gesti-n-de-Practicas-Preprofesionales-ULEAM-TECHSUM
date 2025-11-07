"""
Script para corregir la fecha de la práctica para egresados
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from inscripciones.models import Practica
from django.utils import timezone

print("=" * 70)
print("🔧 CORRIGIENDO FECHA DE PRÁCTICA PARA EGRESADOS")
print("=" * 70)

# Buscar la práctica "Ayudante de factura"
practica = Practica.objects.filter(titulo="Ayudante de factura").first()

if practica:
    print(f"\n📋 Práctica encontrada: {practica.titulo}")
    print(f"   Empresa: {practica.empresa.nombre}")
    print(f"   Dirigido a: {practica.get_dirigido_a_display()}")
    print(f"   ❌ Fecha límite ACTUAL: {practica.fecha_limite_inscripcion}")
    
    # Actualizar fechas a valores válidos (futuro)
    practica.fecha_inicio = timezone.now().date() + timedelta(days=30)
    practica.fecha_fin = timezone.now().date() + timedelta(days=142)
    practica.fecha_limite_inscripcion = timezone.now() + timedelta(days=20)
    practica.activa = True
    practica.save()
    
    print(f"   ✅ Fecha límite NUEVA: {practica.fecha_limite_inscripcion}")
    print(f"   ✅ Fecha inicio: {practica.fecha_inicio}")
    print(f"   ✅ Fecha fin: {practica.fecha_fin}")
    print(f"   ✅ Activa: {'Sí' if practica.activa else 'No'}")
    
    print("\n✅ Práctica actualizada exitosamente!")
    print(f"\n💡 Ahora los egresados deberían poder ver esta práctica en:")
    print(f"   http://127.0.0.1:8000/practicas/")
    
else:
    print("\n❌ No se encontró la práctica 'Ayudante de factura'")

print("\n" + "=" * 70)
