"""
Script para migrar datos de SQLite a Supabase/PostgreSQL
USAR SOLO SI YA TIENES DATOS EN db.sqlite3

Pasos:
1. Configura Supabase en .env
2. Ejecuta: python migrate_to_supabase.py
"""

import os
import sys
import django
import json

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')

def migrate_data():
    """Migra datos de SQLite a Supabase"""
    print("=" * 60)
    print("📦 MIGRACIÓN DE DATOS: SQLite → Supabase")
    print("=" * 60)
    
    # Verificar que existe db.sqlite3
    sqlite_db = 'db.sqlite3'
    if not os.path.exists(sqlite_db):
        print("\n⚠️  No se encontró db.sqlite3")
        print("   No hay datos para migrar.")
        return
    
    print(f"\n✅ Encontrado: {sqlite_db}")
    
    # Paso 1: Exportar datos de SQLite
    print("\n📤 PASO 1: Exportando datos de SQLite...")
    print("   Ejecutando: python manage.py dumpdata --natural-foreign --natural-primary > backup_sqlite.json")
    
    os.system('python manage.py dumpdata --natural-foreign --natural-primary --indent 2 > backup_sqlite.json')
    
    if os.path.exists('backup_sqlite.json'):
        size = os.path.getsize('backup_sqlite.json')
        print(f"   ✅ Exportado: backup_sqlite.json ({size} bytes)")
    else:
        print("   ❌ Error al exportar datos")
        return
    
    # Paso 2: Configurar Supabase
    print("\n⚙️  PASO 2: Configurando Supabase...")
    print("   Asegúrate de que el archivo .env esté configurado con:")
    print("   - DB_NAME")
    print("   - DB_USER")
    print("   - DB_PASSWORD")
    print("   - DB_HOST")
    print("   - DB_PORT")
    
    input("\n   Presiona ENTER cuando hayas configurado .env...")
    
    # Paso 3: Crear tablas en Supabase
    print("\n🔨 PASO 3: Creando tablas en Supabase...")
    print("   Ejecutando: python manage.py migrate")
    
    os.system('python manage.py migrate')
    
    # Paso 4: Importar datos
    print("\n📥 PASO 4: Importando datos a Supabase...")
    print("   Ejecutando: python manage.py loaddata backup_sqlite.json")
    
    result = os.system('python manage.py loaddata backup_sqlite.json')
    
    if result == 0:
        print("\n✅ MIGRACIÓN COMPLETADA CON ÉXITO")
        print("\n📊 Resumen:")
        print("   ✓ Datos exportados de SQLite")
        print("   ✓ Tablas creadas en Supabase")
        print("   ✓ Datos importados a Supabase")
        
        print("\n💾 Archivos creados:")
        print("   - backup_sqlite.json (respaldo de tus datos)")
        
        print("\n🔍 Próximos pasos:")
        print("   1. Verifica tus datos en Supabase Table Editor")
        print("   2. Ejecuta: python test_supabase_connection.py")
        print("   3. Ejecuta: python manage.py runserver")
        print("   4. Prueba tu aplicación")
        
        print("\n⚠️  IMPORTANTE:")
        print("   - Conserva backup_sqlite.json como respaldo")
        print("   - Conserva db.sqlite3 como respaldo")
        print("   - Puedes renombrar db.sqlite3 a db.sqlite3.backup")
        
    else:
        print("\n❌ ERROR EN LA MIGRACIÓN")
        print("   Revisa los mensajes de error anteriores")
        print("   Consulta GUIA_SUPABASE.md para ayuda")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("\n⚠️  ADVERTENCIA: Este script migrará todos tus datos a Supabase")
    print("   Asegúrate de haber configurado correctamente el archivo .env")
    
    response = input("\n¿Continuar? (si/no): ").strip().lower()
    
    if response in ['si', 's', 'yes', 'y']:
        migrate_data()
    else:
        print("\n❌ Migración cancelada")
        print("   Configura .env y vuelve a ejecutar este script")
