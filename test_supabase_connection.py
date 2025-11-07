"""
Script para verificar la conexión a Supabase
Ejecutar: python test_supabase_connection.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.db import connection
from django.conf import settings
from decouple import config

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("=" * 60)
    print("🔍 VERIFICANDO CONEXIÓN A SUPABASE")
    print("=" * 60)
    
    # Mostrar configuración (sin contraseña)
    print("\n📋 Configuración actual:")
    print(f"   Database: {settings.DATABASES['default']['NAME']}")
    print(f"   User: {settings.DATABASES['default']['USER']}")
    print(f"   Host: {settings.DATABASES['default']['HOST']}")
    print(f"   Port: {settings.DATABASES['default']['PORT']}")
    print(f"   SSL Mode: {settings.DATABASES['default']['OPTIONS'].get('sslmode', 'N/A')}")
    
    # Intentar conexión
    print("\n🔄 Intentando conectar...\n")
    
    try:
        with connection.cursor() as cursor:
            # Verificar versión de PostgreSQL
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print("✅ CONEXIÓN EXITOSA!")
            print(f"\n📊 PostgreSQL Version:")
            print(f"   {version[:80]}...")
            
            # Contar tablas
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            table_count = cursor.fetchone()[0]
            print(f"\n📁 Tablas en la base de datos: {table_count}")
            
            # Listar tablas de Django
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'inscripciones_%'
                ORDER BY table_name
            """)
            django_tables = cursor.fetchall()
            
            if django_tables:
                print("\n📋 Tablas de la aplicación 'inscripciones':")
                for table in django_tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"   ✓ {table[0]}: {count} registros")
            else:
                print("\n⚠️  No se encontraron tablas de Django.")
                print("   Ejecuta: python manage.py migrate")
            
            # Verificar Supabase API
            print(f"\n🔗 Supabase URL: {config('SUPABASE_URL', default='No configurado')}")
            print(f"🔑 Supabase Key: {'Configurado ✓' if config('SUPABASE_KEY', default='') else 'No configurado ✗'}")
            
            print("\n" + "=" * 60)
            print("✅ TODO ESTÁ FUNCIONANDO CORRECTAMENTE")
            print("=" * 60)
            return True
            
    except Exception as e:
        print("❌ ERROR DE CONEXIÓN!")
        print(f"\n⚠️  Detalles del error:")
        print(f"   {str(e)}")
        print("\n💡 Soluciones posibles:")
        print("   1. Verifica que el archivo .env esté configurado correctamente")
        print("   2. Comprueba que la contraseña de DB_PASSWORD sea correcta")
        print("   3. Asegúrate de que DB_HOST y DB_PORT sean correctos")
        print("   4. Verifica tu conexión a internet")
        print("   5. Comprueba que tu proyecto de Supabase esté activo")
        print("\n📖 Consulta GUIA_SUPABASE.md para más ayuda")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
