"""
Script de verificación pre-despliegue para Render
Ejecutar antes de hacer push al repositorio
"""
import os
import sys

def verificar_archivo(ruta, descripcion):
    """Verifica que un archivo exista"""
    if os.path.exists(ruta):
        print(f"✅ {descripcion}: OK")
        return True
    else:
        print(f"❌ {descripcion}: NO ENCONTRADO")
        return False

def verificar_contenido_archivo(ruta, contenido_esperado, descripcion):
    """Verifica que un archivo contenga cierto texto"""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if contenido_esperado in contenido:
                print(f"✅ {descripcion}: OK")
                return True
            else:
                print(f"⚠️  {descripcion}: FALTA CONFIGURACIÓN")
                return False
    except:
        print(f"❌ {descripcion}: ERROR AL LEER")
        return False

def main():
    print("\n" + "="*80)
    print("🔍 VERIFICACIÓN PRE-DESPLIEGUE PARA RENDER")
    print("="*80 + "\n")
    
    errores = 0
    advertencias = 0
    
    # 1. Archivos esenciales
    print("📁 ARCHIVOS ESENCIALES:")
    print("-" * 80)
    if not verificar_archivo('requirements.txt', 'requirements.txt'):
        errores += 1
    if not verificar_archivo('build.sh', 'build.sh'):
        errores += 1
    if not verificar_archivo('render.yaml', 'render.yaml'):
        errores += 1
    if not verificar_archivo('manage.py', 'manage.py'):
        errores += 1
    if not verificar_archivo('poblar_carreras_uleam.py', 'poblar_carreras_uleam.py'):
        advertencias += 1
    
    # 2. Configuración de Django
    print("\n⚙️  CONFIGURACIÓN DJANGO (settings.py):")
    print("-" * 80)
    if not verificar_contenido_archivo(
        'sistema_practicas/settings.py',
        "config('DEBUG'",
        "DEBUG configurable desde .env"
    ):
        advertencias += 1
    
    if not verificar_contenido_archivo(
        'sistema_practicas/settings.py',
        "ALLOWED_HOSTS",
        "ALLOWED_HOSTS configurado"
    ):
        errores += 1
    
    if not verificar_contenido_archivo(
        'sistema_practicas/settings.py',
        "whitenoise",
        "WhiteNoise para archivos estáticos"
    ):
        advertencias += 1
    
    # 3. Dependencias críticas
    print("\n📦 DEPENDENCIAS CRÍTICAS (requirements.txt):")
    print("-" * 80)
    dependencias = [
        ('Django', 'Django'),
        ('gunicorn', 'Gunicorn (servidor WSGI)'),
        ('psycopg2-binary', 'PostgreSQL driver'),
        ('whitenoise', 'WhiteNoise (archivos estáticos)'),
        ('supabase', 'Supabase SDK'),
        ('python-decouple', 'Python Decouple (variables de entorno)'),
    ]
    
    for dep, desc in dependencias:
        if not verificar_contenido_archivo('requirements.txt', dep, desc):
            errores += 1
    
    # 4. Build script
    print("\n🔨 BUILD SCRIPT (build.sh):")
    print("-" * 80)
    if not verificar_contenido_archivo(
        'build.sh',
        'collectstatic',
        'Comando collectstatic'
    ):
        errores += 1
    
    if not verificar_contenido_archivo(
        'build.sh',
        'migrate',
        'Comando migrate'
    ):
        errores += 1
    
    # 5. Render config
    print("\n🌐 RENDER CONFIG (render.yaml):")
    print("-" * 80)
    if not verificar_contenido_archivo(
        'render.yaml',
        'gunicorn',
        'Comando gunicorn en startCommand'
    ):
        errores += 1
    
    if not verificar_contenido_archivo(
        'render.yaml',
        'DATABASE_URL',
        'Variable DATABASE_URL'
    ):
        advertencias += 1
    
    # 6. Verificar migraciones
    print("\n🗄️  MIGRACIONES:")
    print("-" * 80)
    migraciones_path = 'inscripciones/migrations'
    if os.path.exists(migraciones_path):
        archivos = os.listdir(migraciones_path)
        migraciones = [f for f in archivos if f.endswith('.py') and f != '__init__.py']
        print(f"✅ Encontradas {len(migraciones)} migraciones")
        
        # Verificar migraciones importantes
        if any('dirigido_a' in f for f in migraciones):
            print(f"✅ Migración 'dirigido_a' encontrada")
        else:
            print(f"⚠️  Migración 'dirigido_a' no encontrada")
            advertencias += 1
    else:
        print(f"❌ Carpeta de migraciones no encontrada")
        errores += 1
    
    # 7. Verificar carreras
    print("\n🎓 CARRERAS ULEAM:")
    print("-" * 80)
    if verificar_contenido_archivo(
        'poblar_carreras_uleam.py',
        'CARRERAS_ULEAM',
        'Lista CARRERAS_ULEAM'
    ):
        try:
            with open('poblar_carreras_uleam.py', 'r', encoding='utf-8') as f:
                contenido = f.read()
                # Contar aproximadamente cuántas carreras hay
                num_carreras = contenido.count("'nombre':")
                if num_carreras >= 40:
                    print(f"✅ Aproximadamente {num_carreras} carreras definidas")
                else:
                    print(f"⚠️  Solo {num_carreras} carreras encontradas (esperadas 43)")
                    advertencias += 1
        except:
            print(f"⚠️  No se pudo contar carreras")
            advertencias += 1
    
    # 8. Gitignore
    print("\n🚫 GITIGNORE:")
    print("-" * 80)
    if os.path.exists('.gitignore'):
        if verificar_contenido_archivo('.gitignore', '.env', 'Excluye .env'):
            if verificar_contenido_archivo('.gitignore', 'db.sqlite3', 'Excluye db.sqlite3'):
                print("✅ .gitignore configurado correctamente")
        else:
            advertencias += 1
    else:
        print("⚠️  .gitignore no encontrado (crear uno)")
        advertencias += 1
    
    # RESUMEN
    print("\n" + "="*80)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*80)
    
    if errores == 0 and advertencias == 0:
        print("✅ ¡PERFECTO! El sistema está listo para desplegarse en Render")
        print("\n🚀 Próximos pasos:")
        print("   1. git add .")
        print("   2. git commit -m 'Preparado para producción'")
        print("   3. git push origin main")
        print("   4. Ir a Render.com y crear Web Service")
        return 0
    
    elif errores == 0:
        print(f"⚠️  Sistema casi listo con {advertencias} advertencia(s)")
        print("\n💡 Revisa las advertencias anteriores y corrígelas si es posible")
        print("   El despliegue debería funcionar, pero puede haber problemas menores")
        return 0
    
    else:
        print(f"❌ Encontrados {errores} error(es) crítico(s) y {advertencias} advertencia(s)")
        print("\n🔧 Corrige los errores antes de desplegar:")
        print("   - Revisa los archivos marcados con ❌")
        print("   - Asegúrate de que todos los archivos esenciales existan")
        print("   - Verifica la configuración en settings.py")
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        print("\n" + "="*80 + "\n")
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
