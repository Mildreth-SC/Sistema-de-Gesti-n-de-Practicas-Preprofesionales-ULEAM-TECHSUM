"""
Vistas de autenticación usando Supabase Auth
Reemplaza el sistema de autenticación tradicional de Django
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.db import transaction
from .supabase_client import supabase_auth
from .models import Estudiante, Empresa, Facultad, Carrera
from .forms import (
    EstudianteRegistrationForm,
    EmpresaRegistrationForm,
    FacultadRegistrationForm
)
import logging

logger = logging.getLogger(__name__)


def login_view(request):
    """
    Vista de login usando Supabase Auth
    Permite login con EMAIL o USERNAME
    Verifica que empresas y facultades estén aprobadas por el administrador
    """
    # Si ya está autenticado, redirigir
    if request.user.is_authenticated:
        return _redirect_by_user_type(request.user)
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Validaciones básicas
        if not username_or_email or not password:
            messages.error(request, 'Por favor, ingresa tu usuario/email y contraseña.')
            return render(request, 'inscripciones/login.html')
        
        # Intentar obtener el email del usuario
        # Si ingresó email, usarlo directamente
        # Si ingresó username, buscar el email asociado
        email = username_or_email
        
        # Si no parece un email (no tiene @), buscar el usuario por username
        if '@' not in username_or_email:
            try:
                user_obj = User.objects.get(username__iexact=username_or_email)
                email = user_obj.email
            except User.DoesNotExist:
                messages.error(request, 'Usuario o contraseña incorrectos.')
                return render(request, 'inscripciones/login.html')
        
        # Intentar login con Supabase Auth usando el email
        result = supabase_auth.signin(email, password)
        
        if result['success']:
            # Verificar si es empresa o facultad y si está aprobada
            try:
                django_user = User.objects.get(email=email)
                
                # Verificar aprobación para empresas
                if hasattr(django_user, 'empresa'):
                    empresa = django_user.empresa
                    if empresa.estado_aprobacion == 'pendiente':
                        messages.warning(
                            request,
                            'Tu cuenta está PENDIENTE DE APROBACIÓN por el administrador. '
                            'Recibirás una notificación por email cuando tu cuenta sea aprobada.'
                        )
                        return render(request, 'inscripciones/login.html')
                    
                    elif empresa.estado_aprobacion == 'rechazada':
                        messages.error(
                            request,
                            f'Tu solicitud de registro ha sido RECHAZADA. '
                            f'Motivo: {empresa.observaciones_aprobacion or "No especificado"}. '
                            'Por favor, contacta al administrador para más información.'
                        )
                        return render(request, 'inscripciones/login.html')
                
                # Verificar aprobación para facultades
                elif hasattr(django_user, 'facultad'):
                    facultad = django_user.facultad
                    if facultad.estado_aprobacion == 'pendiente':
                        messages.warning(
                            request,
                            'Tu cuenta está PENDIENTE DE APROBACIÓN por el administrador. '
                            'Recibirás una notificación por email cuando tu cuenta sea aprobada.'
                        )
                        return render(request, 'inscripciones/login.html')
                    
                    elif facultad.estado_aprobacion == 'rechazada':
                        messages.error(
                            request,
                            f'Tu solicitud de registro ha sido RECHAZADA. '
                            f'Motivo: {facultad.observaciones_aprobacion or "No especificado"}. '
                            'Por favor, contacta al administrador para más información.'
                        )
                        return render(request, 'inscripciones/login.html')
                
                # Si llegó aquí, el usuario está aprobado o es estudiante
                # Guardar tokens en la sesión de Django
                request.session['supabase_access_token'] = result['access_token']
                request.session['supabase_refresh_token'] = result['refresh_token']
                
                # Guardar metadata del usuario
                if result['user'].user_metadata:
                    request.session['supabase_user_metadata'] = result['user'].user_metadata
                
                request.session.modified = True
                
                messages.success(request, f'Bienvenido {django_user.get_full_name() or django_user.username}!')
                return _redirect_by_user_type(django_user)
                
            except User.DoesNotExist:
                # El middleware lo creará en el próximo request
                # Guardar tokens en la sesión
                request.session['supabase_access_token'] = result['access_token']
                request.session['supabase_refresh_token'] = result['refresh_token']
                if result['user'].user_metadata:
                    request.session['supabase_user_metadata'] = result['user'].user_metadata
                request.session.modified = True
                
                messages.success(request, f'Bienvenido!')
                return redirect('home')
        else:
            messages.error(request, f'{result["message"]}')
            return render(request, 'inscripciones/login.html')
    
    return render(request, 'inscripciones/login.html')


def logout_view(request):
    """
    Vista de logout - cierra sesión en Supabase y Django
    """
    # Cerrar sesión en Supabase
    supabase_auth.signout()
    
    # Limpiar tokens de la sesión
    request.session.pop('supabase_access_token', None)
    request.session.pop('supabase_refresh_token', None)
    request.session.pop('supabase_user_metadata', None)
    
    # Cerrar sesión en Django
    django_logout(request)
    
    messages.success(request, 'Has cerrado sesión correctamente. ¡Hasta pronto!')
    return redirect('home')


def registro_estudiante(request):
    """
    Registro de estudiante usando Supabase Auth
    """
    if request.user.is_authenticated:
        messages.info(request, 'Ya tienes una cuenta activa.')
        return redirect('home')
    
    if request.method == 'POST':
        form = EstudianteRegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Obtener datos del formulario
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password1']
                    
                    # Metadata del estudiante para Supabase
                    user_metadata = {
                        'nombre': form.cleaned_data['first_name'],
                        'apellido': form.cleaned_data['last_name'],
                        'rol': 'estudiante',
                        'carrera_id': form.cleaned_data['carrera'].id if form.cleaned_data.get('carrera') else None,
                        'telefono': form.cleaned_data.get('telefono', ''),
                    }
                    
                    # Registrar en Supabase Auth
                    result = supabase_auth.signup(
                        email=email,
                        password=password,
                        user_metadata=user_metadata
                    )
                    
                    if result['success']:
                        # Crear usuario de Django (inactivo hasta que confirme email)
                        user = User.objects.create_user(
                            username=email,
                            email=email,
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            is_active=False  # Se activará cuando confirme el email
                        )
                        
                        # Crear perfil de estudiante
                        estudiante = Estudiante.objects.create(
                            user=user,
                            tipo_usuario=form.cleaned_data.get('tipo_usuario', 'estudiante'),
                            carrera=form.cleaned_data.get('carrera'),
                            codigo_estudiante=form.cleaned_data.get('codigo_estudiante', ''),
                            ciclo_actual=form.cleaned_data.get('ciclo_actual') if form.cleaned_data.get('tipo_usuario') == 'estudiante' else None,
                            tipo_titulo=form.cleaned_data.get('tipo_titulo') if form.cleaned_data.get('tipo_usuario') == 'egresado' else None,
                            telefono=form.cleaned_data.get('telefono', ''),
                            direccion=form.cleaned_data.get('direccion', ''),
                            fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento')
                        )
                        
                        tipo = "egresado" if form.cleaned_data.get('tipo_usuario') == 'egresado' else "estudiante"
                        logger.info(f" {tipo.capitalize()} registrado: {email}")
                        
                        messages.success(
                            request,
                            'Registro exitoso. Hemos enviado un correo de confirmación a tu email. '
                            'Por favor, revisa tu bandeja de entrada y confirma tu cuenta para poder iniciar sesión.'
                        )
                        return redirect('login')
                    else:
                        messages.error(request, f'Error al registrar: {result["message"]}')
                        
            except Exception as e:
                logger.error(f"Error al registrar estudiante: {e}")
                # Verificar si es un error de clave duplicada
                error_message = str(e)
                if 'codigo_estudiante' in error_message and 'unique constraint' in error_message.lower():
                    messages.error(request, 'Ya existe un estudiante registrado con este código. Por favor, verifica tu código o contacta al administrador.')
                else:
                    messages.error(request, f'Error al procesar el registro: {error_message}')
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudianteRegistrationForm()
    
    return render(request, 'inscripciones/registro_estudiante.html', {'form': form})


def registro_empresa(request):
    """
    Registro de empresa usando Supabase Auth con documentos legales
    """
    if request.user.is_authenticated:
        messages.info(request, 'Ya tienes una cuenta activa.')
        return redirect('home')
    
    if request.method == 'POST':
        form = EmpresaRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Obtener datos del formulario
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password1']
                    
                    # Metadata de la empresa para Supabase
                    user_metadata = {
                        'nombre': form.cleaned_data['nombre'],
                        'rol': 'empresa',
                        'ruc': form.cleaned_data['ruc'],
                        'sector': form.cleaned_data['sector'],
                        'telefono': form.cleaned_data['telefono'],
                    }
                    
                    # Registrar en Supabase Auth
                    result = supabase_auth.signup(
                        email=email,
                        password=password,
                        user_metadata=user_metadata
                    )
                    
                    if result['success']:
                        # El usuario Django se crea en el formulario
                        # pero está inactivo hasta que el admin apruebe
                        user = form.save()
                        user.is_active = False  # Inactivo hasta aprobación del admin
                        user.save()
                        
                        logger.info(f" Empresa registrada (pendiente de aprobación): {email}")
                        
                        messages.success(
                            request,
                            'Registro enviado exitosamente. Tu solicitud ha sido recibida. '
                            'Tu registro está PENDIENTE DE APROBACIÓN por el administrador. '
                            'Recibirás una notificación por email cuando tu cuenta sea aprobada.'
                        )
                        return redirect('login')
                    else:
                        messages.error(
                            request, 
                            f'Error al registrar en el sistema de autenticación: {result["message"]}'
                        )
                        
            except Exception as e:
                logger.error(f"❌ Error al registrar empresa: {e}")
                messages.error(
                    request, 
                    f'Error al procesar el registro: {str(e)}'
                )
        else:
            # Mostrar errores del formulario de forma clara
            messages.error(
                request,
                'Por favor, corrige los siguientes errores:'
            )
            for field, errors in form.errors.items():
                field_label = form.fields[field].label if field in form.fields else field
                for error in errors:
                    messages.error(request, f'{field_label}: {error}')
    else:
        form = EmpresaRegistrationForm()
    
    return render(request, 'inscripciones/registro_empresa.html', {'form': form})


def registro_facultad(request):
    """
    Registro de facultad usando Supabase Auth con documentos de autorización
    """
    if request.user.is_authenticated:
        messages.info(request, 'Ya tienes una cuenta activa.')
        return redirect('home')
    
    if request.method == 'POST':
        form = FacultadRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Obtener datos del formulario
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password1']
                    
                    # Metadata de la facultad para Supabase
                    user_metadata = {
                        'nombre': form.cleaned_data['nombre'],
                        'rol': 'facultad',
                        'codigo': form.cleaned_data['codigo'],
                        'telefono': form.cleaned_data['telefono'],
                    }
                    
                    # Registrar en Supabase Auth
                    result = supabase_auth.signup(
                        email=email,
                        password=password,
                        user_metadata=user_metadata
                    )
                    
                    if result['success']:
                        # El usuario Django se crea en el formulario
                        # pero está inactivo hasta que el admin apruebe
                        user = form.save()
                        user.is_active = False  # Inactivo hasta aprobación del admin
                        user.save()
                        
                        logger.info(f" Facultad registrada (pendiente de aprobación): {email}")
                        
                        messages.success(
                            request,
                            'Registro enviado exitosamente. Tu solicitud ha sido recibida. '
                            'Tu registro está PENDIENTE DE APROBACIÓN por el administrador. '
                            'Recibirás una notificación por email cuando tu cuenta sea aprobada.'
                        )
                        return redirect('login')
                    else:
                        messages.error(
                            request,
                            f'Error al registrar en el sistema de autenticación: {result["message"]}'
                        )
                        
            except Exception as e:
                logger.error(f" Error al registrar facultad: {e}")
                messages.error(
                    request, 
                    f'Error al procesar el registro: {str(e)}'
                )
        else:
            # Mostrar errores del formulario de forma clara
            messages.error(
                request,
                'Por favor, corrige los siguientes errores:'
            )
            for field, errors in form.errors.items():
                field_label = form.fields[field].label if field in form.fields else field
                for error in errors:
                    messages.error(request, f'{field_label}: {error}')
    else:
        form = FacultadRegistrationForm()
    
    return render(request, 'inscripciones/registro_facultad.html', {'form': form})


def solicitar_reset_password(request):
    """
    Solicitar restablecimiento de contraseña usando Supabase Auth
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Por favor, ingresa tu correo electrónico.')
            return render(request, 'inscripciones/solicitar_reset_password.html')
        
        # Enviar email de recuperación con Supabase
        result = supabase_auth.send_password_reset_email(email)
        
        # Siempre mostramos el mismo mensaje por seguridad
        messages.success(
            request,
            '📧 Si el correo existe en nuestro sistema, recibirás instrucciones '
            'para restablecer tu contraseña. Por favor, revisa tu bandeja de entrada.'
        )
        return redirect('login')
    
    return render(request, 'inscripciones/solicitar_reset_password.html')


def reset_password_callback(request):
    """
    Callback después de hacer clic en el link del email de recuperación
    Aquí el usuario puede establecer su nueva contraseña
    """
    # Obtener el access_token del hash de la URL (#access_token=...)
    # Este token viene en el fragmento de la URL, lo manejamos con JavaScript
    # y lo enviamos al backend
    
    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        
        # Validaciones
        if not all([access_token, new_password, confirm_password]):
            messages.error(request, 'Por favor, completa todos los campos.')
            return render(request, 'inscripciones/reset_password_supabase.html')
        
        if new_password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'inscripciones/reset_password_supabase.html')
        
        if len(new_password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return render(request, 'inscripciones/reset_password_supabase.html')
        
        # Actualizar contraseña con Supabase
        result = supabase_auth.update_password(new_password, access_token)
        
        if result['success']:
            messages.success(
                request,
                'Tu contraseña ha sido actualizada exitosamente. '
                'Ahora puedes iniciar sesión con tu nueva contraseña.'
            )
            return redirect('login')
        else:
            messages.error(request, f'Error al actualizar contraseña: {result["message"]}')
            return render(request, 'inscripciones/reset_password_supabase.html')
    
    return render(request, 'inscripciones/reset_password_supabase.html')


def auth_callback(request):
    """
    Callback para confirmación de email
    Supabase redirige aquí después de que el usuario confirma su email
    """
    # El access_token viene en el fragmento de la URL (#access_token=...)
    # Lo manejamos con JavaScript en el template
    
    messages.success(
        request,
        'Tu email ha sido confirmado exitosamente. '
        'Ahora puedes iniciar sesión con tus credenciales.'
    )
    return redirect('login')


# Función auxiliar
def _redirect_by_user_type(user):
    """Redirige según el tipo de usuario"""
    if hasattr(user, 'empresa'):
        return redirect('panel_empresa')
    elif hasattr(user, 'facultad'):
        return redirect('panel_facultad')
    elif hasattr(user, 'estudiante'):
        return redirect('home')
    else:
        return redirect('home')
