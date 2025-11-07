# 🚀 GUÍA COMPLETA PARA DEPLOY EN RENDER

## 📋 **REQUISITOS PREVIOS**

1. ✅ Tu código debe estar en GitHub
2. ✅ Tener una cuenta en Render.com (gratis)
3. ✅ Tener una base de datos PostgreSQL (Supabase o Render)

---

## 🎯 **PASO 1: PREPARAR TU PROYECTO (YA HECHO)**

Los siguientes archivos YA están configurados en tu proyecto:

- ✅ `build.sh` - Script de construcción
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `runtime.txt` - Versión de Python
- ✅ `settings.py` - Configurado para producción

---

## 📤 **PASO 2: SUBIR TU CÓDIGO A GITHUB**

### 2.1 Inicializar Git (si no lo has hecho)

```bash
git init
git add .
git commit -m "Preparado para deploy en Render"
```

### 2.2 Crear repositorio en GitHub

1. Ve a https://github.com
2. Haz clic en el botón **"New"** (arriba a la derecha)
3. Nombre del repositorio: `sistema-practicas-uleam`
4. **NO** marques "Initialize with README" (ya tienes código)
5. Haz clic en **"Create repository"**

### 2.3 Conectar y subir tu código

GitHub te dará estos comandos (cópialos y ejecútalos):

```bash
git remote add origin https://github.com/TU-USUARIO/sistema-practicas-uleam.git
git branch -M main
git push -u origin main
```

---

## 🌐 **PASO 3: CREAR BASE DE DATOS EN RENDER (OPCIONAL)**

**NOTA:** Si ya tienes Supabase configurado, puedes usar esa base de datos. Si no, crea una nueva en Render:

### 3.1 Crear PostgreSQL Database

1. Ve a https://dashboard.render.com
2. Haz clic en **"New +"** (arriba a la derecha)
3. Selecciona **"PostgreSQL"**
4. Configura:
   - **Name**: `sistema-practicas-db`
   - **Database**: `sistema_practicas`
   - **User**: `uleam_user` (o déjalo automático)
   - **Region**: Selecciona **Oregon (US West)** (gratis)
   - **PostgreSQL Version**: **16** (más reciente)
   - **Plan**: **Free** (0 USD/mes)
5. Haz clic en **"Create Database"**

### 3.2 Copiar la URL de conexión

Una vez creada, verás:
- **Internal Database URL** (úsala si tu app está en Render)
- **External Database URL** (úsala desde fuera de Render)

**COPIA LA "Internal Database URL"** - se ve así:
```
postgresql://user:password@dpg-xxx.oregon-postgres.render.com/database
```

---

## 🚀 **PASO 4: CREAR WEB SERVICE EN RENDER**

### 4.1 Crear nuevo Web Service

1. Ve a https://dashboard.render.com
2. Haz clic en **"New +"**
3. Selecciona **"Web Service"**
4. Conecta tu repositorio de GitHub:
   - Si es la primera vez, haz clic en **"Connect GitHub"**
   - Autoriza a Render para acceder a tus repositorios
   - Busca `sistema-practicas-uleam`
   - Haz clic en **"Connect"**

### 4.2 Configurar el Web Service

**Configuración Básica:**

- **Name**: `sistema-practicas-uleam`
- **Region**: **Oregon (US West)** (mismo que la base de datos)
- **Branch**: `main`
- **Root Directory**: (déjalo en blanco)
- **Runtime**: **Python 3**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn sistema_practicas.wsgi:application`

**Plan:**
- Selecciona **Free** (0 USD/mes)
- ⚠️ **IMPORTANTE**: El plan gratuito hace "spin down" después de 15 minutos de inactividad (la primera carga será lenta)

### 4.3 Variables de Entorno

Haz clic en **"Advanced"** y luego en **"Add Environment Variable"**.

Agrega TODAS estas variables (una por una):

#### Variables REQUERIDAS:

```plaintext
SECRET_KEY
tu-clave-secreta-super-segura-cambiala-ahora-12345

DEBUG
False

ALLOWED_HOSTS
.onrender.com,sistema-practicas-uleam.onrender.com

DATABASE_URL
[PEGA LA URL QUE COPIASTE EN EL PASO 3.2]

CSRF_TRUSTED_ORIGINS
https://sistema-practicas-uleam.onrender.com

SITE_URL
https://sistema-practicas-uleam.onrender.com
```

#### Variables de Supabase (si las usas):

```plaintext
SUPABASE_URL
https://tu-proyecto.supabase.co

SUPABASE_KEY
tu-anon-key

SUPABASE_SERVICE_ROLE_KEY
tu-service-role-key
```

#### Variables de Email (opcional, para enviar correos):

```plaintext
EMAIL_BACKEND
django.core.mail.backends.smtp.EmailBackend

EMAIL_HOST
smtp.gmail.com

EMAIL_PORT
587

EMAIL_USE_TLS
True

EMAIL_HOST_USER
tu-email@gmail.com

EMAIL_HOST_PASSWORD
tu-contraseña-de-aplicacion

DEFAULT_FROM_EMAIL
noreply@sistema-practicas.com
```

### 4.4 Crear el Web Service

1. Revisa que todo esté correcto
2. Haz clic en **"Create Web Service"**
3. Render comenzará a construir tu aplicación (toma 5-10 minutos)

---

## ⏳ **PASO 5: ESPERAR A QUE TERMINE EL DEPLOY**

### 5.1 Observar el proceso de construcción

En la pestaña **"Logs"** verás:

```
==> Building...
🚀 Iniciando proceso de construcción...
📦 Instalando dependencias de Python...
...
🗄️ Recolectando archivos estáticos...
...
🔄 Aplicando migraciones de base de datos...
...
✅ Construcción completada exitosamente!

==> Deploying...
==> Your service is live 🎉
```

### 5.2 Acceder a tu aplicación

Una vez completado, verás el mensaje: **"Your service is live 🎉"**

Tu URL será: `https://sistema-practicas-uleam.onrender.com`

---

## 👤 **PASO 6: CREAR SUPERUSUARIO**

### 6.1 Abrir Shell en Render

1. En el dashboard de Render, ve a tu Web Service
2. En el menú superior, haz clic en **"Shell"**
3. Se abrirá una terminal en tu servidor

### 6.2 Crear superusuario

En la terminal de Render, ejecuta:

```bash
python manage.py createsuperuser
```

Ingresa:
- **Username**: admin
- **Email**: admin@uleam.edu.ec
- **Password**: (tu contraseña segura)
- **Password (again)**: (repite la contraseña)

### 6.3 Acceder al admin

Ve a: `https://sistema-practicas-uleam.onrender.com/admin/`

---

## 📁 **PASO 7: CONFIGURAR ARCHIVOS MEDIA (SUBIDA DE ARCHIVOS)**

### 7.1 Problema con el plan gratuito

⚠️ **IMPORTANTE**: El plan gratuito de Render **NO persiste archivos subidos**. Cuando el servidor se reinicia, los archivos se pierden.

### 7.2 Soluciones:

#### Opción A: Usar Cloudinary (Recomendado - Gratis)

1. Crea cuenta en https://cloudinary.com (plan gratuito)
2. Instala la librería:
   ```bash
   pip install cloudinary django-cloudinary-storage
   ```
3. Configura en `settings.py`:
   ```python
   CLOUDINARY_STORAGE = {
       'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
       'API_KEY': config('CLOUDINARY_API_KEY'),
       'API_SECRET': config('CLOUDINARY_API_SECRET'),
   }
   DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
   ```

#### Opción B: Usar Supabase Storage

Ya tienes Supabase configurado, puedes usar Supabase Storage para los archivos media.

#### Opción C: Upgrade a plan de pago

El plan **Starter ($7/mes)** incluye almacenamiento persistente.

---

## 🔄 **PASO 8: ACTUALIZACIONES FUTURAS**

### 8.1 Hacer cambios en tu código

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

### 8.2 Deploy automático

Render detectará el push y automáticamente:
1. Descargará el nuevo código
2. Ejecutará `build.sh`
3. Reiniciará el servidor

---

## ✅ **PASO 9: VERIFICAR QUE TODO FUNCIONA**

### 9.1 Checklist:

- [ ] La página principal carga: `https://sistema-practicas-uleam.onrender.com/`
- [ ] Puedes acceder al admin: `https://sistema-practicas-uleam.onrender.com/admin/`
- [ ] Los archivos estáticos se cargan (CSS, JS, imágenes)
- [ ] Puedes registrar un estudiante
- [ ] Puedes registrar una empresa
- [ ] Las empresas aprobadas pueden crear prácticas
- [ ] Los estudiantes pueden inscribirse

### 9.2 Si algo falla:

1. Ve a la pestaña **"Logs"** en Render
2. Busca el error (generalmente aparece en rojo)
3. Los errores más comunes:
   - **Error de base de datos**: Verifica `DATABASE_URL`
   - **Error 500**: Verifica `SECRET_KEY` y `DEBUG=False`
   - **CSS no se carga**: Ejecuta `python manage.py collectstatic` en el Shell

---

## 🎉 **¡LISTO!**

Tu sistema de prácticas está ONLINE en:
`https://sistema-practicas-uleam.onrender.com`

### 📊 Recursos Útiles:

- **Dashboard de Render**: https://dashboard.render.com
- **Documentación de Render**: https://render.com/docs
- **Logs en tiempo real**: En tu Web Service > Logs
- **Shell (terminal)**: En tu Web Service > Shell

### ⚠️ Limitaciones del Plan Gratuito:

1. El servicio se "duerme" después de 15 minutos sin actividad
2. La primera carga después de dormir toma ~1 minuto
3. No persiste archivos subidos (usa Cloudinary)
4. 750 horas/mes de servicio (suficiente para un proyecto)

### 💰 Plan de Pago (Opcional):

Si necesitas:
- Servicio 24/7 sin "spin down"
- Almacenamiento persistente
- Más recursos (CPU, RAM)

Considera el plan **Starter ($7/mes)**.

---

## 🆘 SOPORTE

Si algo no funciona:
1. Revisa los **Logs** en Render
2. Verifica todas las **Variables de Entorno**
3. Asegúrate que `DATABASE_URL` sea correcta
4. Verifica que `ALLOWED_HOSTS` incluya tu dominio de Render

¡Tu aplicación está lista para el mundo! 🌍🚀
