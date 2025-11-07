from django.apps import AppConfig


class InscripcionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inscripciones'
    
    def ready(self):
        """Importar signals cuando la app esté lista"""
        import inscripciones.signals
