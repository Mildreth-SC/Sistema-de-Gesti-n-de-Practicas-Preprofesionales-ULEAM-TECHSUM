from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.home, name='home'),
    path('practicas/', views.lista_practicas, name='lista_practicas'),
    path('practicas-internas/', views.lista_practicas_internas, name='lista_practicas_internas'),
    path('practicas/<int:pk>/', views.detalle_practica, name='detalle_practica'),
    path('practicas-internas/<int:pk>/', views.detalle_practica_interna, name='detalle_practica_interna'),
    path('empresas/', views.lista_empresas, name='lista_empresas'),
    path('empresas/<int:pk>/', views.detalle_empresa, name='detalle_empresa'),
    
    # Autenticación
    path('registro/', views.registro_estudiante, name='registro_estudiante'),
    path('registro-empresa/', views.registro_empresa, name='registro_empresa'),
    path('registro-facultad/', views.registro_facultad, name='registro_facultad'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Perfiles
    path('perfil/', views.perfil_estudiante, name='perfil_estudiante'),
    path('empresa/perfil/', views.perfil_empresa, name='perfil_empresa'),
    path('facultad/perfil/', views.perfil_facultad, name='perfil_facultad'),
    
    # Inscripciones
    path('inscribirse/<int:pk>/', views.inscribirse_practica, name='inscribirse_practica'),
    path('inscribirse-interna/<int:pk>/', views.inscribirse_practica_interna, name='inscribirse_practica_interna'),
    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),
    path('inscripcion/<int:pk>/', views.detalle_inscripcion, name='detalle_inscripcion'),
    path('cancelar-inscripcion/<int:pk>/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    path('cancelar-inscripcion-interna/<int:pk>/', views.cancelar_inscripcion_interna, name='cancelar_inscripcion_interna'),
    
    # Gestión de documentos
    path('inscripcion/<int:inscripcion_pk>/documentos/', views.gestionar_documentos, name='gestionar_documentos'),
    path('documento/<int:documento_pk>/eliminar/', views.eliminar_documento, name='eliminar_documento'),
    
    # Panel de Empresa
    path('empresa/panel/', views.panel_empresa, name='panel_empresa'),
    path('empresa/practicas/', views.mis_practicas_empresa, name='mis_practicas_empresa'),
    path('empresa/practicas/crear/', views.crear_practica_empresa, name='crear_practica_empresa'),
    path('empresa/practicas/<int:pk>/editar/', views.editar_practica_empresa, name='editar_practica_empresa'),
    path('empresa/practicas/<int:pk>/eliminar/', views.eliminar_practica_empresa, name='eliminar_practica_empresa'),
    path('empresa/practicas/<int:pk>/postulantes/', views.postulantes_practica, name='postulantes_practica'),
    path('empresa/inscripcion/<int:inscripcion_pk>/evaluar/', views.evaluar_postulante, name='evaluar_postulante'),
    
    # Panel de Facultad
    path('facultad/panel/', views.panel_facultad, name='panel_facultad'),
    path('facultad/practicas/', views.mis_practicas_facultad, name='mis_practicas_facultad'),
    path('facultad/practicas/crear/', views.crear_practica_facultad, name='crear_practica_facultad'),
    path('facultad/practicas/<int:pk>/editar/', views.editar_practica_facultad, name='editar_practica_facultad'),
    path('facultad/practicas/<int:pk>/eliminar/', views.eliminar_practica_facultad, name='eliminar_practica_facultad'),
    path('facultad/practicas/<int:pk>/postulantes/', views.postulantes_practica_interna, name='postulantes_practica_interna'),
    path('facultad/inscripcion/<int:inscripcion_pk>/evaluar/', views.evaluar_postulante_interno, name='evaluar_postulante_interno'),
]
