# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def estudiante_required(view_func):
    """
    Decorador para verificar que el usuario tenga un perfil de estudiante
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not hasattr(request.user, 'estudiante'):
            messages.error(request, 'Necesitas un perfil de estudiante para acceder a esta función.')
            return redirect('perfil_estudiante')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def empresa_required(view_func):
    """
    Decorador para verificar que el usuario sea una empresa
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not hasattr(request.user, 'empresa'):
            messages.error(request, 'Necesitas un perfil de empresa para acceder a esta función.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def facultad_required(view_func):
    """
    Decorador para verificar que el usuario sea una facultad
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not hasattr(request.user, 'facultad'):
            messages.error(request, 'Necesitas un perfil de facultad para acceder a esta función.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper
