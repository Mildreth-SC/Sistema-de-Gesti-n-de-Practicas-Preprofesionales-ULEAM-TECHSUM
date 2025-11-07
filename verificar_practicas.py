#!/usr/bin/env python
"""
Script temporal para verificar prácticas en la base de datos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from inscripciones.models import PracticaInterna, Practica, Empresa, Facultad

print("=" * 70)
print("VERIFICACIÓN DE PRÁCTICAS EN LA BASE DE DATOS")
print("=" * 70)

# Prácticas Internas
print("\n🎓 PRÁCTICAS INTERNAS:")
print(f"   Total en DB: {PracticaInterna.objects.count()}")
print(f"   Con activa=True: {PracticaInterna.objects.filter(activa=True).count()}")
print(f"   Con activa=False: {PracticaInterna.objects.filter(activa=False).count()}")

print("\n   Primeras 5 prácticas internas:")
for p in PracticaInterna.objects.all()[:5]:
    print(f"   • ID: {p.id} | Título: {p.titulo} | Activa: {p.activa}")

# Prácticas Externas
print("\n🏢 PRÁCTICAS EXTERNAS:")
print(f"   Total en DB: {Practica.objects.count()}")
print(f"   Con activa=True: {Practica.objects.filter(activa=True).count()}")
print(f"   Con activa=False: {Practica.objects.filter(activa=False).count()}")

print("\n   Primeras 5 prácticas externas:")
for p in Practica.objects.all()[:5]:
    print(f"   • ID: {p.id} | Título: {p.titulo} | Activa: {p.activa}")

# Empresas
print("\n🏭 EMPRESAS:")
print(f"   Total en DB: {Empresa.objects.count()}")
print(f"   Con activa=True: {Empresa.objects.filter(activa=True).count()}")

# Facultades
print("\n🎓 FACULTADES:")
print(f"   Total en DB: {Facultad.objects.count()}")
print(f"   Con activa=True: {Facultad.objects.filter(activa=True).count()}")

print("\n" + "=" * 70)
print("VERIFICACIÓN COMPLETA")
print("=" * 70)
