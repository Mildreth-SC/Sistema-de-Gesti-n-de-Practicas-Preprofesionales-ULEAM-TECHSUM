"""
Servicio de autenticación integrado con Supabase Auth
Proporciona funciones para registro, login, verificación de email y recuperación de contraseña
"""
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)


class SupabaseAuthService:
    """Servicio de autenticación con Supabase"""
    
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.supabase_service_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
        self.client = None
        self.admin_client = None
        
        if self.supabase_url and self.supabase_key:
            try:
                # Cliente normal (con anon key)
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
                
                # Cliente admin (con service role key) para enviar emails
                if self.supabase_service_key:
                    self.admin_client: Client = create_client(
                        self.supabase_url, 
                        self.supabase_service_key
                    )
                    logger.info("Supabase Auth inicializado con service role key")
                else:
                    logger.warning("SUPABASE_SERVICE_ROLE_KEY no configurado - algunas funciones estarán limitadas")
                    
            except Exception as e:
                logger.error(f"Error al inicializar cliente Supabase: {e}")
    
    def is_available(self):
        """Verifica si Supabase está configurado"""
        return self.client is not None
    
    def is_admin_available(self):
        """Verifica si el cliente admin está disponible"""
        return self.admin_client is not None
    
    def send_verification_email(self, user, request=None):
        """
        Envía email de verificación al usuario
        
        Primero intenta usar Supabase Auth (si está configurado con SMTP personalizado)
        Si falla, usa Django Email como fallback
        
        Args:
            user: Instancia del modelo User de Django
            request: Request de Django para construir URLs absolutas
        
        Returns:
            bool: True si el email se envió correctamente
        """
        # Intentar usar Supabase Auth si está disponible
        if self.is_admin_available():
            try:
                logger.info(f"Intentando enviar email de verificación via Supabase Auth para {user.email}")
                
                # Generar token y URL
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                if request:
                    verification_url = request.build_absolute_uri(
                        f'/verificar-email/{uid}/{token}/'
                    )
                else:
                    verification_url = f"{settings.SITE_URL}/verificar-email/{uid}/{token}/"
                
                # Usar Supabase Auth para enviar email
                # Supabase maneja los templates desde su dashboard
                response = self.admin_client.auth.admin.generate_link({
                    "type": "signup",
                    "email": user.email,
                    "options": {
                        "redirect_to": verification_url
                    }
                })
                
                if response:
                    logger.info(f"Email de verificación enviado via Supabase Auth a {user.email}")
                    return True
                    
            except Exception as e:
                logger.warning(f"Error con Supabase Auth, usando Django Email como fallback: {e}")
        
        # Fallback: Usar Django Email
        try:
            # Generar token de verificación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construir URL de verificación
            if request:
                verification_url = request.build_absolute_uri(
                    f'/verificar-email/{uid}/{token}/'
                )
            else:
                verification_url = f"{settings.SITE_URL}/verificar-email/{uid}/{token}/"
            
            # Contexto para el template
            context = {
                'user': user,
                'verification_url': verification_url,
                'site_name': 'Sistema de Gestión de Prácticas - ULEAM',
            }
            
            # Renderizar email HTML
            html_message = render_to_string('inscripciones/emails/verificacion_email.html', context)
            plain_message = strip_tags(html_message)
            
            # Enviar email
            send_mail(
                subject='Verifica tu cuenta - Sistema de Prácticas ULEAM',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Email de verificación enviado via Django Email a {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar email de verificación: {e}")
            return False
    
    def verify_email_token(self, uidb64, token):
        """
        Verifica el token de email
        
        Args:
            uidb64: User ID codificado en base64
            token: Token de verificación
        
        Returns:
            User|None: Usuario si el token es válido, None en caso contrario
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                return user
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
        
        return None
    
    def send_password_reset_email(self, user, request=None):
        """
        Envía email para resetear contraseña
        
        Primero intenta usar Supabase Auth (si está configurado)
        Si falla, usa Django Email como fallback
        
        Args:
            user: Instancia del modelo User de Django
            request: Request de Django para construir URLs absolutas
        
        Returns:
            bool: True si el email se envió correctamente
        """
        # Intentar usar Supabase Auth si está disponible
        if self.is_admin_available():
            try:
                logger.info(f"Intentando enviar email de reset via Supabase Auth para {user.email}")
                
                # Generar token y URL
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                if request:
                    reset_url = request.build_absolute_uri(
                        f'/restablecer-contrasena/{uid}/{token}/'
                    )
                else:
                    reset_url = f"{settings.SITE_URL}/restablecer-contrasena/{uid}/{token}/"
                
                # Usar Supabase Auth para enviar email
                response = self.admin_client.auth.admin.generate_link({
                    "type": "recovery",
                    "email": user.email,
                    "options": {
                        "redirect_to": reset_url
                    }
                })
                
                if response:
                    logger.info(f"Email de recuperación enviado via Supabase Auth a {user.email}")
                    return True
                    
            except Exception as e:
                logger.warning(f"Error con Supabase Auth, usando Django Email como fallback: {e}")
        
        # Fallback: Usar Django Email
        try:
            # Generar token de reset
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construir URL de reset
            if request:
                reset_url = request.build_absolute_uri(
                    f'/restablecer-contrasena/{uid}/{token}/'
                )
            else:
                reset_url = f"{settings.SITE_URL}/restablecer-contrasena/{uid}/{token}/"
            
            # Contexto para el template
            context = {
                'user': user,
                'reset_url': reset_url,
                'site_name': 'Sistema de Gestión de Prácticas - ULEAM',
            }
            
            # Renderizar email HTML
            html_message = render_to_string('inscripciones/emails/reset_password.html', context)
            plain_message = strip_tags(html_message)
            
            # Enviar email
            send_mail(
                subject='Recuperación de Contraseña - Sistema de Prácticas ULEAM',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Email de recuperación enviado via Django Email a {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar email de recuperación: {e}")
            return False
    
    def register_with_supabase(self, email, password):
        """
        Registra usuario en Supabase Auth
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
        
        Returns:
            dict|None: Datos del usuario de Supabase o None si falla
        """
        if not self.is_available():
            logger.warning("Supabase no está configurado, usando solo Django Auth")
            return None
        
        try:
            # Registrar en Supabase Auth
            # Supabase enviará automáticamente el email de confirmación
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
            })
            
            if response.user:
                logger.info(f"Usuario registrado en Supabase Auth: {email}")
                logger.info(f"Email de confirmación enviado automáticamente por Supabase a {email}")
                return response.user
            
        except Exception as e:
            logger.error(f"Error al registrar en Supabase Auth: {e}")
        
        return None
    
    def sign_in_with_supabase(self, email, password):
        """
        Inicia sesión con Supabase Auth
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
        
        Returns:
            dict|None: Sesión de Supabase o None si falla
        """
        if not self.is_available():
            return None
        
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            
            if response.session:
                logger.info(f"Usuario autenticado en Supabase Auth: {email}")
                return response.session
            
        except Exception as e:
            logger.error(f"Error al iniciar sesión en Supabase Auth: {e}")
        
        return None
    
    def send_password_recovery_email(self, email):
        """
        Envía email de recuperación de contraseña usando Supabase Auth
        
        Args:
            email: Email del usuario
        
        Returns:
            bool: True si el email se envió correctamente
        """
        if not self.is_available():
            logger.warning("Supabase no está configurado")
            return False
        
        try:
            # Supabase enviará automáticamente el email de recuperación
            self.client.auth.reset_password_email(email)
            logger.info(f"Email de recuperación enviado automáticamente por Supabase a {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar email de recuperación con Supabase: {e}")
            return False


# Instancia global del servicio
supabase_auth = SupabaseAuthService()
