# -*- coding: utf-8 -*-
"""
Backend de autenticación personalizado para Django
Permite login con username O email
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Backend personalizado que permite autenticación con email o username
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica usuario usando email o username
        
        Args:
            request: HttpRequest object
            username: Puede ser el username o el email
            password: Contraseña del usuario
        
        Returns:
            User object si la autenticación es exitosa, None en caso contrario
        """
        if username is None or password is None:
            return None
        
        try:
            # Intentar encontrar el usuario por username O email
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
            
            # Verificar la contraseña
            if user.check_password(password):
                return user
            
        except User.DoesNotExist:
            # No existe usuario con ese username o email
            return None
        except User.MultipleObjectsReturned:
            # Si hay múltiples usuarios (no debería pasar), devolver None
            return None
        
        return None
    
    def get_user(self, user_id):
        """
        Obtiene un usuario por su ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
