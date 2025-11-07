#!/usr/bin/env python
"""
Test directo de las funciones de respuesta del chatbot
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from chatbot.views import get_practicas_disponibles, get_practicas_internas_disponibles, get_estadisticas_sistema

print("=" * 70)
print("TEST DE FUNCIONES DE RESPUESTA")
print("=" * 70)

print("\n1️⃣  get_estadisticas_sistema():")
print("-" * 70)
print(get_estadisticas_sistema())

print("\n\n2️⃣  get_practicas_disponibles():")
print("-" * 70)
print(get_practicas_disponibles())

print("\n\n3️⃣  get_practicas_internas_disponibles():")
print("-" * 70)
print(get_practicas_internas_disponibles())

print("\n" + "=" * 70)
