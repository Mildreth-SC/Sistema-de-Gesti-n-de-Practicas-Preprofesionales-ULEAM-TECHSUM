from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from .models import Practica, Inscripcion, Estudiante, Empresa, Carrera, DocumentoInscripcion, Facultad, PracticaInterna, InscripcionInterna
from .decorators import estudiante_required
from .forms import (
    EstudianteRegistrationForm, EstudianteUpdateForm, EmpresaForm, 
    PracticaForm, InscripcionForm, DocumentoInscripcionForm, BusquedaPracticasForm,
    EmpresaRegistrationForm, FacultadRegistrationForm, PracticaInternaForm, 
    InscripcionInternaForm, BusquedaPracticasInternasForm, EstudianteProfileForm,
    UserUpdateForm
)


def login_view(request):
    """Vista de login personalizada con mensajes de error"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Por favor, ingresa tu usuario y contraseña.')
            return render(request, 'inscripciones/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.get_full_name() or user.username}!')
            
            # Redirigir según el tipo de usuario
            if hasattr(user, 'empresa'):
                return redirect('panel_empresa')
            elif hasattr(user, 'facultad'):
                return redirect('panel_facultad')
            elif hasattr(user, 'estudiante'):
                return redirect('home')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Por favor, verifica tus credenciales.')
            return render(request, 'inscripciones/login.html')
    
    return render(request, 'inscripciones/login.html')


def logout_view(request):
    """Vista de logout personalizada con mensaje"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente. ¡Hasta pronto!')
    return redirect('home')


def home(request):
    """Vista principal del sistema"""
    practicas_destacadas = Practica.objects.filter(
        activa=True, 
        estado='disponible',
        fecha_limite_inscripcion__gte=timezone.now()
    ).order_by('-fecha_publicacion')[:6]
    
    empresas_destacadas = Empresa.objects.filter(activa=True).order_by('-fecha_registro')[:4]
    
    # Estadísticas para la página principal
    total_empresas = Empresa.objects.filter(activa=True).count()
    total_practicas = Practica.objects.filter(activa=True).count()
    total_estudiantes = Estudiante.objects.filter(user__is_active=True).count()
    total_facultades = Facultad.objects.filter(activa=True).count()
    
    context = {
        'practicas_destacadas': practicas_destacadas,
        'empresas_destacadas': empresas_destacadas,
        'total_empresas': total_empresas,
        'total_practicas': total_practicas,
        'total_estudiantes': total_estudiantes,
        'total_facultades': total_facultades,
    }
    return render(request, 'inscripciones/home.html', context)


def lista_practicas(request):
    """Lista todas las prácticas disponibles con filtros"""
    practicas = Practica.objects.filter(
        activa=True,
        fecha_limite_inscripcion__gte=timezone.now()
    ).order_by('-fecha_publicacion')
    
    form = BusquedaPracticasForm(request.GET)
    
    if form.is_valid():
        titulo = form.cleaned_data.get('titulo')
        empresa = form.cleaned_data.get('empresa')
        sector = form.cleaned_data.get('sector')
        fecha_desde = form.cleaned_data.get('fecha_inicio_desde')
        fecha_hasta = form.cleaned_data.get('fecha_inicio_hasta')
        
        if titulo:
            practicas = practicas.filter(titulo__icontains=titulo)
        if empresa:
            practicas = practicas.filter(empresa=empresa)
        if sector:
            practicas = practicas.filter(empresa__sector__icontains=sector)
        if fecha_desde:
            practicas = practicas.filter(fecha_inicio__gte=fecha_desde)
        if fecha_hasta:
            practicas = practicas.filter(fecha_inicio__lte=fecha_hasta)
    
    paginator = Paginator(practicas, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'inscripciones/lista_practicas.html', context)


def lista_practicas_internas(request):
    """Lista todas las prácticas internas activas de facultades"""
    form = BusquedaPracticasInternasForm(request.GET or None)
    
    practicas = PracticaInterna.objects.filter(
        activa=True,
        fecha_limite_inscripcion__gte=timezone.now()
    ).select_related('facultad').order_by('-fecha_publicacion')
    
    # Aplicar filtros si existen
    if form.is_valid():
        titulo = form.cleaned_data.get('titulo')
        facultad = form.cleaned_data.get('facultad')
        tipo_servicio = form.cleaned_data.get('tipo_servicio')
        fecha_desde = form.cleaned_data.get('fecha_inicio_desde')
        fecha_hasta = form.cleaned_data.get('fecha_inicio_hasta')
        
        if titulo:
            practicas = practicas.filter(Q(titulo__icontains=titulo) | Q(descripcion_proyecto__icontains=titulo))
        if facultad:
            practicas = practicas.filter(facultad=facultad)
        if tipo_servicio:
            practicas = practicas.filter(tipo_servicio=tipo_servicio)
        if fecha_desde:
            practicas = practicas.filter(fecha_inicio__gte=fecha_desde)
        if fecha_hasta:
            practicas = practicas.filter(fecha_inicio__lte=fecha_hasta)
    
    paginator = Paginator(practicas, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'inscripciones/lista_practicas_internas.html', context)


def detalle_practica(request, pk):
    """Detalle de una práctica específica"""
    practica = get_object_or_404(Practica, pk=pk, activa=True)
    
    # Verificar si el usuario está inscrito
    inscrito = False
    inscripcion = None
    if request.user.is_authenticated:
        try:
            estudiante = Estudiante.objects.get(user=request.user)
            inscripcion = Inscripcion.objects.get(estudiante=estudiante, practica=practica)
            inscrito = True
        except (Estudiante.DoesNotExist, Inscripcion.DoesNotExist):
            pass
    
    context = {
        'practica': practica,
        'inscrito': inscrito,
        'inscripcion': inscripcion,
        'now': timezone.now(),
    }
    return render(request, 'inscripciones/detalle_practica.html', context)


def detalle_practica_interna(request, pk):
    """Detalle de una práctica interna específica"""
    practica = get_object_or_404(PracticaInterna, pk=pk, activa=True)
    
    # Verificar si el usuario está inscrito
    inscrito = False
    inscripcion = None
    if request.user.is_authenticated:
        try:
            estudiante = Estudiante.objects.get(user=request.user)
            inscripcion = InscripcionInterna.objects.get(estudiante=estudiante, practica_interna=practica)
            inscrito = True
        except (Estudiante.DoesNotExist, InscripcionInterna.DoesNotExist):
            pass
    
    context = {
        'practica': practica,
        'inscrito': inscrito,
        'inscripcion': inscripcion,
        'now': timezone.now(),
    }
    return render(request, 'inscripciones/detalle_practica_interna.html', context)


@estudiante_required
def inscribirse_practica(request, pk):
    """Inscripción a una práctica"""
    practica = get_object_or_404(Practica, pk=pk, activa=True)
    
    try:
        estudiante = Estudiante.objects.get(user=request.user)
    except Estudiante.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil de estudiante primero.')
        return redirect('perfil_estudiante')
    
    # Verificar si ya está inscrito
    inscripcion_existente = Inscripcion.objects.filter(estudiante=estudiante, practica=practica).first()
    if inscripcion_existente:
        messages.warning(request, f'Ya estás inscrito en esta práctica. Tu inscripción fue realizada el {inscripcion_existente.fecha_inscripcion.strftime("%d/%m/%Y")}.')
        return redirect('mis_inscripciones')
    
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            try:
                # Usar transacción atómica con bloqueo para evitar race conditions
                with transaction.atomic():
                    # Bloquear la fila de la práctica para lectura/escritura
                    practica_locked = Practica.objects.select_for_update().get(pk=pk)
                    
                    # Verificar si puede inscribirse (dentro de la transacción)
                    if not practica_locked.puede_inscribirse:
                        messages.error(request, 'No puedes inscribirte en esta práctica. Puede que los cupos se hayan agotado.')
                        return redirect('detalle_practica', pk=pk)
                    
                    # Verificar nuevamente duplicados (por si acaso)
                    if Inscripcion.objects.filter(estudiante=estudiante, practica=practica_locked).exists():
                        messages.warning(request, 'Ya estás inscrito en esta práctica. No puedes inscribirte dos veces.')
                        return redirect('mis_inscripciones')
                    
                    # Crear inscripción
                    inscripcion = form.save(commit=False)
                    inscripcion.estudiante = estudiante
                    inscripcion.practica = practica_locked
                    inscripcion.save()
                    
                    # Reducir cupos disponibles de forma segura
                    practica_locked.cupos_disponibles -= 1
                    practica_locked.save(update_fields=['cupos_disponibles'])
                    
                messages.success(request, f'¡Felicidades! Te has inscrito exitosamente en la práctica "{practica_locked.titulo}". Puedes ver el estado de tu inscripción en "Mis Inscripciones".')
                return redirect('mis_inscripciones')
            except Exception as e:
                messages.error(request, f'Error al procesar tu inscripción: {str(e)}. Por favor, intenta nuevamente.')
                return redirect('detalle_practica', pk=pk)
    else:
        # Verificar si puede inscribirse (antes de mostrar formulario)
        if not practica.puede_inscribirse:
            messages.error(request, 'No puedes inscribirte en esta práctica.')
            return redirect('detalle_practica', pk=pk)
        form = InscripcionForm()
    
    context = {
        'practica': practica,
        'form': form,
    }
    return render(request, 'inscripciones/inscribirse_practica.html', context)


@estudiante_required
def mis_inscripciones(request):
    """Lista las inscripciones del estudiante"""
    try:
        estudiante = Estudiante.objects.get(user=request.user)
        inscripciones = Inscripcion.objects.filter(estudiante=estudiante).order_by('-fecha_inscripcion')
        
        # Filtro por estado si está presente
        estado = request.GET.get('estado')
        if estado:
            inscripciones = inscripciones.filter(estado=estado)
        
        context = {
            'inscripciones': inscripciones,
        }
        return render(request, 'inscripciones/mis_inscripciones.html', context)
    except Estudiante.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil de estudiante primero.')
        return redirect('perfil_estudiante')


@estudiante_required
def cancelar_inscripcion(request, pk):
    """Cancelar una inscripción"""
    inscripcion = get_object_or_404(Inscripcion, pk=pk, estudiante__user=request.user)
    
    # Solo se puede cancelar si está pendiente
    if inscripcion.estado != 'pendiente':
        messages.error(request, 'Solo puedes cancelar inscripciones pendientes.')
        return redirect('mis_inscripciones')
    
    # Verificar que la fecha límite no haya pasado (opcional pero recomendado)
    if timezone.now() > inscripcion.practica.fecha_limite_inscripcion:
        messages.error(request, 'Ya pasó la fecha límite para cancelar esta inscripción.')
        return redirect('mis_inscripciones')
    
    try:
        with transaction.atomic():
            # Bloquear para actualización
            practica = Practica.objects.select_for_update().get(pk=inscripcion.practica.pk)
            
            # Cambiar estado de inscripción
            inscripcion.estado = 'cancelada'
            inscripcion.save(update_fields=['estado'])
            
            # Restaurar cupo disponible
            practica.cupos_disponibles += 1
            practica.save(update_fields=['cupos_disponibles'])
            
        messages.success(request, 'Inscripción cancelada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al cancelar la inscripción: {str(e)}')
    
    return redirect('mis_inscripciones')


@estudiante_required
def inscribirse_practica_interna(request, pk):
    """Inscripción a una práctica interna"""
    practica = get_object_or_404(PracticaInterna, pk=pk, activa=True)
    
    try:
        estudiante = Estudiante.objects.get(user=request.user)
    except Estudiante.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil de estudiante primero.')
        return redirect('perfil_estudiante')
    
    # Verificar si ya está inscrito
    inscripcion_existente = InscripcionInterna.objects.filter(estudiante=estudiante, practica_interna=practica).first()
    if inscripcion_existente:
        messages.warning(request, f'Ya estás inscrito en esta práctica. Tu inscripción fue realizada el {inscripcion_existente.fecha_inscripcion.strftime("%d/%m/%Y")}.')
        return redirect('mis_inscripciones')
    
    if request.method == 'POST':
        form = InscripcionInternaForm(request.POST)
        if form.is_valid():
            try:
                # Usar transacción atómica con bloqueo
                with transaction.atomic():
                    # Bloquear la fila de la práctica
                    practica_locked = PracticaInterna.objects.select_for_update().get(pk=pk)
                    
                    # Verificar cupos disponibles
                    if practica_locked.cupos_disponibles <= 0:
                        messages.error(request, 'No hay cupos disponibles para esta práctica.')
                        return redirect('detalle_practica_interna', pk=pk)
                    
                    # Verificar fecha límite
                    if timezone.now() > practica_locked.fecha_limite_inscripcion:
                        messages.error(request, 'La fecha límite de inscripción ha pasado.')
                        return redirect('detalle_practica_interna', pk=pk)
                    
                    # Verificar duplicados
                    if InscripcionInterna.objects.filter(estudiante=estudiante, practica_interna=practica_locked).exists():
                        messages.warning(request, 'Ya estás inscrito en esta práctica.')
                        return redirect('mis_inscripciones')
                    
                    # Crear inscripción
                    inscripcion = form.save(commit=False)
                    inscripcion.estudiante = estudiante
                    inscripcion.practica_interna = practica_locked
                    inscripcion.save()
                    
                    # Reducir cupos disponibles
                    practica_locked.cupos_disponibles -= 1
                    practica_locked.save(update_fields=['cupos_disponibles'])
                
                messages.success(request, '¡Inscripción realizada exitosamente!')
                return redirect('mis_inscripciones')
            except Exception as e:
                messages.error(request, f'Error al procesar la inscripción: {str(e)}')
                return redirect('detalle_practica_interna', pk=pk)
    else:
        form = InscripcionInternaForm()
    
    context = {
        'practica': practica,
        'form': form,
    }
    return render(request, 'inscripciones/inscribirse_practica_interna.html', context)


@estudiante_required
def cancelar_inscripcion_interna(request, pk):
    """Cancelar una inscripción interna"""
    inscripcion = get_object_or_404(InscripcionInterna, pk=pk, estudiante__user=request.user)
    
    # Solo se puede cancelar si está pendiente
    if inscripcion.estado != 'pendiente':
        messages.error(request, 'Solo puedes cancelar inscripciones pendientes.')
        return redirect('mis_inscripciones')
    
    # Verificar que la fecha límite no haya pasado
    if timezone.now() > inscripcion.practica_interna.fecha_limite_inscripcion:
        messages.error(request, 'Ya pasó la fecha límite para cancelar esta inscripción.')
        return redirect('mis_inscripciones')
    
    try:
        with transaction.atomic():
            # Bloquear para actualización
            practica = PracticaInterna.objects.select_for_update().get(pk=inscripcion.practica_interna.pk)
            
            # Cambiar estado de inscripción
            inscripcion.estado = 'cancelada'
            inscripcion.save(update_fields=['estado'])
            
            # Restaurar cupo disponible
            practica.cupos_disponibles += 1
            practica.save(update_fields=['cupos_disponibles'])
            
        messages.success(request, 'Inscripción cancelada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al cancelar la inscripción: {str(e)}')
    
    return redirect('mis_inscripciones')


def registro_estudiante(request):
    """Registro de nuevos estudiantes"""
    if request.user.is_authenticated:
        # Si el usuario autenticado ya tiene un perfil, redirigir a home.
        if hasattr(request.user, 'estudiante'):
            return redirect('home')
        # Si no tiene perfil, se podría redirigir a una página para crearlo,
        # pero por ahora, lo más simple es permitir que la vista continúe
        # para que pueda crear su perfil si llega aquí.
        # Sin embargo, el flujo normal es que sea redirigido a 'perfil_estudiante'
        # y desde allí se le pida crear el perfil.
        pass

    if request.method == 'POST':
        form = EstudianteRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, '¡Cuenta creada exitosamente! Por favor, inicia sesión con tus credenciales.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {str(e)}')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    if field == 'username':
                        messages.error(request, f'Usuario: {error}')
                    elif field == 'email':
                        messages.error(request, f'Email: {error}')
                    elif field == 'codigo_estudiante':
                        messages.error(request, f'Código de Estudiante: {error}')
                    elif field == 'password2':
                        messages.error(request, f'Contraseña: {error}')
                    else:
                        messages.error(request, f'{field}: {error}')
    else:
        form = EstudianteRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inscripciones/registro_estudiante.html', context)


def registro_empresa(request):
    """Registro de nuevas empresas"""
    if request.method == 'POST':
        form = EmpresaRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, '¡Empresa registrada exitosamente! Por favor, inicia sesión con tus credenciales.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error al registrar la empresa: {str(e)}')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    if field == 'username':
                        messages.error(request, f'Usuario: {error}')
                    elif field == 'email':
                        messages.error(request, f'Email: {error}')
                    elif field == 'ruc':
                        messages.error(request, f'RUC: {error}')
                    elif field == 'password2':
                        messages.error(request, f'Contraseña: {error}')
                    else:
                        messages.error(request, f'{error}')
    else:
        form = EmpresaRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inscripciones/registro_empresa.html', context)


def registro_facultad(request):
    """Registro de nuevas facultades"""
    if request.method == 'POST':
        form = FacultadRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, '¡Facultad registrada exitosamente! Por favor, inicia sesión con tus credenciales.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error al registrar la facultad: {str(e)}')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    if field == 'username':
                        messages.error(request, f'Usuario: {error}')
                    elif field == 'email':
                        messages.error(request, f'Email: {error}')
                    elif field == 'codigo':
                        messages.error(request, f'Código: {error}')
                    elif field == 'password2':
                        messages.error(request, f'Contraseña: {error}')
                    else:
                        messages.error(request, f'{error}')
    else:
        form = FacultadRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inscripciones/registro_facultad.html', context)


@login_required
def perfil_estudiante(request):
    """Perfil del estudiante"""
    try:
        estudiante = Estudiante.objects.get(user=request.user)
        # Si el perfil existe, se usan los formularios de actualización
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            estudiante_form = EstudianteUpdateForm(request.POST, request.FILES, instance=estudiante)
            if user_form.is_valid() and estudiante_form.is_valid():
                user_form.save()
                estudiante_form.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('perfil_estudiante')
        else:
            user_form = UserUpdateForm(instance=request.user)
            estudiante_form = EstudianteUpdateForm(instance=estudiante)
        
        context = {
            'estudiante': estudiante,
            'user_form': user_form,
            'estudiante_form': estudiante_form,
            'has_profile': True
        }
        return render(request, 'inscripciones/perfil_estudiante.html', context)

    except Estudiante.DoesNotExist:
        # Si el perfil no existe, se usa el formulario de creación de perfil
        if request.method == 'POST':
            form = EstudianteProfileForm(request.POST, request.FILES)
            if form.is_valid():
                perfil = form.save(commit=False)
                perfil.user = request.user
                perfil.save()
                messages.success(request, 'Perfil completado exitosamente.')
                return redirect('perfil_estudiante')
        else:
            form = EstudianteProfileForm()
        
        context = {
            'form': form,
            'has_profile': False
        }
        return render(request, 'inscripciones/perfil_estudiante.html', context)


def lista_empresas(request):
    """Lista todas las empresas"""
    empresas = Empresa.objects.filter(activa=True).order_by('nombre')
    
    paginator = Paginator(empresas, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'inscripciones/lista_empresas.html', context)


def detalle_empresa(request, pk):
    """Detalle de una empresa"""
    empresa = get_object_or_404(Empresa, pk=pk, activa=True)
    practicas = Practica.objects.filter(empresa=empresa, activa=True).order_by('-fecha_publicacion')
    
    context = {
        'empresa': empresa,
        'practicas': practicas,
    }
    return render(request, 'inscripciones/detalle_empresa.html', context)


@estudiante_required
def gestionar_documentos(request, inscripcion_pk):
    """Gestión de documentos de una inscripción"""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_pk, estudiante__user=request.user)
    
    if request.method == 'POST':
        form = DocumentoInscripcionForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.inscripcion = inscripcion
            documento.save()
            messages.success(request, 'Documento subido exitosamente.')
            return redirect('gestionar_documentos', inscripcion_pk=inscripcion_pk)
    else:
        form = DocumentoInscripcionForm()
    
    documentos = inscripcion.documentos.all()
    
    context = {
        'inscripcion': inscripcion,
        'documentos': documentos,
        'form': form,
    }
    return render(request, 'inscripciones/gestionar_documentos.html', context)


@estudiante_required
def eliminar_documento(request, documento_pk):
    """Eliminar un documento"""
    documento = get_object_or_404(DocumentoInscripcion, pk=documento_pk, inscripcion__estudiante__user=request.user)
    inscripcion_pk = documento.inscripcion.pk
    documento.delete()
    messages.success(request, 'Documento eliminado exitosamente.')
    return redirect('gestionar_documentos', inscripcion_pk=inscripcion_pk)


@estudiante_required
def detalle_inscripcion(request, pk):
    """Ver detalles de una inscripción específica"""
    inscripcion = get_object_or_404(Inscripcion, pk=pk, estudiante__user=request.user)
    documentos = inscripcion.documentos.all()
    
    context = {
        'inscripcion': inscripcion,
        'documentos': documentos,
    }
    return render(request, 'inscripciones/detalle_inscripcion.html', context)


# ============================================
# VISTAS PARA EMPRESAS
# ============================================

@login_required
def panel_empresa(request):
    """Panel de control para empresas"""
    from .decorators import empresa_required
    
    if not hasattr(request.user, 'empresa'):
        messages.error(request, 'No tienes un perfil de empresa.')
        return redirect('home')
    
    empresa = request.user.empresa
    practicas = Practica.objects.filter(empresa=empresa).order_by('-fecha_publicacion')
    
    # Estadísticas
    total_practicas = practicas.count()
    practicas_activas = practicas.filter(activa=True, estado='disponible').count()
    total_postulaciones = Inscripcion.objects.filter(practica__empresa=empresa).count()
    postulaciones_pendientes = Inscripcion.objects.filter(practica__empresa=empresa, estado='pendiente').count()
    
    context = {
        'empresa': empresa,
        'practicas': practicas[:5],  # Últimas 5 prácticas
        'total_practicas': total_practicas,
        'practicas_activas': practicas_activas,
        'total_postulaciones': total_postulaciones,
        'postulaciones_pendientes': postulaciones_pendientes,
    }
    return render(request, 'inscripciones/panel_empresa.html', context)


@login_required
def mis_practicas_empresa(request):
    """Lista de todas las prácticas de la empresa"""
    if not hasattr(request.user, 'empresa'):
        messages.error(request, 'No tienes un perfil de empresa.')
        return redirect('home')
    
    empresa = request.user.empresa
    practicas = Practica.objects.filter(empresa=empresa).order_by('-fecha_publicacion')
    
    # Filtros
    estado = request.GET.get('estado')
    if estado:
        practicas = practicas.filter(estado=estado)
    
    paginator = Paginator(practicas, 10)
    page = request.GET.get('page')
    practicas = paginator.get_page(page)
    
    context = {
        'empresa': empresa,
        'practicas': practicas,
    }
    return render(request, 'inscripciones/mis_practicas_empresa.html', context)


@login_required
def perfil_empresa(request):
    """Vista de perfil de la empresa"""
    if not hasattr(request.user, 'empresa'):
        messages.error(request, 'No tienes un perfil de empresa.')
        return redirect('home')
    
    empresa = request.user.empresa
    
    # Estadísticas básicas
    total_practicas = Practica.objects.filter(empresa=empresa).count()
    practicas_activas = Practica.objects.filter(empresa=empresa, activa=True).count()
    
    context = {
        'empresa': empresa,
        'total_practicas': total_practicas,
        'practicas_activas': practicas_activas,
    }
    return render(request, 'inscripciones/perfil_empresa.html', context)


@login_required
def crear_practica_empresa(request):
    """Crear una nueva práctica"""
    if not hasattr(request.user, 'empresa'):
        messages.error(request, 'No tienes un perfil de empresa.')
        return redirect('home')
    
    empresa = request.user.empresa
    
    if request.method == 'POST':
        form = PracticaForm(request.POST)
        if form.is_valid():
            practica = form.save(commit=False)
            practica.empresa = empresa
            # Inicializar cupos_disponibles con el mismo valor que cupos_totales
            practica.cupos_disponibles = practica.cupos_totales
            practica.save()
            messages.success(request, 'Práctica creada exitosamente.')
            return redirect('panel_empresa')
    else:
        form = PracticaForm()
    
    context = {
        'empresa': empresa,
        'form': form,
    }
    return render(request, 'inscripciones/crear_practica.html', context)


@login_required
def editar_practica_empresa(request, pk):
    """Editar una práctica existente"""
    if not hasattr(request.user, 'empresa'):
        messages.error(request, 'No tienes un perfil de empresa.')
        return redirect('home')
    
    empresa = request.user.empresa
    practica = get_object_or_404(Practica, pk=pk, empresa=empresa)
    
    if request.method == 'POST':
        form = PracticaForm(request.POST, instance=practica)
        if form.is_valid():
            practica_actualizada = form.save(commit=False)
            # Ajustar cupos_disponibles si se modificaron los cupos_totales
            if 'cupos_totales' in form.changed_data:
                diferencia = practica_actualizada.cupos_totales - practica.cupos_totales
                practica_actualizada.cupos_disponibles = practica.cupos_disponibles + diferencia
            practica_actualizada.save()
            messages.success(request, 'Práctica actualizada exitosamente.')
            return redirect('mis_practicas_empresa')
    else:
        form = PracticaForm(instance=practica)
    
    context = {
        'empresa': empresa,
        'practica': practica,
        'form': form,
    }
    return render(request, 'inscripciones/editar_practica.html', context)


@login_required
def eliminar_practica_empresa(request, pk):
    """Eliminar una práctica"""
    if not hasattr(request.user, 'empresa'):
        messages.error(request, 'No tienes un perfil de empresa.')
        return redirect('home')
    
    empresa = request.user.empresa
    practica = get_object_or_404(Practica, pk=pk, empresa=empresa)
    
    if request.method == 'POST':
        titulo = practica.titulo
        practica.delete()
        messages.success(request, f'La práctica "{titulo}" ha sido eliminada exitosamente.')
        return redirect('mis_practicas_empresa')
    
    # Si no es POST, redirigir a mis prácticas
    return redirect('mis_practicas_empresa')


@login_required
def postulantes_practica(request, pk):
    """Ver postulantes de una práctica"""
    if not hasattr(request.user, 'empresa'):
        messages.error(request, 'No tienes un perfil de empresa.')
        return redirect('home')
    
    empresa = request.user.empresa
    practica = get_object_or_404(Practica, pk=pk, empresa=empresa)
    inscripciones = Inscripcion.objects.filter(practica=practica).select_related('estudiante__user', 'estudiante__carrera').order_by('-fecha_inscripcion')
    
    # Filtros
    estado = request.GET.get('estado')
    if estado:
        inscripciones = inscripciones.filter(estado=estado)
    
    context = {
        'empresa': empresa,
        'practica': practica,
        'inscripciones': inscripciones,
    }
    return render(request, 'inscripciones/postulantes_practica.html', context)


@login_required
def evaluar_postulante(request, inscripcion_pk):
    """Aprobar o rechazar un postulante y asignar calificaciones"""
    if not hasattr(request.user, 'empresa'):
        messages.error(request, 'No tienes un perfil de empresa.')
        return redirect('home')
    
    empresa = request.user.empresa
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_pk, practica__empresa=empresa)
    
    # Obtener calificaciones existentes
    from .models import Calificacion
    calificaciones_existentes = Calificacion.objects.filter(inscripcion=inscripcion)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        # Procesar calificaciones si se enviaron
        if 'guardar_calificaciones' in request.POST:
            from .forms import CalificacionForm
            form = CalificacionForm(request.POST, quimestres=['Q1'], periodos=['P1', 'P2', 'P3'])
            
            if form.is_valid():
                # Guardar calificaciones
                for field_name, valor in form.cleaned_data.items():
                    if valor:  # Solo guardar si hay un valor
                        # Parsear el nombre del campo: comportamiento_Q1_P1 o proyecto_Q1_P1
                        parts = field_name.split('_')
                        tipo_calificacion = parts[0]  # 'comportamiento' o 'proyecto'
                        quimestre = parts[1]  # 'Q1'
                        periodo = parts[2]  # 'P1', 'P2', 'P3'
                        
                        # Crear o actualizar calificación
                        Calificacion.objects.update_or_create(
                            inscripcion=inscripcion,
                            tipo_calificacion=tipo_calificacion,
                            quimestre=quimestre,
                            periodo=periodo,
                            defaults={
                                'valor': valor,
                                'registrado_por': request.user
                            }
                        )
                
                messages.success(request, 'Calificaciones guardadas exitosamente.')
                return redirect('evaluar_postulante', inscripcion_pk=inscripcion_pk)
        
        # Procesar aprobación/rechazo
        observaciones = request.POST.get('observaciones', '')
        
        if accion == 'aprobar':
            inscripcion.estado = 'aprobada'
            inscripcion.fecha_evaluacion = timezone.now()
            inscripcion.observaciones = observaciones
            inscripcion.save()
            messages.success(request, 'Postulante aprobado exitosamente.')
            return redirect('postulantes_practica', pk=inscripcion.practica.pk)
        elif accion == 'rechazar':
            inscripcion.estado = 'rechazada'
            inscripcion.fecha_evaluacion = timezone.now()
            inscripcion.observaciones = observaciones
            inscripcion.save()
            messages.success(request, 'Postulante rechazado.')
            return redirect('postulantes_practica', pk=inscripcion.practica.pk)
    
    # Preparar datos para el formulario con valores existentes
    from .forms import CalificacionForm
    initial_data = {}
    for calificacion in calificaciones_existentes:
        field_name = f'{calificacion.tipo_calificacion}_{calificacion.quimestre}_{calificacion.periodo}'
        initial_data[field_name] = calificacion.valor
    
    form = CalificacionForm(initial=initial_data, quimestres=['Q1'], periodos=['P1', 'P2', 'P3'])
    
    context = {
        'empresa': empresa,
        'inscripcion': inscripcion,
        'form': form,
        'calificaciones': calificaciones_existentes,
    }
    return render(request, 'inscripciones/evaluar_postulante.html', context)


# ============================================
# VISTAS PARA FACULTADES
# ============================================

@login_required
def panel_facultad(request):
    """Panel de control para facultades"""
    if not hasattr(request.user, 'facultad'):
        messages.error(request, 'No tienes un perfil de facultad.')
        return redirect('home')
    
    facultad = request.user.facultad
    practicas = PracticaInterna.objects.filter(facultad=facultad).order_by('-fecha_publicacion')
    
    # Estadísticas
    total_practicas = practicas.count()
    practicas_activas = practicas.filter(activa=True, estado='disponible').count()
    total_postulaciones = InscripcionInterna.objects.filter(practica_interna__facultad=facultad).count()
    postulaciones_pendientes = InscripcionInterna.objects.filter(practica_interna__facultad=facultad, estado='pendiente').count()
    
    context = {
        'facultad': facultad,
        'practicas': practicas[:5],  # Últimas 5 prácticas
        'total_practicas': total_practicas,
        'practicas_activas': practicas_activas,
        'total_postulaciones': total_postulaciones,
        'postulaciones_pendientes': postulaciones_pendientes,
    }
    return render(request, 'inscripciones/panel_facultad.html', context)


@login_required
def mis_practicas_facultad(request):
    """Lista de todas las prácticas internas de la facultad"""
    if not hasattr(request.user, 'facultad'):
        messages.error(request, 'No tienes un perfil de facultad.')
        return redirect('home')
    
    facultad = request.user.facultad
    practicas = PracticaInterna.objects.filter(facultad=facultad).order_by('-fecha_publicacion')
    
    # Filtros
    estado = request.GET.get('estado')
    if estado:
        practicas = practicas.filter(estado=estado)
    
    paginator = Paginator(practicas, 10)
    page = request.GET.get('page')
    practicas = paginator.get_page(page)
    
    context = {
        'facultad': facultad,
        'practicas': practicas,
    }
    return render(request, 'inscripciones/mis_practicas_facultad.html', context)


@login_required
def perfil_facultad(request):
    """Vista de perfil de la facultad"""
    if not hasattr(request.user, 'facultad'):
        messages.error(request, 'No tienes un perfil de facultad.')
        return redirect('home')
    
    facultad = request.user.facultad
    
    # Estadísticas básicas
    total_practicas = PracticaInterna.objects.filter(facultad=facultad).count()
    practicas_activas = PracticaInterna.objects.filter(facultad=facultad, activa=True).count()
    
    context = {
        'facultad': facultad,
        'total_practicas': total_practicas,
        'practicas_activas': practicas_activas,
    }
    return render(request, 'inscripciones/perfil_facultad.html', context)


@login_required
def crear_practica_facultad(request):
    """Crear una nueva práctica interna"""
    if not hasattr(request.user, 'facultad'):
        messages.error(request, 'No tienes un perfil de facultad.')
        return redirect('home')
    
    facultad = request.user.facultad
    
    if request.method == 'POST':
        form = PracticaInternaForm(request.POST)
        if form.is_valid():
            practica = form.save(commit=False)
            practica.facultad = facultad
            # Inicializar cupos_disponibles con el mismo valor que cupos_totales
            practica.cupos_disponibles = practica.cupos_totales
            practica.save()
            messages.success(request, 'Práctica interna creada exitosamente.')
            return redirect('panel_facultad')
    else:
        form = PracticaInternaForm()
    
    context = {
        'facultad': facultad,
        'form': form,
    }
    return render(request, 'inscripciones/crear_practica_interna.html', context)


@login_required
def editar_practica_facultad(request, pk):
    """Editar una práctica interna existente"""
    if not hasattr(request.user, 'facultad'):
        messages.error(request, 'No tienes un perfil de facultad.')
        return redirect('home')
    
    facultad = request.user.facultad
    practica = get_object_or_404(PracticaInterna, pk=pk, facultad=facultad)
    
    if request.method == 'POST':
        form = PracticaInternaForm(request.POST, instance=practica)
        if form.is_valid():
            practica_actualizada = form.save(commit=False)
            
            # Si cambió cupos_totales, ajustar cupos_disponibles proporcionalmente
            if practica.cupos_totales != practica_actualizada.cupos_totales:
                cupos_ocupados = practica.cupos_totales - practica.cupos_disponibles
                practica_actualizada.cupos_disponibles = max(0, practica_actualizada.cupos_totales - cupos_ocupados)
            
            practica_actualizada.save()
            messages.success(request, 'Práctica interna actualizada exitosamente.')
            return redirect('mis_practicas_facultad')
    else:
        form = PracticaInternaForm(instance=practica)
    
    context = {
        'facultad': facultad,
        'practica': practica,
        'form': form,
    }
    return render(request, 'inscripciones/editar_practica_interna.html', context)


@login_required
def eliminar_practica_facultad(request, pk):
    """Eliminar una práctica interna"""
    if not hasattr(request.user, 'facultad'):
        messages.error(request, 'No tienes un perfil de facultad.')
        return redirect('home')
    
    facultad = request.user.facultad
    practica = get_object_or_404(PracticaInterna, pk=pk, facultad=facultad)
    
    if request.method == 'POST':
        titulo = practica.titulo
        practica.delete()
        messages.success(request, f'La práctica interna "{titulo}" ha sido eliminada exitosamente.')
        return redirect('mis_practicas_facultad')
    
    # Si no es POST, redirigir a mis prácticas
    return redirect('mis_practicas_facultad')


@login_required
def postulantes_practica_interna(request, pk):
    """Ver postulantes de una práctica interna"""
    if not hasattr(request.user, 'facultad'):
        messages.error(request, 'No tienes un perfil de facultad.')
        return redirect('home')
    
    facultad = request.user.facultad
    practica = get_object_or_404(PracticaInterna, pk=pk, facultad=facultad)
    inscripciones = InscripcionInterna.objects.filter(practica_interna=practica).select_related('estudiante__user', 'estudiante__carrera').order_by('-fecha_inscripcion')
    
    # Filtros
    estado = request.GET.get('estado')
    if estado:
        inscripciones = inscripciones.filter(estado=estado)
    
    context = {
        'facultad': facultad,
        'practica': practica,
        'inscripciones': inscripciones,
    }
    return render(request, 'inscripciones/postulantes_practica_interna.html', context)


@login_required
def evaluar_postulante_interno(request, inscripcion_pk):
    """Aprobar o rechazar un postulante interno"""
    if not hasattr(request.user, 'facultad'):
        messages.error(request, 'No tienes un perfil de facultad.')
        return redirect('home')
    
    facultad = request.user.facultad
    inscripcion = get_object_or_404(InscripcionInterna, pk=inscripcion_pk, practica_interna__facultad=facultad)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        observaciones = request.POST.get('observaciones', '')
        
        if accion == 'aprobar':
            inscripcion.estado = 'aprobada'
            inscripcion.fecha_evaluacion = timezone.now()
            inscripcion.observaciones = observaciones
            inscripcion.save()
            messages.success(request, 'Postulante aprobado exitosamente.')
        elif accion == 'rechazar':
            inscripcion.estado = 'rechazada'
            inscripcion.fecha_evaluacion = timezone.now()
            inscripcion.observaciones = observaciones
            inscripcion.save()
            messages.success(request, 'Postulante rechazado.')
        
        return redirect('postulantes_practica_interna', pk=inscripcion.practica_interna.pk)
    
    context = {
        'facultad': facultad,
        'inscripcion': inscripcion,
    }
    return render(request, 'inscripciones/evaluar_postulante_interno.html', context)
