"""
Script para configurar el bucket de Supabase Storage
Ejecutar este script UNA VEZ después de hacer deploy en Render
"""
from supabase import create_client
from decouple import config

# Configuración de Supabase
SUPABASE_URL = config('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = config('SUPABASE_SERVICE_ROLE_KEY')

def configurar_bucket():
    """
    Crea el bucket 'media' en Supabase Storage si no existe
    """
    print("🔧 Configurando Supabase Storage...")
    
    # Crear cliente de Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    
    try:
        # Intentar crear el bucket
        supabase.storage.create_bucket(
            'media',
            options={
                'public': True,  # Público para que las imágenes sean accesibles
                'fileSizeLimit': 52428800,  # 50 MB máximo por archivo
                'allowedMimeTypes': [
                    'image/png',
                    'image/jpeg',
                    'image/jpg',
                    'image/gif',
                    'image/webp',
                    'application/pdf'
                ]
            }
        )
        print("✅ Bucket 'media' creado exitosamente")
        print("✅ Configuración:")
        print("   - Público: Sí")
        print("   - Tamaño máximo: 50 MB")
        print("   - Tipos permitidos: Imágenes y PDF")
        
    except Exception as e:
        if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
            print("✅ Bucket 'media' ya existe")
        else:
            print(f"❌ Error al crear bucket: {e}")
            return False
    
    # Verificar que el bucket esté público
    try:
        buckets = supabase.storage.list_buckets()
        media_bucket = next((b for b in buckets if b['name'] == 'media'), None)
        
        if media_bucket:
            print(f"✅ Bucket encontrado: {media_bucket['name']}")
            print(f"   - ID: {media_bucket['id']}")
            print(f"   - Público: {media_bucket.get('public', False)}")
        else:
            print("⚠️ No se pudo verificar el bucket")
    except Exception as e:
        print(f"⚠️ Error al verificar bucket: {e}")
    
    print("\n🎉 Configuración completada!")
    print("\n📝 Próximos pasos:")
    print("1. En Render, agrega estas variables de entorno:")
    print(f"   SUPABASE_URL={SUPABASE_URL}")
    print(f"   SUPABASE_SERVICE_ROLE_KEY=[tu_service_role_key]")
    print("2. Haz un nuevo deploy o reinicia el servicio")
    print("3. Las nuevas imágenes se guardarán en Supabase Storage")
    
    return True

if __name__ == '__main__':
    configurar_bucket()
