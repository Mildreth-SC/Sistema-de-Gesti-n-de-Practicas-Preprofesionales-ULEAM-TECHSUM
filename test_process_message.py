#!/usr/bin/env python
"""
Test del process_message (fallback sin OpenAI)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from chatbot.views import process_message

print("=" * 70)
print("TEST DE process_message (FALLBACK SIN OPENAI)")
print("=" * 70)

# Probar diferentes mensajes
mensajes = [
    "Hola",
    "¿Qué prácticas hay disponibles?",
    "Muéstrame las prácticas",
    "Ver prácticas",
    "Hay prácticas disponibles?",
    "Prácticas internas",
    "Muéstrame empresas"
]

for msg in mensajes:
    print(f"\n{'=' * 70}")
    print(f"MENSAJE: {msg}")
    print('=' * 70)
    response = process_message(msg)
    print(response['response'][:500] + "..." if len(response['response']) > 500 else response['response'])
    print()
