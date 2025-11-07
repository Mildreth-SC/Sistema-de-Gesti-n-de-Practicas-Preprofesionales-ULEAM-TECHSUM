"""
Custom Storage Backend para Django usando Supabase Storage
Esto permite guardar archivos media (imágenes) en Supabase en lugar del servidor
"""
from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
from urllib.parse import urljoin
import os


class SupabaseStorage(Storage):
    """
    Storage backend para guardar archivos en Supabase Storage
    """
    
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_SERVICE_ROLE_KEY
        self.bucket_name = getattr(settings, 'SUPABASE_BUCKET_NAME', 'media')
        self.client = create_client(self.supabase_url, self.supabase_key)
        
    def _get_bucket(self):
        """Obtiene o crea el bucket de Supabase"""
        try:
            # Intentar crear el bucket (si ya existe, fallará silenciosamente)
            self.client.storage.create_bucket(
                self.bucket_name,
                options={'public': True}
            )
        except Exception:
            pass  # El bucket ya existe
        
        return self.client.storage.from_(self.bucket_name)
    
    def _save(self, name, content):
        """
        Guarda el archivo en Supabase Storage
        """
        bucket = self._get_bucket()
        
        # Leer el contenido del archivo
        content.seek(0)
        file_data = content.read()
        
        # Subir a Supabase
        try:
            bucket.upload(
                path=name,
                file=file_data,
                file_options={"content-type": content.content_type if hasattr(content, 'content_type') else 'application/octet-stream'}
            )
            return name
        except Exception as e:
            # Si ya existe, intentar actualizar
            try:
                bucket.update(
                    path=name,
                    file=file_data,
                    file_options={"content-type": content.content_type if hasattr(content, 'content_type') else 'application/octet-stream'}
                )
                return name
            except Exception as update_error:
                raise Exception(f"Error al guardar archivo: {str(e)}, {str(update_error)}")
    
    def _open(self, name, mode='rb'):
        """
        No se implementa porque generalmente solo necesitamos URLs públicas
        """
        raise NotImplementedError("SupabaseStorage no soporta lectura directa de archivos")
    
    def delete(self, name):
        """
        Elimina un archivo de Supabase Storage
        """
        bucket = self._get_bucket()
        try:
            bucket.remove([name])
        except Exception:
            pass  # Si no existe, ignorar
    
    def exists(self, name):
        """
        Verifica si un archivo existe en Supabase Storage
        """
        bucket = self._get_bucket()
        try:
            bucket.list(path=os.path.dirname(name))
            files = bucket.list(path=os.path.dirname(name))
            file_names = [f['name'] for f in files]
            return os.path.basename(name) in file_names
        except Exception:
            return False
    
    def url(self, name):
        """
        Retorna la URL pública del archivo
        """
        bucket = self._get_bucket()
        # Generar URL pública
        public_url = bucket.get_public_url(name)
        return public_url
    
    def size(self, name):
        """
        Retorna el tamaño del archivo
        """
        # No implementado - Supabase no proporciona esta info fácilmente
        return 0
    
    def get_available_name(self, name, max_length=None):
        """
        Retorna un nombre de archivo disponible
        """
        # Sobrescribir archivos con el mismo nombre
        if self.exists(name):
            self.delete(name)
        return name
