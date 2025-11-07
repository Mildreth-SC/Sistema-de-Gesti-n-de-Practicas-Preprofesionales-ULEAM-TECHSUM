#!/usr/bin/env python
"""
Test específico de los tres casos problemáticos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from chatbot.views import process_message

print("=" * 70)
print("TEST DE LOS 3 CASOS PROBLEMÁTICOS")
print("=" * 70)

# Casos problemáticos del usuario
mensajes = [
    ("Ver prácticas", "Debe mostrar EXTERNAS"),
    ("Prácticas internas", "Debe mostrar INTERNAS"),
    ("Ver empresas", "Debe mostrar EMPRESAS"),
    ("Muéstrame empresas", "Debe mostrar EMPRESAS"),
    ("Dame las internas", "Debe mostrar INTERNAS"),
    ("interna", "Debe mostrar INTERNAS"),
    ("facultad", "Debe mostrar INTERNAS"),
]

for msg, esperado in mensajes:
    print(f"\n{'=' * 70}")
    print(f"MENSAJE: {msg}")
    print(f"ESPERADO: {esperado}")
    print('=' * 70)
    response = process_message(msg)
    resp_text = response['response']
    
    # Verificar qué tipo de respuesta es
    if "🎯 **Prácticas Externas" in resp_text:
        print("✅ RESPUESTA: Prácticas EXTERNAS")
    elif "🎓 **Prácticas Internas" in resp_text:
        print("✅ RESPUESTA: Prácticas INTERNAS")
    elif "🏢 **Empresas" in resp_text:
        print("✅ RESPUESTA: Empresas")
    elif "no capté bien" in resp_text or "no entiendo" in resp_text:
        print("❌ RESPUESTA: No entendido")
    else:
        print("⚠️  RESPUESTA: Otro tipo")
    
    # Mostrar primeras líneas
    print("\nPrimeras líneas:")
    print(resp_text[:200] + "...")
