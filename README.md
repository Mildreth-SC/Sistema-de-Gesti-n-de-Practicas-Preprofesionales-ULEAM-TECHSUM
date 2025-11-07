# Sistema de Inscripción para Prácticas Pre Profesionales

Un sistema web desarrollado con Django para gestionar las inscripciones de estudiantes universitarios a prácticas pre profesionales.

## Características Principales

- **Gestión de Estudiantes**: Registro y perfil de estudiantes universitarios
- **Gestión de Empresas**: Registro y administración de empresas participantes
- **Gestión de Prácticas**: Publicación y administración de oportunidades de práctica
- **Sistema de Inscripciones**: Proceso completo de inscripción de estudiantes
- **Panel de Administración**: Interfaz administrativa completa
- **Interfaz Responsiva**: Diseño moderno con Bootstrap 5

## Tecnologías Utilizadas

- **Backend**: Django 5.2.7
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Base de Datos**: SQLite (desarrollo)
- **Formularios**: Django Crispy Forms con Bootstrap 5

## Estructura del Proyecto

```
practicas_universidad/
├── sistema_practicas/          # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── inscripciones/              # Aplicación principal
│   ├── models.py              # Modelos de datos
│   ├── views.py               # Vistas del sistema
│   ├── forms.py               # Formularios
│   ├── urls.py                # URLs de la aplicación
│   ├── admin.py               # Configuración del admin
│   └── fixtures/              # Datos iniciales
├── templates/                 # Templates HTML
│   └── inscripciones/
├── static/                    # Archivos estáticos
├── media/                     # Archivos multimedia
├── manage.py                  # Script de gestión de Django
└── requirements.txt           # Dependencias del proyecto
```

## Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd practicas_universidad
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Cargar Datos Iniciales

```bash
python manage.py loaddata inscripciones/fixtures/carreras.json
```

### 6. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

El sistema estará disponible en: http://127.0.0.1:8000/

## Modelos de Datos

### Carrera
- Información de las carreras universitarias
- Campos: nombre, código, descripción, estado activo

### Estudiante
- Perfil extendido del usuario Django
- Campos: código estudiante, carrera, ciclo actual, contacto, foto

### Empresa
- Información de empresas participantes
- Campos: nombre, RUC, dirección, contacto, sector, logo

### Práctica
- Oportunidades de práctica profesional
- Campos: título, descripción, requisitos, duración, cupos, fechas

### Inscripción
- Relación entre estudiantes y prácticas
- Campos: estado, observaciones, fechas de evaluación

### DocumentoInscripcion
- Documentos adjuntos a las inscripciones
- Campos: tipo, nombre, archivo

## Funcionalidades del Sistema

### Para Estudiantes
- ✅ Registro de cuenta
- ✅ Perfil personal editizable
- ✅ Búsqueda avanzada de prácticas con filtros
- ✅ Inscripción a prácticas
- ✅ Seguimiento de inscripciones
- ✅ **Gestión completa de documentos** (NUEVO)
- ✅ **Vista detallada de inscripciones** (NUEVO)
- ✅ **Subida múltiple de documentos** (NUEVO)
- ✅ **Cancelación de inscripciones pendientes**
- ✅ Filtrado de inscripciones por estado

### Para Administradores
- ✅ Gestión completa de carreras
- ✅ Gestión de empresas
- ✅ Publicación de prácticas
- ✅ Evaluación de inscripciones
- ✅ Panel de administración completo
- ✅ Gestión de documentos de inscripciones
- ✅ Reportes y estadísticas

## URLs Principales

- `/` - Página principal
- `/practicas/` - Lista de prácticas
- `/practicas/<id>/` - Detalle de práctica
- `/empresas/` - Lista de empresas
- `/empresas/<id>/` - Detalle de empresa
- `/registro/` - Registro de estudiante
- `/login/` - Inicio de sesión
- `/perfil/` - Perfil del estudiante
- `/mis-inscripciones/` - Inscripciones del estudiante
- `/admin/` - Panel de administración

## Configuración de Producción

### Variables de Entorno
Crear archivo `.env` con:
```
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com
DATABASE_URL=postgresql://usuario:password@host:puerto/db
```

### Base de Datos
Para producción, cambiar a PostgreSQL en `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_db',
        'USER': 'usuario',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Contribución

1. Fork el proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o consultas, contactar a:
- Email: soporte@sistema-practicas.com
- Documentación: [Wiki del Proyecto](link-a-wiki)

## Changelog

### v1.0.0 (2024-10-25)
- Versión inicial del sistema
- Funcionalidades básicas implementadas
- Interfaz responsive con Bootstrap 5
- Sistema de autenticación completo
- Panel de administración configurado
