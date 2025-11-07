from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Carrera, Estudiante, Empresa, Practica, Inscripcion, DocumentoInscripcion, 
    Facultad, PracticaInterna, InscripcionInterna, Calificacion, DocumentoInscripcionInterna
)


# Personalización del sitio admin
admin.site.site_header = "ULEAM - Sistema de Prácticas Pre Profesionales"
admin.site.site_title = "Administración ULEAM"
admin.site.index_title = "Panel de Administración"


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activa']
    list_filter = ['activa']
    search_fields = ['nombre', 'codigo']
    ordering = ['nombre']
    list_per_page = 20


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['codigo_estudiante', 'get_nombre_completo', 'carrera', 'ciclo_actual', 'activo']
    list_filter = ['carrera', 'ciclo_actual', 'activo']
    search_fields = ['codigo_estudiante', 'user__first_name', 'user__last_name', 'user__email']
    ordering = ['codigo_estudiante']
    readonly_fields = ['fecha_registro']
    list_per_page = 20
    
    def get_nombre_completo(self, obj):
        return obj.user.get_full_name() if obj.user else "Sin usuario"
    get_nombre_completo.short_description = "Nombre Completo"


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ruc', 'sector', 'contacto_responsable', 'estado_aprobacion', 'activa']
    list_filter = ['sector', 'estado_aprobacion', 'activa']
    search_fields = ['nombre', 'ruc', 'contacto_responsable']
    ordering = ['nombre']
    readonly_fields = ['fecha_registro', 'fecha_aprobacion', 'aprobado_por']
    list_per_page = 20
    actions = ['aprobar_empresas', 'rechazar_empresas', 'activar_empresas', 'desactivar_empresas']
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'ruc', 'sector', 'logo')
        }),
        ('Contacto', {
            'fields': ('contacto_responsable', 'email', 'telefono', 'direccion')
        }),
        ('Documentos Legales', {
            'fields': ('documento_constitucion', 'documento_ruc', 'documento_representante'),
            'classes': ('collapse',)
        }),
        ('Estado y Aprobación', {
            'fields': ('estado_aprobacion', 'observaciones_aprobacion', 'fecha_aprobacion', 'aprobado_por', 'activa', 'descripcion', 'fecha_registro'),
            'classes': ('wide',)
        }),
        ('Usuario del Sistema', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )
    
    def aprobar_empresas(self, request, queryset):
        from django.utils import timezone
        count = 0
        for empresa in queryset:
            if empresa.estado_aprobacion != 'aprobada':
                empresa.estado_aprobacion = 'aprobada'
                empresa.fecha_aprobacion = timezone.now()
                empresa.aprobado_por = request.user
                empresa.activa = True
                # Activar el usuario asociado
                if empresa.user:
                    empresa.user.is_active = True
                    empresa.user.save()
                empresa.save()
                count += 1
        self.message_user(request, f"✅ {count} empresa(s) aprobada(s) exitosamente. Los usuarios ahora pueden iniciar sesión.")
    aprobar_empresas.short_description = "✅ Aprobar empresas seleccionadas"
    
    def rechazar_empresas(self, request, queryset):
        from django.utils import timezone
        count = 0
        for empresa in queryset:
            if empresa.estado_aprobacion != 'rechazada':
                empresa.estado_aprobacion = 'rechazada'
                empresa.fecha_aprobacion = timezone.now()
                empresa.aprobado_por = request.user
                empresa.activa = False
                # Desactivar el usuario asociado
                if empresa.user:
                    empresa.user.is_active = False
                    empresa.user.save()
                empresa.save()
                count += 1
        self.message_user(request, f"❌ {count} empresa(s) rechazada(s). Los usuarios no podrán iniciar sesión.")
    rechazar_empresas.short_description = "❌ Rechazar empresas seleccionadas"
    
    def activar_empresas(self, request, queryset):
        queryset.update(activa=True)
        self.message_user(request, f"{queryset.count()} empresa(s) activada(s).")
    activar_empresas.short_description = "Activar empresas seleccionadas"
    
    def desactivar_empresas(self, request, queryset):
        queryset.update(activa=False)
        self.message_user(request, f"{queryset.count()} empresa(s) desactivada(s).")
    desactivar_empresas.short_description = "Desactivar empresas seleccionadas"


@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'empresa', 'dirigido_a', 'estado', 'cupos_disponibles', 'fecha_inicio', 'fecha_limite_inscripcion', 'activa']
    list_filter = ['estado', 'dirigido_a', 'empresa', 'fecha_inicio', 'activa']
    search_fields = ['titulo', 'empresa__nombre', 'descripcion']
    ordering = ['-fecha_publicacion']
    readonly_fields = ['fecha_publicacion']
    date_hierarchy = 'fecha_inicio'
    list_per_page = 20
    actions = ['activar_practicas', 'desactivar_practicas']
    
    def activar_practicas(self, request, queryset):
        queryset.update(activa=True)
        self.message_user(request, f"{queryset.count()} prácticas activadas exitosamente.")
    activar_practicas.short_description = "Activar prácticas seleccionadas"
    
    def desactivar_practicas(self, request, queryset):
        queryset.update(activa=False)
        self.message_user(request, f"{queryset.count()} prácticas desactivadas exitosamente.")
    desactivar_practicas.short_description = "Desactivar prácticas seleccionadas"


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['get_estudiante_nombre', 'practica', 'estado', 'fecha_inscripcion', 'fecha_evaluacion']
    list_filter = ['estado', 'fecha_inscripcion', 'practica__empresa']
    search_fields = ['estudiante__user__first_name', 'estudiante__user__last_name', 'practica__titulo']
    ordering = ['-fecha_inscripcion']
    readonly_fields = ['fecha_inscripcion']
    date_hierarchy = 'fecha_inscripcion'
    list_per_page = 20
    actions = ['aprobar_inscripciones', 'rechazar_inscripciones']
    
    def get_estudiante_nombre(self, obj):
        return obj.estudiante.user.get_full_name()
    get_estudiante_nombre.short_description = "Estudiante"
    
    def aprobar_inscripciones(self, request, queryset):
        queryset.update(estado='aprobada')
        self.message_user(request, f"{queryset.count()} inscripciones aprobadas.")
    aprobar_inscripciones.short_description = "Aprobar inscripciones seleccionadas"
    
    def rechazar_inscripciones(self, request, queryset):
        queryset.update(estado='rechazada')
        self.message_user(request, f"{queryset.count()} inscripciones rechazadas.")
    rechazar_inscripciones.short_description = "Rechazar inscripciones seleccionadas"


@admin.register(DocumentoInscripcion)
class DocumentoInscripcionAdmin(admin.ModelAdmin):
    list_display = ['inscripcion', 'tipo', 'nombre', 'fecha_subida']
    list_filter = ['tipo', 'fecha_subida']
    search_fields = ['nombre', 'inscripcion__estudiante__user__first_name']
    ordering = ['-fecha_subida']
    readonly_fields = ['fecha_subida']


@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'decano', 'contacto_responsable', 'estado_aprobacion', 'activa']
    list_filter = ['estado_aprobacion', 'activa']
    search_fields = ['nombre', 'codigo', 'decano', 'contacto_responsable']
    ordering = ['nombre']
    readonly_fields = ['fecha_registro', 'fecha_aprobacion', 'aprobado_por']
    list_per_page = 20
    actions = ['aprobar_facultades', 'rechazar_facultades', 'activar_facultades', 'desactivar_facultades']
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'decano', 'logo')
        }),
        ('Contacto', {
            'fields': ('contacto_responsable', 'email', 'telefono', 'direccion')
        }),
        ('Documentos Legales', {
            'fields': ('documento_autorizacion', 'documento_representante', 'documento_resolucion'),
            'classes': ('collapse',)
        }),
        ('Estado y Aprobación', {
            'fields': ('estado_aprobacion', 'observaciones_aprobacion', 'fecha_aprobacion', 'aprobado_por', 'activa', 'descripcion', 'fecha_registro'),
            'classes': ('wide',)
        }),
        ('Usuario del Sistema', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )
    
    def aprobar_facultades(self, request, queryset):
        from django.utils import timezone
        count = 0
        for facultad in queryset:
            if facultad.estado_aprobacion != 'aprobada':
                facultad.estado_aprobacion = 'aprobada'
                facultad.fecha_aprobacion = timezone.now()
                facultad.aprobado_por = request.user
                facultad.activa = True
                # Activar el usuario asociado
                if facultad.user:
                    facultad.user.is_active = True
                    facultad.user.save()
                facultad.save()
                count += 1
        self.message_user(request, f"✅ {count} facultad(es) aprobada(s) exitosamente. Los usuarios ahora pueden iniciar sesión.")
    aprobar_facultades.short_description = "✅ Aprobar facultades seleccionadas"
    
    def rechazar_facultades(self, request, queryset):
        from django.utils import timezone
        count = 0
        for facultad in queryset:
            if facultad.estado_aprobacion != 'rechazada':
                facultad.estado_aprobacion = 'rechazada'
                facultad.fecha_aprobacion = timezone.now()
                facultad.aprobado_por = request.user
                facultad.activa = False
                # Desactivar el usuario asociado
                if facultad.user:
                    facultad.user.is_active = False
                    facultad.user.save()
                facultad.save()
                count += 1
        self.message_user(request, f"❌ {count} facultad(es) rechazada(s). Los usuarios no podrán iniciar sesión.")
    rechazar_facultades.short_description = "❌ Rechazar facultades seleccionadas"
    
    def activar_facultades(self, request, queryset):
        queryset.update(activa=True)
        self.message_user(request, f"{queryset.count()} facultad(es) activada(s).")
    activar_facultades.short_description = "Activar facultades seleccionadas"
    
    def desactivar_facultades(self, request, queryset):
        queryset.update(activa=False)
        self.message_user(request, f"{queryset.count()} facultad(es) desactivada(s).")
    desactivar_facultades.short_description = "Desactivar facultades seleccionadas"


@admin.register(PracticaInterna)
class PracticaInternaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'facultad', 'tipo_servicio', 'estado', 'cupos_disponibles', 'fecha_inicio', 'fecha_limite_inscripcion']
    list_filter = ['estado', 'facultad', 'tipo_servicio', 'fecha_inicio', 'activa']
    search_fields = ['titulo', 'facultad__nombre', 'descripcion']
    ordering = ['-fecha_publicacion']
    readonly_fields = ['fecha_publicacion']
    date_hierarchy = 'fecha_inicio'


@admin.register(InscripcionInterna)
class InscripcionInternaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'practica_interna', 'estado', 'fecha_inscripcion', 'fecha_evaluacion']
    list_filter = ['estado', 'fecha_inscripcion', 'practica_interna__facultad']
    search_fields = ['estudiante__user__first_name', 'estudiante__user__last_name', 'practica_interna__titulo']
    ordering = ['-fecha_inscripcion']
    readonly_fields = ['fecha_inscripcion']
    date_hierarchy = 'fecha_inscripcion'


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['get_estudiante', 'get_practica', 'tipo_calificacion', 'quimestre', 'periodo', 'valor', 'fecha_registro']
    list_filter = ['tipo_calificacion', 'quimestre', 'periodo', 'valor', 'fecha_registro']
    search_fields = [
        'inscripcion__estudiante__user__first_name', 
        'inscripcion__estudiante__user__last_name',
        'inscripcion_interna__estudiante__user__first_name',
        'inscripcion_interna__estudiante__user__last_name'
    ]
    ordering = ['-fecha_registro']
    readonly_fields = ['fecha_registro']
    date_hierarchy = 'fecha_registro'
    list_per_page = 20
    
    fieldsets = (
        ('Inscripción', {
            'fields': ('inscripcion', 'inscripcion_interna')
        }),
        ('Calificación', {
            'fields': ('tipo_calificacion', 'quimestre', 'periodo', 'valor')
        }),
        ('Registro', {
            'fields': ('registrado_por', 'fecha_registro'),
            'classes': ('collapse',)
        }),
    )
    
    def get_estudiante(self, obj):
        if obj.inscripcion:
            return obj.inscripcion.estudiante.user.get_full_name()
        elif obj.inscripcion_interna:
            return obj.inscripcion_interna.estudiante.user.get_full_name()
        return "N/A"
    get_estudiante.short_description = "Estudiante"
    
    def get_practica(self, obj):
        if obj.inscripcion:
            return f"{obj.inscripcion.practica.titulo} ({obj.inscripcion.practica.empresa.nombre})"
        elif obj.inscripcion_interna:
            return f"{obj.inscripcion_interna.practica_interna.titulo} ({obj.inscripcion_interna.practica_interna.facultad.nombre})"
        return "N/A"
    get_practica.short_description = "Práctica"


@admin.register(DocumentoInscripcionInterna)
class DocumentoInscripcionInternaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'get_estudiante', 'tipo', 'archivo', 'fecha_subida']
    list_filter = ['tipo', 'fecha_subida']
    search_fields = ['nombre', 'inscripcion_interna__estudiante__user__first_name', 'inscripcion_interna__estudiante__user__last_name']
    ordering = ['-fecha_subida']
    readonly_fields = ['fecha_subida']
    date_hierarchy = 'fecha_subida'
    list_per_page = 20
    
    def get_estudiante(self, obj):
        return obj.inscripcion_interna.estudiante.user.get_full_name()
    get_estudiante.short_description = "Estudiante"
