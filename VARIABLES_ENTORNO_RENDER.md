# ⚙️ VARIABLES DE ENTORNO PARA RENDER

## 📋 LISTA COMPLETA DE VARIABLES

Copia y pega estas variables en Render Dashboard → Environment Variables

---

## 🔴 OBLIGATORIAS

### Django Core

```
SECRET_KEY
```
**Valor:** Dejar que Render lo genere automáticamente (click en "Generate")
**Descripción:** Clave secreta para Django

```
DEBUG
```
**Valor:** `False`
**Descripción:** Modo debug desactivado para producción

```
ALLOWED_HOSTS
```
**Valor:** `.onrender.com,localhost,127.0.0.1`
**Descripción:** Hosts permitidos para acceder a la app

```
CSRF_TRUSTED_ORIGINS
```
**Valor:** `https://*.onrender.com`
**Descripción:** Orígenes confiables para CSRF

---

### Base de Datos (Supabase)

```
DATABASE_URL
```
**Valor:** `postgresql://postgres.owrgthzfdlnhkiwzdgbd:Milxi26.@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true`
**Descripción:** URL de conexión a PostgreSQL en Supabase

```
SUPABASE_URL
```
**Valor:** `https://owrgthzfdlnhkiwzdgbd.supabase.co`
**Descripción:** URL del proyecto Supabase

```
SUPABASE_KEY
```
**Valor:** `[OBTENER DE SUPABASE DASHBOARD]`
**Descripción:** Anon/Public key de Supabase

**🔑 CÓMO OBTENER SUPABASE_KEY:**
1. Ve a: https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/settings/api
2. En la sección **"Project API keys"**
3. Copia la clave **"anon"** o **"public"**
4. Pégala en esta variable

---

## 🟡 OPCIONALES (PERO RECOMENDADAS)

### OpenAI (Para Chatbot Inteligente)

```
OPENAI_API_KEY
```
**Valor:** `[OBTENER DE OPENAI DASHBOARD]`
**Descripción:** API Key para el chatbot con IA

**🔑 CÓMO OBTENER OPENAI_API_KEY:**
1. Ve a: https://platform.openai.com/api-keys
2. Click en **"Create new secret key"**
3. Dale un nombre: "Sistema Prácticas ULEAM"
4. Copia la clave (¡solo se muestra una vez!)
5. Pégala en esta variable

**⚠️ IMPORTANTE:**
- Sin esta clave, el chatbot usará respuestas predefinidas (limitadas)
- Con esta clave, el chatbot usará GPT-4 (inteligencia avanzada)
- Cuesta ~$0.03 por 1000 mensajes (muy económico)

---

### Email (Configuración)

```
EMAIL_BACKEND
```
**Valor:** `django.core.mail.backends.console.EmailBackend`
**Descripción:** Backend de email (console para desarrollo)

**Alternativas:**
- Console (desarrollo): `django.core.mail.backends.console.EmailBackend`
- SMTP (producción): `django.core.mail.backends.smtp.EmailBackend`

```
DEFAULT_FROM_EMAIL
```
**Valor:** `noreply@uleam.edu.ec`
**Descripción:** Email remitente por defecto

---

### Python Version

```
PYTHON_VERSION
```
**Valor:** `3.11.0`
**Descripción:** Versión de Python a usar

---

## 🟢 OPCIONALES AVANZADAS (Email Real - Producción)

### Si quieres enviar emails reales con Gmail:

```
EMAIL_BACKEND
```
**Valor:** `django.core.mail.backends.smtp.EmailBackend`

```
EMAIL_HOST
```
**Valor:** `smtp.gmail.com`

```
EMAIL_PORT
```
**Valor:** `587`

```
EMAIL_USE_TLS
```
**Valor:** `True`

```
EMAIL_HOST_USER
```
**Valor:** `tu_email@gmail.com`

```
EMAIL_HOST_PASSWORD
```
**Valor:** `[APP PASSWORD DE GMAIL]`

**🔑 CÓMO OBTENER APP PASSWORD DE GMAIL:**
1. Ve a: https://myaccount.google.com/apppasswords
2. Selecciona "Correo" y "Otro (nombre personalizado)"
3. Escribe: "Sistema Prácticas ULEAM"
4. Copia la contraseña de 16 caracteres
5. Pégala en `EMAIL_HOST_PASSWORD`

---

### Si quieres usar SendGrid (Recomendado para producción):

```
EMAIL_BACKEND
```
**Valor:** `django.core.mail.backends.smtp.EmailBackend`

```
EMAIL_HOST
```
**Valor:** `smtp.sendgrid.net`

```
EMAIL_PORT
```
**Valor:** `587`

```
EMAIL_USE_TLS
```
**Valor:** `True`

```
EMAIL_HOST_USER
```
**Valor:** `apikey`

```
EMAIL_HOST_PASSWORD
```
**Valor:** `[API KEY DE SENDGRID]`

**🔑 CÓMO OBTENER SENDGRID API KEY:**
1. Crea cuenta: https://signup.sendgrid.com/
2. Dashboard → Settings → API Keys
3. Create API Key (Full Access)
4. Copia la key
5. Pégala en `EMAIL_HOST_PASSWORD`

---

## 📝 RESUMEN DE VARIABLES MÍNIMAS

Para un deploy básico funcional, necesitas SOLO estas:

```env
SECRET_KEY=[Auto-generado por Render]
DEBUG=False
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
DATABASE_URL=postgresql://postgres.owrgthzfdlnhkiwzdgbd:Milxi26.@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
SUPABASE_URL=https://owrgthzfdlnhkiwzdgbd.supabase.co
SUPABASE_KEY=[OBTENER DE SUPABASE]
```

---

## 🎯 CONFIGURACIÓN RECOMENDADA COMPLETA

Para producción con todas las funcionalidades:

```env
# Django Core
SECRET_KEY=[Auto-generado]
DEBUG=False
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://*.onrender.com

# Base de Datos
DATABASE_URL=postgresql://postgres.owrgthzfdlnhkiwzdgbd:Milxi26.@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
SUPABASE_URL=https://owrgthzfdlnhkiwzdgbd.supabase.co
SUPABASE_KEY=[OBTENER DE SUPABASE]

# OpenAI (Chatbot)
OPENAI_API_KEY=[OBTENER DE OPENAI]

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@uleam.edu.ec

# Python
PYTHON_VERSION=3.11.0
```

---

## 🔐 SEGURIDAD

### ⚠️ NUNCA SUBAS AL REPOSITORIO:

- ❌ API Keys (OpenAI, SendGrid, etc.)
- ❌ Passwords de base de datos
- ❌ SECRET_KEY
- ❌ Credenciales de email

### ✅ SIEMPRE USA:

- ✅ Variables de entorno en Render
- ✅ `.env` en local (y agregarlo a `.gitignore`)
- ✅ `python-decouple` para leer variables

---

## 🧪 TESTING DE VARIABLES

Para verificar que las variables estén correctas:

1. Deploy en Render
2. Ve al Shell de Render
3. Ejecuta:

```python
python manage.py shell
```

Luego:

```python
from django.conf import settings

# Verificar DEBUG
print(f"DEBUG: {settings.DEBUG}")  # Debe ser False

# Verificar ALLOWED_HOSTS
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")

# Verificar DATABASE
print(f"DB: {settings.DATABASES['default']['NAME']}")

# Verificar SUPABASE
print(f"SUPABASE_URL: {settings.SUPABASE_URL}")

# Verificar OPENAI (si configurado)
try:
    print(f"OPENAI: {settings.OPENAI_API_KEY[:10]}...")
except:
    print("OPENAI: No configurado")
```

---

## 📊 PRIORIDADES

### 🔴 CRÍTICAS (Sistema no funciona sin ellas):
1. `SECRET_KEY`
2. `DEBUG`
3. `ALLOWED_HOSTS`
4. `DATABASE_URL`
5. `SUPABASE_URL`
6. `SUPABASE_KEY`

### 🟡 IMPORTANTES (Funcionalidad limitada):
7. `OPENAI_API_KEY` (Chatbot inteligente)
8. `EMAIL_BACKEND` (Notificaciones)

### 🟢 OPCIONALES (Mejoras):
9. `CSRF_TRUSTED_ORIGINS` (Seguridad)
10. `PYTHON_VERSION` (Control de versión)

---

**Última actualización:** 7 de Noviembre de 2025  
**Autor:** GitHub Copilot  
**Versión:** 2.0
