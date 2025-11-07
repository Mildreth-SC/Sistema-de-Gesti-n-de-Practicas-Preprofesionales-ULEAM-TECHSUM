"""
Middleware para gestionar sesiones de Supabase Auth en Django
Sincroniza la autenticación de Supabase con Django
"""
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login, logout as django_logout
from django.utils.deprecation import MiddlewareMixin
from .supabase_client import supabase_auth
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class SupabaseAuthMiddleware(MiddlewareMixin):
    """
    Middleware para sincronizar sesiones de Supabase con Django
    
    - Lee el access_token de Supabase desde la sesión de Django
    - Verifica si el token es válido
    - Sincroniza el usuario de Supabase con Django User
    - Refresca tokens expirados automáticamente
    """
    
    def process_request(self, request):
        """Procesa cada request para verificar la sesión de Supabase"""
        
        # Excluir rutas de registro y login del middleware
        excluded_paths = [
            '/registro_estudiante/',
            '/registro_empresa/',
            '/registro_facultad/',
            '/login/',
            '/admin/',
        ]
        
        # Si la ruta está excluida, no procesar
        if any(request.path.startswith(path) for path in excluded_paths):
            return None
        
        # Obtener tokens de la sesión de Django
        access_token = request.session.get('supabase_access_token')
        refresh_token = request.session.get('supabase_refresh_token')
        
        # Si no hay token, el usuario no está autenticado con Supabase
        if not access_token:
            return None
        
        # Verificar si el usuario de Supabase existe
        try:
            supabase_user = supabase_auth.get_user(access_token)
            
            if supabase_user:
                # Usuario válido, sincronizar con Django
                self._sync_user_with_django(request, supabase_user)
            else:
                # Token inválido, intentar refrescar
                if refresh_token:
                    self._refresh_and_sync(request, refresh_token)
                else:
                    # No hay refresh token, cerrar sesión
                    self._cleanup_session(request)
                    
        except Exception as e:
            logger.error(f"Error en SupabaseAuthMiddleware: {e}")
            # En caso de error, intentar refrescar
            if refresh_token:
                self._refresh_and_sync(request, refresh_token)
            else:
                self._cleanup_session(request)
        
        return None
    
    def _sync_user_with_django(self, request, supabase_user):
        """
        Sincroniza el usuario de Supabase con Django User
        
        Args:
            request: HttpRequest
            supabase_user: Usuario de Supabase
        """
        email = supabase_user.email
        
        # Buscar o crear usuario de Django
        try:
            django_user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Crear usuario de Django si no existe
            django_user = User.objects.create_user(
                username=email,
                email=email,
                is_active=True
            )
            logger.info(f"Usuario Django creado para {email}")
        
        # Actualizar is_active basado en confirmación de email
        if supabase_user.email_confirmed_at:
            django_user.is_active = True
            django_user.save()
        
        # Si el usuario no está autenticado en Django, hacer login
        if not request.user.is_authenticated or request.user.email != email:
            django_login(request, django_user, backend='django.contrib.auth.backends.ModelBackend')
            logger.info(f"Usuario Django autenticado: {email}")
    
    def _refresh_and_sync(self, request, refresh_token):
        """
        Refresca el access token y sincroniza usuario
        
        Args:
            request: HttpRequest
            refresh_token: Refresh token de Supabase
        """
        result = supabase_auth.refresh_session(refresh_token)
        
        if result['success']:
            # Guardar nuevos tokens en la sesión
            request.session['supabase_access_token'] = result['access_token']
            request.session['supabase_refresh_token'] = result['session'].refresh_token
            request.session.modified = True
            
            # Obtener usuario y sincronizar
            supabase_user = supabase_auth.get_user(result['access_token'])
            if supabase_user:
                self._sync_user_with_django(request, supabase_user)
            
            logger.info("Sesión de Supabase refrescada correctamente")
        else:
            # No se pudo refrescar, cerrar sesión
            self._cleanup_session(request)
            logger.warning("No se pudo refrescar la sesión de Supabase")
    
    def _cleanup_session(self, request):
        """
        Limpia la sesión cuando los tokens son inválidos
        
        Args:
            request: HttpRequest
        """
        # Eliminar tokens de Supabase de la sesión
        request.session.pop('supabase_access_token', None)
        request.session.pop('supabase_refresh_token', None)
        request.session.pop('supabase_user_metadata', None)
        request.session.modified = True
        
        # Cerrar sesión de Django
        if request.user.is_authenticated:
            django_logout(request)
            logger.info("Sesión de Django cerrada (tokens de Supabase inválidos)")
