#!/usr/bin/env python
"""
Test para verificar que el chatbot obtiene el contexto correctamente
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

# Importar la función get_system_context
from chatbot.views import get_system_context

print("=" * 70)
print("PROBANDO FUNCIÓN get_system_context() DEL CHATBOT")
print("=" * 70)

try:
    context = get_system_context()
    print("\n✅ CONTEXTO GENERADO:")
    print(context)
    print("\n" + "=" * 70)
    print(f"Longitud del contexto: {len(context)} caracteres")
    print("=" * 70)
    
    # Verificar que contiene datos reales
    if "No hay prácticas" in context:
        print("\n⚠️  ADVERTENCIA: El contexto indica que no hay prácticas!")
    else:
        print("\n✅ El contexto SÍ contiene información de prácticas")
        
except Exception as e:
    print(f"\n❌ ERROR al generar contexto: {str(e)}")
    import traceback
    traceback.print_exc()
