# 🎓 Sistema de Gestión de Prácticas Preprofesionales - ULEAM

[![Django Version](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue.svg)](https://supabase.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Render-purple.svg)](https://render.com/)

Sistema web completo para gestionar las prácticas preprofesionales de estudiantes y egresados en la Universidad Laica Eloy Alfaro de Manabí (ULEAM). Desarrollado con Django 5.2.7, PostgreSQL (Supabase) y OpenAI.

---

## ✨ Características Principales

### 👥 Gestión Multi-Usuario
- ✅ **Estudiantes Activos**: Registro con ciclo académico
- ✅ **Egresados**: Registro con tipo de título (Licenciatura/Ingeniería)
- ✅ **Empresas**: Registro con aprobación administrativa
- ✅ **Facultades**: Gestión de prácticas internas
- ✅ **Administradores**: Panel completo de gestión

### 📋 Gestión de Prácticas
- ✅ **Prácticas Externas**: Empresas publican oportunidades
- ✅ **Prácticas Internas**: Facultades ofrecen proyectos de vinculación
- ✅ **CRUD Completo**: Crear, Leer, Actualizar, Eliminar
- ✅ **Filtros Avanzados**: Por área, modalidad, empresa, sector, fecha
- ✅ **43 Carreras de ULEAM**: Todas las facultades representadas

### 🎯 Sistema de Postulaciones
- ✅ **Inscripciones**: Estudiantes/egresados se postulan
- ✅ **Validaciones**: Compatibilidad usuario-práctica
- ✅ **Estados**: Pendiente, Aprobada, Rechazada, Cancelada
- ✅ **Gestión de Documentos**: Carga de PDFs
- ✅ **Evaluación**: Empresas/facultades evalúan postulantes

### 📊 Panel de Administración
- ✅ **Django Admin**: Gestión completa de modelos
- ✅ **Panel Empresa**: Gestión de prácticas y postulantes
- ✅ **Panel Facultad**: Gestión de prácticas internas
- ✅ **Sistema de Calificaciones**: Seguimiento de desempeño
- ✅ **Notificaciones**: Alertas en tiempo real

### 🤖 Chatbot Inteligente (IA)
- ✅ **OpenAI GPT-4**: Respuestas inteligentes
- ✅ **Búsqueda de Prácticas**: Asistencia personalizada
- ✅ **Fallback**: Respuestas predefinidas sin API key

---

## 🛠️ Stack Tecnológico

### Backend
- **Django 5.2.7** - Framework web de Python
- **PostgreSQL** - Base de datos (Supabase)
- **Gunicorn** - Servidor WSGI para producción
- **WhiteNoise** - Servir archivos estáticos

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **Bootstrap 5.3** - Framework CSS responsivo
- **JavaScript** - Interactividad del cliente
- **Django Crispy Forms** - Formularios elegantes

### Integración y Deploy
- **Supabase** - Base de datos PostgreSQL en la nube
- **OpenAI API** - Chatbot inteligente
- **Render.com** - Plataforma de despliegue
- **GitHub** - Control de versiones

---

## 📋 Requerimientos del Sistema

### Software
- Python 3.11+
- PostgreSQL 14+ (o Supabase)
- Git 2.0+

### Dependencias Python (ver `requirements.txt`)
```txt
Django==5.2.7
django-crispy-forms==2.3
crispy-bootstrap5==2024.10
Pillow==10.4.0
psycopg2-binary==2.9.10
supabase==2.11.0
python-decouple==3.8
gunicorn==22.0.0
whitenoise==6.7.0
dj-database-url==3.0.1
openai==1.54.5
```

---

## � Instalación y Configuración

### 1. Clonar el Repositorio

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JuanMoranULEAM/Sistema-de-Gesti-n-de-Practicas-Preprofesionales-ULEAM---TEHCSUM.git
cd Sistema-de-Gesti-n-de-Practicas-Preprofesionales-ULEAM---TEHCSUM
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Django
SECRET_KEY=tu-clave-secreta-django
DEBUG=True

# Base de Datos (Supabase)
DATABASE_URL=postgresql://usuario:password@host:puerto/dbname?pgbouncer=true
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-supabase-anon-key

# OpenAI (Opcional - Chatbot)
OPENAI_API_KEY=tu-openai-api-key

# Email (Opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 6. Poblar Carreras de ULEAM

```bash
python poblar_carreras_uleam.py
```

Este script poblará la base de datos con **43 carreras** de todas las facultades de ULEAM.

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 8. (Opcional) Poblar Datos de Prueba

```bash
python poblar_datos_prueba.py
```

### 9. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

Abre tu navegador en: `http://127.0.0.1:8000/`

---

## 🌐 Despliegue en Producción (Render.com)

### Opción A: Despliegue Rápido (15 minutos)

Ver guía completa en: **[DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md)**

```bash
# 1. Verificar que todo esté listo
python verificar_pre_deploy.py

# 2. Subir a GitHub
git add .
git commit -m "Listo para producción"
git push origin main

# 3. Ir a Render.com y crear Web Service
# 4. Configurar variables de entorno
# 5. ¡Deploy automático!
```

### Opción B: Guía Detallada

Ver documentación completa en:
- **[DESPLIEGUE_RENDER.md](DESPLIEGUE_RENDER.md)** - Guía paso a paso con troubleshooting
- **[VARIABLES_ENTORNO_RENDER.md](VARIABLES_ENTORNO_RENDER.md)** - Explicación de variables
- **[CHECKLIST_DEPLOY.txt](CHECKLIST_DEPLOY.txt)** - Checklist imprimible

---

## 📂 Estructura del Proyecto
├── manage.py                  # Script de gestión de Django
├── requirements.txt           # Dependencias del proyecto
├── build.sh                   # Script de build para Render
├── render.yaml                # Configuración de Render
└── .env.example               # Ejemplo de variables de entorno
```

## 🚀 Instalación y Configuración

### Prerequisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git
- Cuenta de Supabase (para producción)
- Cuenta de Render (para deployment)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JuanMoranULEAM/Sistema-de-Gesti-n-de-Practicas-Preprofesionales-ULEAM---TEHCSUM.git
cd Sistema-de-Gesti-n-de-Practicas-Preprofesionales-ULEAM---TEHCSUM
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

### 4. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env` y completa las variables:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:
```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
DATABASE_URL=postgresql://...  # Para usar Supabase
# O déjalo vacío para usar SQLite en desarrollo local
```

### 5. Configurar Base de Datos

```bash
python manage.py migrate
```

### 6. Cargar Datos Iniciales (Opcional)

```bash
python manage.py loaddata inscripciones/fixtures/carreras.json
```

O usar los scripts de población:
```bash
python crear_usuarios_empresas_facultades.py
python poblar_datos_prueba.py
```

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 8. Ejecutar Servidor de Desarrollo

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
- ✅ Perfil personal editable
- ✅ Búsqueda avanzada de prácticas con filtros
- ✅ Inscripción a prácticas externas e internas
- ✅ Seguimiento de inscripciones
- ✅ Gestión completa de documentos
- ✅ Vista detallada de inscripciones
- ✅ Subida múltiple de documentos
- ✅ Cancelación de inscripciones pendientes
- ✅ Filtrado de inscripciones por estado

### Para Empresas
- ✅ Registro y perfil de empresa
- ✅ Publicación de ofertas de prácticas
- ✅ Gestión de prácticas publicadas
- ✅ Evaluación de postulantes
- ✅ Sistema de calificación
- ✅ Visualización de documentos de postulantes

### Para Facultades
- ✅ Gestión de prácticas internas
- ✅ Publicación de oportunidades internas
- ✅ Evaluación de estudiantes
- ✅ Seguimiento de inscripciones internas

### Para Administradores
- ✅ Gestión completa de carreras
- ✅ Gestión de empresas y facultades
- ✅ Supervisión de todas las prácticas
- ✅ Panel de administración completo
- ✅ Gestión de documentos
- ✅ Reportes y estadísticas

## 🌐 URLs Principales

### Estudiantes
- `/` - Página principal
- `/practicas/` - Lista de prácticas externas
- `/practicas/<id>/` - Detalle de práctica externa
- `/practicas-internas/` - Lista de prácticas internas
- `/practicas-internas/<id>/` - Detalle de práctica interna
- `/empresas/` - Lista de empresas
- `/empresas/<id>/` - Detalle de empresa
- `/registro/` - Registro de estudiante
- `/login/` - Inicio de sesión
- `/perfil/` - Perfil del estudiante
- `/mis-inscripciones/` - Inscripciones del estudiante

### Empresas
- `/registro-empresa/` - Registro de empresa
- `/panel-empresa/` - Panel de gestión de empresa
- `/perfil-empresa/` - Perfil de empresa
- `/crear-practica/` - Crear nueva oferta de práctica
- `/mis-practicas-empresa/` - Prácticas publicadas

### Facultades
- `/registro-facultad/` - Registro de facultad
- `/panel-facultad/` - Panel de gestión de facultad
- `/perfil-facultad/` - Perfil de facultad
- `/crear-practica-interna/` - Crear práctica interna
- `/mis-practicas-facultad/` - Prácticas internas publicadas

### Administración
- `/admin/` - Panel de administración de Django

## 📦 Deployment en Producción

### Render + Supabase

El proyecto está configurado para desplegarse en **Render.com** usando **Supabase** como base de datos PostgreSQL.

**Guía completa de deployment**: Ver [GUIA_DEPLOY_RENDER_SUPABASE.md](GUIA_DEPLOY_RENDER_SUPABASE.md)

**Pasos resumidos:**

1. **Crear proyecto en Supabase** y obtener credenciales
2. **Configurar Render** con el repositorio de GitHub
3. **Agregar variables de entorno** en Render:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
4. **Desplegar** automáticamente con cada push a `main`

### Variables de Entorno para Producción

```env
SECRET_KEY=tu-clave-secreta-generada
DEBUG=False
ALLOWED_HOSTS=.onrender.com,tu-dominio.com
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[PASSWORD]@[HOST]:6543/postgres?pgbouncer=true
SUPABASE_URL=https://[PROJECT-REF].supabase.co
SUPABASE_KEY=[ANON-KEY]
CSRF_TRUSTED_ORIGINS=https://*.onrender.com,https://tu-dominio.com
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto fue desarrollado para la Universidad Laica Eloy Alfaro de Manabí (ULEAM).

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema, contactar al equipo de desarrollo.

## 🔄 Changelog

### v2.0.0 (2024-11)
- ✅ Migración a Render + Supabase
- ✅ Limpieza de código y archivos obsoletos
- ✅ Eliminación de configuraciones de Vercel
- ✅ Documentación actualizada
- ✅ Configuración optimizada para producción

### v1.0.0 (2024-10)
- ✅ Versión inicial del sistema
- ✅ Gestión de prácticas externas e internas
- ✅ Sistema de inscripciones completo
- ✅ Evaluación de postulantes
- ✅ Interfaz responsive con Bootstrap 5
- ✅ Panel de administración configurado

## 📚 Documentación Adicional

- [Guía de Deployment en Render](GUIA_DEPLOY_RENDER_SUPABASE.md)
- [Ejemplo de Variables de Entorno](.env.example)

---

**Desarrollado para ULEAM - Universidad Laica Eloy Alfaro de Manabí**
