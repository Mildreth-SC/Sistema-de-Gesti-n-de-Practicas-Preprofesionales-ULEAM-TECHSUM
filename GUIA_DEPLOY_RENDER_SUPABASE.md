# 🚀 Guía de Deploy - Render + Supabase

Esta guía te ayudará a desplegar el Sistema de Gestión de Prácticas Preprofesionales en Render usando Supabase como base de datos.

## 📋 Prerequisitos

1. **Cuenta de Supabase**: https://supabase.com/
2. **Cuenta de Render**: https://render.com/
3. **Cuenta de GitHub** con el repositorio del proyecto

---

## 1️⃣ Configurar Base de Datos en Supabase

### Paso 1: Crear un nuevo proyecto en Supabase

1. Ve a https://app.supabase.com/
2. Haz clic en **"New Project"**
3. Completa la información:
   - **Name**: `sistema-practicas-uleam` (o el nombre que prefieras)
   - **Database Password**: Crea una contraseña segura (¡guárdala!)
   - **Region**: Selecciona la más cercana (ej: `us-east-1`)
4. Haz clic en **"Create new project"**
5. Espera 2-3 minutos mientras se crea el proyecto

### Paso 2: Obtener las credenciales de conexión

1. Ve a **Settings** (⚙️) en el menú lateral
2. Haz clic en **Database**
3. En la sección **Connection string**, selecciona:
   - **Mode**: Transaction (Connection pooling)
   - Copia la cadena de conexión que empieza con `postgresql://`
   
   Ejemplo:
   ```
   postgresql://postgres.xxxxxxxxxxxxx:TU_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true
   ```

4. También necesitarás (para SUPABASE_URL y SUPABASE_KEY):
   - Ve a **Settings** > **API**
   - Copia **Project URL** (ej: `https://xxxxx.supabase.co`)
   - Copia **anon/public** key

---

## 2️⃣ Configurar Render

### Paso 1: Crear un nuevo Web Service

1. Ve a https://dashboard.render.com/
2. Haz clic en **"New +"** > **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura el servicio:
   - **Name**: `sistema-practicas-uleam`
   - **Region**: Selecciona la misma región que Supabase (ej: Oregon)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn sistema_practicas.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan**: `Free`

### Paso 2: Configurar Variables de Entorno

En la sección **Environment**, agrega las siguientes variables:

| Key | Value | Notas |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.10.15` | Versión de Python |
| `SECRET_KEY` | *Auto-generado* | Haz clic en "Generate" |
| `DEBUG` | `False` | Nunca usar True en producción |
| `ALLOWED_HOSTS` | `.onrender.com,localhost` | Hosts permitidos |
| `DATABASE_URL` | `postgresql://postgres.xxxxx:PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true` | ⚠️ Reemplaza con tu cadena de Supabase |
| `SUPABASE_URL` | `https://xxxxx.supabase.co` | URL de tu proyecto Supabase |
| `SUPABASE_KEY` | `eyJhbG...` | Tu anon/public key de Supabase |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` | Para seguridad CSRF |

### Paso 3: Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. Este proceso tomará 5-10 minutos la primera vez

---

## 3️⃣ Verificar el Deployment

### Esperar a que termine el build

En los logs de Render verás algo como:
```
==> Installing dependencies...
==> Collecting static files...
==> Running migrations...
==> Build successful!
==> Starting service...
```

### Acceder a tu aplicación

1. Una vez completado, Render te dará una URL como:
   ```
   https://sistema-practicas-uleam.onrender.com
   ```

2. Visita esa URL - deberías ver la página de inicio de tu aplicación

---

## 4️⃣ Configuración Post-Deploy

### Crear un superusuario

1. Ve a **Shell** en el dashboard de Render
2. Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```

3. Sigue las instrucciones para crear tu usuario admin

### Poblar datos de prueba (Opcional)

En el Shell de Render:
```bash
python manage.py poblar_datos
```

O usa los scripts incluidos:
```bash
python crear_usuarios_empresas_facultades.py
python poblar_datos_prueba.py
```

---

## 5️⃣ Actualizar la Aplicación

### Deployments automáticos

Render está configurado con `autoDeploy: true`, por lo que:
- Cada vez que hagas `git push` a la rama `main`
- Render automáticamente reconstruirá y desplegará tu aplicación

### Deployments manuales

Si desactivaste auto-deploy, puedes desplegar manualmente desde:
- Dashboard de Render > Tu servicio > **"Manual Deploy"** > **"Deploy latest commit"**

---

## 6️⃣ Monitoreo y Mantenimiento

### Ver logs en tiempo real

1. Ve a tu servicio en Render
2. Haz clic en **"Logs"**
3. Verás todos los logs de tu aplicación en tiempo real

### Verificar la base de datos

1. Ve a tu proyecto en Supabase
2. Haz clic en **"Table Editor"**
3. Verás todas las tablas creadas por Django

### Reiniciar el servicio

Si necesitas reiniciar:
1. Dashboard de Render > Tu servicio
2. Haz clic en **"Manual Deploy"** > **"Clear build cache & deploy"**

---

## 🔧 Solución de Problemas

### Error de conexión a la base de datos

- Verifica que el `DATABASE_URL` sea correcto
- Asegúrate de usar el **Transaction pooling** mode (puerto 6543)
- Verifica que la contraseña no tenga caracteres especiales sin escapar

### Error 500 en producción

- Revisa los logs en Render
- Asegúrate de que `DEBUG=False`
- Verifica que todas las variables de entorno estén configuradas

### Static files no se cargan

- Verifica que `collectstatic` se ejecute en `build.sh`
- Asegúrate de que `whitenoise` esté instalado
- Revisa la configuración de `STATIC_ROOT` y `STATIC_URL`

### Migraciones no se aplican

En el Shell de Render:
```bash
python manage.py migrate --run-syncdb
```

---

## 📚 Recursos Adicionales

- **Documentación de Render**: https://render.com/docs
- **Documentación de Supabase**: https://supabase.com/docs
- **Django Deployment Checklist**: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

---

## 🎉 ¡Listo!

Tu aplicación ahora está desplegada en Render con Supabase. Cada cambio que hagas en GitHub se desplegará automáticamente.

**URL de tu aplicación**: `https://[tu-servicio].onrender.com`

**Panel de administración**: `https://[tu-servicio].onrender.com/admin`
