"""
Script para verificar el estado de aprobación de empresas y facultades
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from inscripciones.models import Empresa, Facultad
from django.contrib.auth.models import User

print("\n" + "="*80)
print("VERIFICACIÓN DE ESTADO DE APROBACIÓN")
print("="*80)

print("\n📊 EMPRESAS REGISTRADAS:")
print("-" * 80)
empresas = Empresa.objects.all()
if empresas:
    for emp in empresas:
        print(f"\nNombre: {emp.nombre}")
        print(f"RUC: {emp.ruc}")
        print(f"Email: {emp.email}")
        print(f"Usuario asociado: {emp.user.username if emp.user else 'Sin usuario'}")
        print(f"Estado aprobación: {emp.estado_aprobacion}")
        print(f"Activa: {emp.activa}")
        print(f"Puede acceder: {emp.puede_acceder()}")
        if emp.observaciones_aprobacion:
            print(f"Observaciones: {emp.observaciones_aprobacion}")
else:
    print("No hay empresas registradas.")

print("\n" + "-" * 80)
print("\n📊 FACULTADES REGISTRADAS:")
print("-" * 80)
facultades = Facultad.objects.all()
if facultades:
    for fac in facultades:
        print(f"\nNombre: {fac.nombre}")
        print(f"Código: {fac.codigo}")
        print(f"Email: {fac.email}")
        print(f"Usuario asociado: {fac.user.username if fac.user else 'Sin usuario'}")
        print(f"Estado aprobación: {fac.estado_aprobacion}")
        print(f"Activa: {fac.activa}")
        print(f"Puede acceder: {fac.puede_acceder()}")
        if fac.observaciones_aprobacion:
            print(f"Observaciones: {fac.observaciones_aprobacion}")
else:
    print("No hay facultades registradas.")

print("\n" + "="*80)
print("RESUMEN:")
print("="*80)
print(f"Total empresas: {empresas.count()}")
print(f"Empresas pendientes: {empresas.filter(estado_aprobacion='pendiente').count()}")
print(f"Empresas aprobadas: {empresas.filter(estado_aprobacion='aprobada').count()}")
print(f"Empresas rechazadas: {empresas.filter(estado_aprobacion='rechazada').count()}")
print(f"\nTotal facultades: {facultades.count()}")
print(f"Facultades pendientes: {facultades.filter(estado_aprobacion='pendiente').count()}")
print(f"Facultades aprobadas: {facultades.filter(estado_aprobacion='aprobada').count()}")
print(f"Facultades rechazadas: {facultades.filter(estado_aprobacion='rechazada').count()}")
print("="*80 + "\n")
