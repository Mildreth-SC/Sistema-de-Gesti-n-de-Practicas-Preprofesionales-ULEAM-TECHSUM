from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Carrera, Estudiante, Empresa, Practica, Inscripcion, DocumentoInscripcion, Facultad, PracticaInterna, InscripcionInterna, Calificacion


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
    list_display = ['nombre', 'ruc', 'sector', 'contacto_responsable', 'activa']
    list_filter = ['sector', 'activa']
    search_fields = ['nombre', 'ruc', 'contacto_responsable']
    ordering = ['nombre']
    readonly_fields = ['fecha_registro']
    list_per_page = 20
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'ruc', 'sector', 'logo')
        }),
        ('Contacto', {
            'fields': ('contacto_responsable', 'email', 'telefono', 'direccion')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'activa', 'fecha_registro')
        }),
        ('Usuario del Sistema', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'empresa', 'estado', 'cupos_disponibles', 'fecha_inicio', 'fecha_limite_inscripcion', 'activa']
    list_filter = ['estado', 'empresa', 'fecha_inicio', 'activa']
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
    list_display = ['nombre', 'codigo', 'decano', 'contacto_responsable', 'activa']
    list_filter = ['activa']
    search_fields = ['nombre', 'codigo', 'decano', 'contacto_responsable']
    ordering = ['nombre']
    readonly_fields = ['fecha_registro']
    list_per_page = 20
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'decano', 'logo')
        }),
        ('Contacto', {
            'fields': ('contacto_responsable', 'email', 'telefono', 'direccion')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'activa', 'fecha_registro')
        }),
        ('Usuario del Sistema', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )


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
