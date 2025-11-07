# 📧 CONFIGURAR SMTP DE SUPABASE

## 🎯 Paso 1: Obtener credenciales SMTP de Supabase

### A. En tu Dashboard de Supabase:

1. **Ve a tu proyecto en Supabase:**
   - URL: https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd

2. **Navega a Settings (Configuración):**
   - Click en el ícono de engranaje en la barra lateral
   - Luego click en **Project Settings**

3. **Ve a la sección de Auth:**
   - En el menú lateral, busca **Authentication**
   - Luego **Email Templates** o **SMTP Settings**

4. **Haz clic en "SMTP Settings":**
   - Verás la opción para configurar SMTP personalizado
   - O puedes usar el SMTP interno de Supabase

### B. Opciones de configuración:

#### Opción 1: Usar SMTP interno de Supabase (Más fácil)

Supabase tiene su propio servicio SMTP integrado. Para usarlo:

**Configuración en .env:**
```env
# Email Configuration - Supabase SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.supabase.io
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu_supabase_service_role_key
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <noreply@tu-proyecto.supabase.co>
SITE_URL=http://localhost:8000
```

**⚠️ IMPORTANTE:** 
- Usa tu `SUPABASE_SERVICE_ROLE_KEY` (NO el anon key)
- El Service Role Key tiene más permisos

#### Opción 2: Configurar SMTP personalizado en Supabase

Si quieres usar Gmail, SendGrid u otro servicio a través de Supabase:

1. En Supabase Dashboard → Project Settings → Auth → SMTP Settings
2. Haz clic en **"Set up custom SMTP"** (Setup SMTP en la imagen)
3. Completa los datos del proveedor que elijas:

**Para Gmail:**
```
Host: smtp.gmail.com
Port: 587
Username: guanoluisamildreth@gmail.com
Password: [tu contraseña de aplicación]
From Email: guanoluisamildreth@gmail.com
```

**Para SendGrid:**
```
Host: smtp.sendgrid.net
Port: 587
Username: apikey
Password: SG.tu_api_key
From Email: practicas@uleam.edu.ec
```

---

## 🎯 Paso 2: Obtener Service Role Key

### A. Ir a API Settings:

1. En tu Dashboard de Supabase
2. Settings → API
3. Busca **Project API keys**

### B. Copiar Service Role Key:

Verás dos keys:
- **anon / public:** Este ya lo tienes en .env
- **service_role:** Este es el que necesitas ⬅️ CÓPIALO

**⚠️ MUY IMPORTANTE:** 
- El service_role key es SECRETO
- NUNCA lo expongas en el frontend
- Solo úsalo en el backend (Django)

---

## 🎯 Paso 3: Configurar en Django

### Actualizar .env:

```env
# Supabase Keys
SUPABASE_URL=https://owrgthzfdlnhkiwzdgbd.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # anon key (ya lo tienes)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # service role key NUEVO

# Email Configuration - Supabase SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.supabase.io
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu_supabase_service_role_key_aqui
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <noreply@owrgthzfdlnhkiwzdgbd.supabase.co>
SITE_URL=http://localhost:8000
```

---

## 🎯 Paso 4: Probar la configuración

```bash
python test_envio_email.py
```

Ingresa tu email para recibir un correo de prueba.

---

## ⚠️ NOTA IMPORTANTE

Según la imagen que compartiste, Supabase muestra:

> "You're using the built-in email service. This service has rate limits and is not meant to be used for production apps."

Esto significa que:

✅ **Para desarrollo/testing:** Funciona perfecto
⚠️ **Para producción:** Supabase recomienda configurar SMTP personalizado

### Límites del servicio built-in de Supabase:
- Limitado en cantidad de emails/hora
- Puede tener delays
- No es 100% confiable para producción

### Recomendación para producción:

1. **Opción A:** Haz clic en **"Set up SMTP"** en Supabase y configura SendGrid
2. **Opción B:** Usa SendGrid directamente desde Django (más rápido)

---

## 📋 Resumen de opciones:

| Opción | Configuración | Producción | Recomendación |
|--------|--------------|------------|---------------|
| Supabase built-in SMTP | 5 min | ⚠️ Limitado | Solo testing |
| SMTP personalizado en Supabase | 10 min | ✅ Sí | Buena |
| SendGrid directo en Django | 10 min | ✅ Sí | Mejor |
| Gmail directo en Django | 5 min | ⚠️ Limitado | Testing |

---

## 🚀 ¿Qué hacer ahora?

### Para testing rápido (5 minutos):
1. Obtén tu `SUPABASE_SERVICE_ROLE_KEY`
2. Actualiza `.env` con la configuración de arriba
3. Prueba con `python test_envio_email.py`

### Para producción (10 minutos):
1. Haz clic en **"Set up SMTP"** en Supabase
2. Configura SendGrid siguiendo `CONFIGURAR_EMAIL_PRODUCCION.md`
3. Tendrás emails profesionales y confiables

---

**¿Necesitas ayuda para obtener el Service Role Key?** Te guío paso a paso.
