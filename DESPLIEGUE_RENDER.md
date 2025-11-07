# 🚀 GUÍA DE DESPLIEGUE EN RENDER

## ✅ CHECKLIST PRE-DESPLIEGUE

Antes de desplegar, asegúrate de tener:

- [x] **Cuenta en Render.com** (gratis): https://render.com
- [x] **Repositorio GitHub** actualizado con todos los cambios
- [x] **Base de datos Supabase** configurada y accesible
- [x] **Variables de entorno** preparadas
- [x] **43 Carreras de ULEAM** en script `poblar_carreras_uleam.py`

---

## 📋 PASO 1: PREPARAR REPOSITORIO GITHUB

### 1.1 Verificar archivos importantes

Asegúrate de que estos archivos estén en el repositorio:

```
✅ build.sh                    # Script de construcción
✅ requirements.txt            # Dependencias Python
✅ render.yaml                 # Configuración Render
✅ poblar_carreras_uleam.py   # Script de carreras
✅ runtime.txt                 # Versión de Python (opcional)
✅ .gitignore                  # Excluir archivos sensibles
```

### 1.2 Asegúrate de que .gitignore excluya:

```gitignore
# No subir al repositorio
.env
*.pyc
__pycache__/
db.sqlite3
staticfiles/
media/
.vscode/
*.log
```

### 1.3 Hacer commit y push

```bash
git add .
git commit -m "Preparado para producción en Render"
git push origin main
```

---

## 🌐 PASO 2: CREAR WEB SERVICE EN RENDER

### 2.1 Ir a Render Dashboard
1. Ve a: https://dashboard.render.com
2. Click en **"New +"** → **"Web Service"**

### 2.2 Conectar Repositorio
1. Selecciona tu repositorio de GitHub
2. Si no aparece, click en **"Configure account"** y autoriza Render

### 2.3 Configuración Básica

| Campo | Valor |
|-------|-------|
| **Name** | `sistema-practicas-uleam` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `bash build.sh` |
| **Start Command** | `gunicorn sistema_practicas.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120` |

### 2.4 Plan
- Selecciona **"Free"** (¡Gratis!)
- ⚠️ Se apaga después de 15 minutos de inactividad
- ⚠️ Tarda ~50 segundos en arrancar de nuevo

---

## 🔑 PASO 3: CONFIGURAR VARIABLES DE ENTORNO

En **Environment Variables**, agrega:

### Variables Obligatorias:

```env
# Django Core
SECRET_KEY=auto-generated-by-render
DEBUG=False
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://*.onrender.com

# Base de Datos Supabase
DATABASE_URL=postgresql://postgres.owrgthzfdlnhkiwzdgbd:Milxi26.@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true

# Supabase Auth
SUPABASE_URL=https://owrgthzfdlnhkiwzdgbd.supabase.co
SUPABASE_KEY=tu_supabase_anon_key
```

### Variables Opcionales (pero recomendadas):

```env
# OpenAI API para Chatbot (IMPORTANTE)
OPENAI_API_KEY=tu_api_key_de_openai

# Email (Opcional - Console en desarrollo)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@uleam.edu.ec

# Python Version
PYTHON_VERSION=3.11.0
```

### ⚠️ IMPORTANTE: Obtener SUPABASE_KEY

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd
2. Settings → API
3. Copia **"anon/public"** key
4. Pégala en `SUPABASE_KEY`

### ⚠️ IMPORTANTE: Obtener OPENAI_API_KEY

1. Ve a: https://platform.openai.com/api-keys
2. Crea una nueva API Key
3. Cópiala inmediatamente (solo se muestra una vez)
4. Pégala en `OPENAI_API_KEY`

---

## 🛠️ PASO 4: DEPLOY

### 4.1 Iniciar Deployment
1. Click en **"Create Web Service"**
2. Render empezará a construir tu app automáticamente

### 4.2 Monitorear el Build

Verás logs en tiempo real:

```bash
🚀 Iniciando build para producción...
📦 Actualizando pip...
📚 Instalando dependencias...
🎨 Recolectando archivos estáticos...
🗄️ Ejecutando migraciones...
🎓 Verificando carreras de ULEAM...
✅ Build completado exitosamente!
```

### 4.3 Tiempo Estimado
- **Primera vez:** 5-8 minutos
- **Subsecuentes:** 3-5 minutos

---

## ✅ PASO 5: VERIFICACIÓN POST-DESPLIEGUE

### 5.1 Verificar que la App esté Viva

Tu URL será algo como:
```
https://sistema-practicas-uleam.onrender.com
```

**Checks:**
- ✅ Página de inicio carga correctamente
- ✅ CSS y assets estáticos se ven bien
- ✅ Login funciona
- ✅ Registro funciona

### 5.2 Crear Superusuario

**IMPORTANTE:** Necesitas crear un superusuario para acceder al admin.

En Render, ve a:
1. **Dashboard** → Tu servicio
2. **Shell** → Click en **"Shell"**
3. Ejecuta:

```bash
python manage.py createsuperuser
```

Completa:
- **Username:** `admin`
- **Email:** `admin@uleam.edu.ec`
- **Password:** `[TU_CONTRASEÑA_SEGURA]`

### 5.3 Verificar Admin Panel

1. Ve a: `https://tu-app.onrender.com/admin/`
2. Login con el superusuario
3. Verifica:
   - ✅ 43 Carreras de ULEAM pobladas
   - ✅ Modelos visibles (Estudiantes, Empresas, Facultades, Prácticas)

### 5.4 Poblar Datos de Prueba (Opcional)

Si quieres datos de ejemplo:

```bash
# En el Shell de Render
python poblar_datos_prueba.py
```

Esto creará:
- 3 Facultades de ejemplo
- 5 Estudiantes de prueba
- 3 Empresas de prueba
- 10 Prácticas de ejemplo

---

## 🔧 CONFIGURACIÓN ADICIONAL

### Actualizar ALLOWED_HOSTS en Supabase (si tienes problemas CORS)

1. Ve a Supabase Dashboard
2. **Settings** → **API**
3. En **CORS Settings**, agrega:
   ```
   https://tu-app.onrender.com
   ```

### Configurar Email Real (Producción)

Si quieres enviar emails reales:

1. **Opción 1: Gmail (Desarrollo)**
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=tu_email@gmail.com
   EMAIL_HOST_PASSWORD=tu_app_password
   ```

2. **Opción 2: SendGrid (Producción)**
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.sendgrid.net
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=tu_sendgrid_api_key
   ```

---

## 🚨 TROUBLESHOOTING

### ❌ Error: "Application failed to start"

**Solución:**
1. Revisa logs en Render Dashboard
2. Verifica que `DATABASE_URL` sea correcto
3. Asegúrate de que Supabase esté activo

### ❌ Error: "Static files not loading"

**Solución:**
1. Verifica que `build.sh` ejecute `collectstatic`
2. Revisa `settings.py`:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

### ❌ Error: "Database connection failed"

**Solución:**
1. Verifica que `DATABASE_URL` incluya `?pgbouncer=true`
2. Revisa que la contraseña no tenga caracteres especiales sin escapar
3. Verifica IP whitelist en Supabase (debería permitir todas las IPs para Render)

### ❌ Error: "ModuleNotFoundError"

**Solución:**
1. Asegúrate de que el módulo esté en `requirements.txt`
2. Verifica que la versión sea compatible
3. Fuerza un redeploy

### ⚠️ App tarda mucho en cargar (primera carga)

**Es normal** - El plan Free de Render se apaga después de 15 min de inactividad.
La primera carga puede tardar 50-60 segundos.

**Soluciones:**
1. Usar plan pagado ($7/mes) para mantener siempre activo
2. Implementar un "ping" cada 10 minutos (con cron-job.org)
3. Avisar a los usuarios que la primera carga es lenta

---

## 📊 MONITOREO Y LOGS

### Ver Logs en Tiempo Real

1. Dashboard → Tu servicio
2. **Logs** (en el menú)
3. Verás todos los requests, errores, etc.

### Logs Útiles

```bash
# Ver migraciones
Applying inscripciones.0001_initial... OK
Applying inscripciones.0011_practica_dirigido_a... OK

# Ver requests
GET /admin/ HTTP/1.1 200 OK
POST /login/ HTTP/1.1 302 FOUND

# Ver errores
ERROR: No module named 'openai'
```

---

## 🔄 ACTUALIZACIONES FUTURAS

Cada vez que hagas cambios:

1. **Hacer commit y push**:
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push origin main
   ```

2. **Auto-deploy**:
   - Render detecta el push
   - Ejecuta `build.sh` automáticamente
   - Reinicia el servicio

3. **Deploy manual** (si desactivaste auto-deploy):
   - Dashboard → Tu servicio
   - Click en **"Manual Deploy"**

---

## 🎯 CHECKLIST FINAL

Antes de compartir la app, verifica:

- [ ] ✅ App accesible en URL de Render
- [ ] ✅ CSS y estilos funcionan
- [ ] ✅ Login/Registro funcionan
- [ ] ✅ Admin panel accesible
- [ ] ✅ 43 Carreras de ULEAM pobladas
- [ ] ✅ Base de datos conectada correctamente
- [ ] ✅ Chatbot responde (si OpenAI configurado)
- [ ] ✅ Crear práctica funciona
- [ ] ✅ Inscribirse a práctica funciona
- [ ] ✅ Evaluar postulante funciona
- [ ] ✅ Imágenes/documentos se suben correctamente

---

## 📞 SOPORTE

### Problemas con Render
- Docs: https://render.com/docs
- Status: https://status.render.com

### Problemas con Supabase
- Docs: https://supabase.com/docs
- Discord: https://discord.supabase.com

### Problemas con el Sistema
- Revisar `CUMPLIMIENTO_RETO_1.md`
- Revisar logs en Render
- Contactar al desarrollador

---

## 🎉 ¡LISTO!

Tu sistema de Prácticas Preprofesionales de ULEAM está en producción.

**URL de ejemplo:**
```
https://sistema-practicas-uleam.onrender.com
```

**Credenciales de Admin:**
- Usuario: `admin`
- Contraseña: La que definiste en `createsuperuser`

**Próximos Pasos:**
1. Crear usuarios de prueba
2. Configurar email real
3. Poblar con datos reales de ULEAM
4. Compartir URL con estudiantes/empresas/facultades
5. Monitorear errores y mejoras

---

**Fecha de despliegue:** 7 de Noviembre de 2025  
**Versión:** 2.0 - Sistema Completo con 43 Carreras ULEAM  
**Desarrollado con:** Django 5.2.7 + PostgreSQL (Supabase) + OpenAI
