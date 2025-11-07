"""
Cliente de Supabase Auth para autenticación completa
Reemplaza el sistema de autenticación de Django con Supabase Auth
"""
from django.conf import settings
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)


class SupabaseAuthClient:
    """Cliente de autenticación con Supabase Auth"""
    
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.supabase_service_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
        self.client = None
        self.admin_client = None
        
        if self.supabase_url and self.supabase_key:
            try:
                # Cliente normal (con anon key) - para operaciones de usuario
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
                logger.info("✅ Supabase Auth cliente inicializado")
                
                # Cliente admin (con service role key) - para operaciones administrativas
                if self.supabase_service_key:
                    self.admin_client: Client = create_client(
                        self.supabase_url, 
                        self.supabase_service_key
                    )
                    logger.info("✅ Supabase Auth admin client inicializado")
                else:
                    logger.warning("⚠️ SUPABASE_SERVICE_ROLE_KEY no configurado")
                    
            except Exception as e:
                logger.error(f"❌ Error al inicializar Supabase Auth: {e}")
    
    def is_available(self):
        """Verifica si Supabase Auth está configurado"""
        return self.client is not None
    
    def is_admin_available(self):
        """Verifica si el cliente admin está disponible"""
        return self.admin_client is not None
    
    def signup(self, email, password, user_metadata=None):
        """
        Registra un nuevo usuario usando Supabase Auth
        Supabase enviará automáticamente el email de confirmación
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña (min 6 caracteres)
            user_metadata (dict): Datos adicionales del usuario
                Ejemplo: {
                    "nombre": "Juan",
                    "apellido": "Pérez",
                    "rol": "estudiante",
                    "carrera_id": 1
                }
        
        Returns:
            dict: {
                "success": bool,
                "user": User object o None,
                "session": Session object o None,
                "message": str,
                "email_sent": bool
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "user": None,
                "session": None,
                "message": "Supabase Auth no está configurado",
                "email_sent": False
            }
        
        try:
            logger.info(f"🔐 Registrando usuario: {email}")
            
            # Preparar datos del usuario
            signup_data = {
                "email": email,
                "password": password,
                "options": {
                    "email_redirect_to": f"{settings.SITE_URL}/auth/callback"
                }
            }
            
            # Agregar metadata si se proporciona
            if user_metadata:
                signup_data["options"]["data"] = user_metadata
            
            # Registrar con Supabase Auth
            response = self.client.auth.sign_up(signup_data)
            
            if response.user:
                logger.info(f"✅ Usuario registrado: {email}")
                logger.info(f"📧 Email de confirmación enviado automáticamente por Supabase")
                
                return {
                    "success": True,
                    "user": response.user,
                    "session": response.session,
                    "message": "¡Registro exitoso! Revisa tu correo para confirmar tu cuenta.",
                    "email_sent": True
                }
            else:
                return {
                    "success": False,
                    "user": None,
                    "session": None,
                    "message": "Error al registrar usuario",
                    "email_sent": False
                }
                
        except Exception as e:
            logger.error(f"❌ Error en signup: {e}")
            error_msg = str(e)
            
            # Mensajes de error personalizados
            if "already registered" in error_msg.lower():
                error_msg = "Este correo ya está registrado"
            elif "password" in error_msg.lower():
                error_msg = "La contraseña debe tener al menos 6 caracteres"
            
            return {
                "success": False,
                "user": None,
                "session": None,
                "message": error_msg,
                "email_sent": False
            }
    
    def signin(self, email, password):
        """
        Inicia sesión con Supabase Auth
        Solo permite login si el email ha sido confirmado
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña
        
        Returns:
            dict: {
                "success": bool,
                "user": User object o None,
                "session": Session object o None,
                "access_token": str o None,
                "refresh_token": str o None,
                "message": str
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "user": None,
                "session": None,
                "access_token": None,
                "refresh_token": None,
                "message": "Supabase Auth no está configurado"
            }
        
        try:
            logger.info(f"🔐 Intento de login: {email}")
            
            # Iniciar sesión con Supabase Auth
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user and response.session:
                logger.info(f"✅ Login exitoso: {email}")
                
                # Verificar si el email está confirmado
                if not response.user.email_confirmed_at:
                    logger.warning(f"⚠️ Email no confirmado: {email}")
                    return {
                        "success": False,
                        "user": None,
                        "session": None,
                        "access_token": None,
                        "refresh_token": None,
                        "message": "Por favor, confirma tu email antes de iniciar sesión"
                    }
                
                return {
                    "success": True,
                    "user": response.user,
                    "session": response.session,
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "message": "Inicio de sesión exitoso"
                }
            else:
                return {
                    "success": False,
                    "user": None,
                    "session": None,
                    "access_token": None,
                    "refresh_token": None,
                    "message": "Credenciales inválidas"
                }
                
        except Exception as e:
            logger.error(f"❌ Error en signin: {e}")
            error_msg = str(e)
            
            # Mensajes de error personalizados
            if "Invalid login credentials" in error_msg or "invalid" in error_msg.lower():
                error_msg = "Email o contraseña incorrectos"
            elif "Email not confirmed" in error_msg:
                error_msg = "Por favor, confirma tu email antes de iniciar sesión"
            
            return {
                "success": False,
                "user": None,
                "session": None,
                "access_token": None,
                "refresh_token": None,
                "message": error_msg
            }
    
    def signout(self):
        """
        Cierra la sesión del usuario
        
        Returns:
            dict: {
                "success": bool,
                "message": str
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "message": "Supabase Auth no está configurado"
            }
        
        try:
            self.client.auth.sign_out()
            logger.info("✅ Sesión cerrada")
            return {
                "success": True,
                "message": "Sesión cerrada correctamente"
            }
        except Exception as e:
            logger.error(f"❌ Error en signout: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    def send_password_reset_email(self, email):
        """
        Envía email de recuperación de contraseña
        Supabase enviará el email automáticamente con un link mágico
        
        Args:
            email (str): Email del usuario
        
        Returns:
            dict: {
                "success": bool,
                "message": str
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "message": "Supabase Auth no está configurado"
            }
        
        try:
            logger.info(f"📧 Enviando email de recuperación a: {email}")
            
            self.client.auth.reset_password_email(
                email,
                {
                    "redirect_to": f"{settings.SITE_URL}/auth/reset-password"
                }
            )
            
            logger.info(f"✅ Email de recuperación enviado a: {email}")
            
            # Por seguridad, siempre devolvemos el mismo mensaje
            return {
                "success": True,
                "message": "Si el correo existe en nuestro sistema, recibirás instrucciones para restablecer tu contraseña"
            }
            
        except Exception as e:
            logger.error(f"❌ Error al enviar email de recuperación: {e}")
            # Por seguridad, siempre devolvemos el mismo mensaje
            return {
                "success": True,
                "message": "Si el correo existe en nuestro sistema, recibirás instrucciones para restablecer tu contraseña"
            }
    
    def update_password(self, new_password, access_token=None):
        """
        Actualiza la contraseña del usuario
        Usar después de que el usuario haga clic en el link del email
        
        Args:
            new_password (str): Nueva contraseña (min 6 caracteres)
            access_token (str): Token de acceso (opcional)
        
        Returns:
            dict: {
                "success": bool,
                "user": User object o None,
                "message": str
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "user": None,
                "message": "Supabase Auth no está configurado"
            }
        
        try:
            if access_token:
                # Establecer sesión con el token
                self.client.auth.set_session(access_token, "")
            
            response = self.client.auth.update_user({
                "password": new_password
            })
            
            if response.user:
                logger.info("✅ Contraseña actualizada")
                return {
                    "success": True,
                    "user": response.user,
                    "message": "Contraseña actualizada correctamente"
                }
            else:
                return {
                    "success": False,
                    "user": None,
                    "message": "Error al actualizar contraseña"
                }
                
        except Exception as e:
            logger.error(f"❌ Error al actualizar contraseña: {e}")
            return {
                "success": False,
                "user": None,
                "message": str(e)
            }
    
    def get_user(self, access_token):
        """
        Obtiene información del usuario usando su access token
        
        Args:
            access_token (str): Token de acceso de Supabase
        
        Returns:
            User object o None
        """
        if not self.is_available():
            return None
        
        try:
            response = self.client.auth.get_user(access_token)
            return response.user if response else None
        except Exception as e:
            logger.error(f"❌ Error al obtener usuario: {e}")
            return None
    
    def refresh_session(self, refresh_token):
        """
        Refresca la sesión usando el refresh token
        
        Args:
            refresh_token (str): Refresh token de Supabase
        
        Returns:
            dict: {
                "success": bool,
                "session": Session object o None,
                "access_token": str o None,
                "message": str
            }
        """
        if not self.is_available():
            return {
                "success": False,
                "session": None,
                "access_token": None,
                "message": "Supabase Auth no está configurado"
            }
        
        try:
            response = self.client.auth.refresh_session(refresh_token)
            
            if response.session:
                logger.info("✅ Sesión refrescada")
                return {
                    "success": True,
                    "session": response.session,
                    "access_token": response.session.access_token,
                    "message": "Sesión refrescada correctamente"
                }
            else:
                return {
                    "success": False,
                    "session": None,
                    "access_token": None,
                    "message": "Error al refrescar sesión"
                }
                
        except Exception as e:
            logger.error(f"❌ Error al refrescar sesión: {e}")
            return {
                "success": False,
                "session": None,
                "access_token": None,
                "message": str(e)
            }


# Instancia global del cliente
supabase_auth = SupabaseAuthClient()
