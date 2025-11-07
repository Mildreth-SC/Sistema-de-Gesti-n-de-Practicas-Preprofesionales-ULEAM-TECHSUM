#!/usr/bin/env python
"""
Test completo del chatbot - simulando exactamente lo que hace la vista
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from chatbot.views import get_system_context, process_message_with_ai
from decouple import config

print("=" * 70)
print("TEST COMPLETO DEL CHATBOT")
print("=" * 70)

# 1. Verificar API Key
api_key = config('OPENAI_API_KEY', default='')
print(f"\n1. API Key configurada: {'✅ SÍ' if api_key else '❌ NO'}")
if api_key:
    print(f"   Primeros 20 caracteres: {api_key[:20]}...")

# 2. Probar get_system_context
print("\n2. Probando get_system_context()...")
try:
    context = get_system_context()
    print(f"   ✅ Contexto generado: {len(context)} caracteres")
    if "Ayudante" in context or "TechSolutions" in context:
        print("   ✅ Contiene datos reales de la BD")
    else:
        print("   ⚠️  NO contiene datos reales")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# 3. Probar process_message_with_ai con mensaje simple
print("\n3. Probando process_message_with_ai('Hola')...")
try:
    response = process_message_with_ai('Hola')
    print(f"   ✅ Respuesta recibida:")
    print(f"   Tipo: {type(response)}")
    print(f"   Keys: {response.keys() if isinstance(response, dict) else 'No es dict'}")
    print(f"\n   RESPUESTA DEL CHATBOT:")
    print("   " + "-" * 66)
    print(f"   {response.get('response', 'NO RESPONSE')[:500]}")
    print("   " + "-" * 66)
    
    # Verificar si menciona las estadísticas reales
    resp_text = response.get('response', '')
    if '10' in resp_text or '6' in resp_text:
        print("   ✅ La respuesta incluye números (posiblemente estadísticas)")
    else:
        print("   ⚠️  La respuesta NO incluye estadísticas numéricas")
        
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

# 4. Probar con pregunta sobre prácticas
print("\n4. Probando con '¿Qué prácticas hay disponibles?'...")
try:
    response = process_message_with_ai('¿Qué prácticas hay disponibles?')
    print(f"   ✅ Respuesta recibida: {len(response.get('response', ''))} caracteres")
    print(f"\n   RESPUESTA DEL CHATBOT:")
    print("   " + "-" * 66)
    print(f"   {response.get('response', 'NO RESPONSE')[:800]}")
    print("   " + "-" * 66)
    
    resp_text = response.get('response', '')
    if 'TechSolutions' in resp_text or 'Ayudante' in resp_text or 'Hotel' in resp_text:
        print("   ✅ La respuesta menciona prácticas reales de la BD")
    else:
        print("   ⚠️  La respuesta NO menciona prácticas específicas")
        
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("FIN DEL TEST")
print("=" * 70)
