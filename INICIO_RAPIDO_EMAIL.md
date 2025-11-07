# 🚀 CONFIGURACIÓN RÁPIDA PARA PRODUCCIÓN

## ✅ Estado Actual

**MODO ACTUAL:** Consola (los emails se muestran en terminal)

Para enviar emails REALES en producción, necesitas configurar un servicio SMTP.

---

## 📋 OPCIÓN RECOMENDADA: SendGrid (10 minutos)

### ¿Por qué SendGrid?
- ✅ **100 emails/día GRATIS** (suficiente para empezar)
- ✅ Dashboard para monitorear emails
- ✅ Alta reputación (no van a spam)
- ✅ Fácil de configurar
- ✅ Profesional

### Pasos Rápidos:

#### 1️⃣ Crear cuenta (3 min)
```
🌐 https://signup.sendgrid.com/
```
- Email: guanoluisamildreth@gmail.com
- Completa el registro
- Verifica tu email

#### 2️⃣ Crear API Key (2 min)
```
1. Inicia sesión en SendGrid
2. Ve a: Settings > API Keys
3. Clic en "Create API Key"
4. Nombre: Sistema-Practicas-ULEAM
5. Permisos: Full Access
6. Clic en "Create & View"
7. ⚠️ COPIA EL API KEY (solo se muestra una vez)
   
   Ejemplo: SG.Xabcd1234efgh5678...
```

#### 3️⃣ Verificar remitente (3 min)
```
1. Ve a: Settings > Sender Authentication
2. Clic en "Verify a Single Sender"
3. Completa:
   - From Name: Sistema de Prácticas ULEAM
   - From Email: guanoluisamildreth@gmail.com
   - Reply To: guanoluisamildreth@gmail.com
   - Dirección: Av. Circunvalación, Manta, Manabí, Ecuador
4. Clic en "Create"
5. Verifica tu email (te llegará un correo de SendGrid)
```

#### 4️⃣ Configurar en .env (2 min)

**Abre el archivo `.env` y REEMPLAZA estas líneas:**

```env
# COMENTA ESTA LÍNEA:
#EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
#SITE_URL=http://localhost:8000

# DESCOMENTA Y COMPLETA ESTAS LÍNEAS:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.tu_api_key_que_copiaste_en_el_paso_2
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <guanoluisamildreth@gmail.com>
SITE_URL=http://localhost:8000
```

**⚠️ IMPORTANTE:** Reemplaza `EMAIL_HOST_PASSWORD` con tu API Key real de SendGrid

#### 5️⃣ Probar (1 min)

```bash
python test_envio_email.py
```

Ingresa tu email: `guanoluisamildreth@gmail.com`

**Si funciona:**
- ✅ Recibirás un email real
- ✅ Revisa tu bandeja de entrada (y spam)

---

## 📋 ALTERNATIVA: Gmail (5 minutos)

### ¿Por qué Gmail?
- ✅ Rápido de configurar
- ✅ No requiere verificación de dominio
- ⚠️ Límite: 500 emails/día
- ⚠️ Puede ir a spam

### Pasos Rápidos:

#### 1️⃣ Habilitar autenticación 2 pasos (2 min)
```
🌐 https://myaccount.google.com/security
```
1. Busca "Verificación en dos pasos"
2. Haz clic en "Comenzar"
3. Sigue las instrucciones

#### 2️⃣ Crear contraseña de aplicación (2 min)
```
🌐 https://myaccount.google.com/apppasswords
```
1. Seleccionar app: **Correo**
2. Seleccionar dispositivo: **Otro** → escribe: `Sistema Prácticas ULEAM`
3. Haz clic en **Generar**
4. **COPIA LA CONTRASEÑA** (16 caracteres con espacios)
   
   Ejemplo: `abcd efgh ijkl mnop`

#### 3️⃣ Configurar en .env (1 min)

**Abre el archivo `.env` y REEMPLAZA estas líneas:**

```env
# COMENTA ESTA LÍNEA:
#EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
#SITE_URL=http://localhost:8000

# DESCOMENTA Y COMPLETA ESTAS LÍNEAS:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=guanoluisamildreth@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <guanoluisamildreth@gmail.com>
SITE_URL=http://localhost:8000
```

**⚠️ IMPORTANTE:** 
- Usa TU contraseña de aplicación (la de 16 caracteres)
- Cópiala CON espacios

#### 4️⃣ Probar

```bash
python test_envio_email.py
```

---

## 🌐 CONFIGURAR PARA PRODUCCIÓN EN RENDER

Cuando hagas deploy a Render.com:

### 1️⃣ Ve a tu proyecto en Render
```
🌐 https://dashboard.render.com/
```

### 2️⃣ Selecciona tu servicio web

### 3️⃣ Ve a la pestaña "Environment"

### 4️⃣ Agrega estas variables:

**Si usas SendGrid:**
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.tu_api_key_real
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <guanoluisamildreth@gmail.com>
SITE_URL=https://tu-app.onrender.com
```

**Si usas Gmail:**
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=guanoluisamildreth@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <guanoluisamildreth@gmail.com>
SITE_URL=https://tu-app.onrender.com
```

**⚠️ IMPORTANTE:** Actualiza `SITE_URL` con tu URL real de Render

### 5️⃣ Redeploy

Haz clic en "Manual Deploy" → "Deploy latest commit"

---

## ✅ Verificar que funciona

### En desarrollo local:

```bash
# 1. Probar configuración
python test_envio_email.py

# 2. Iniciar servidor
python manage.py runserver

# 3. Registrar usuario de prueba
http://localhost:8000/registro/

# 4. Revisar tu email real
```

### En producción (Render):

```bash
# 1. Ve a tu app en Render
https://tu-app.onrender.com/registro/

# 2. Registra un usuario
# 3. Revisa tu email real
# 4. Haz clic en el enlace de verificación
```

---

## 🎯 Qué sucede al registrarse

### ANTES (modo consola):
```
Usuario se registra → Email mostrado en terminal → Cuenta inactiva
```

### AHORA (modo SMTP configurado):
```
Usuario se registra 
  ↓
📧 Email REAL enviado a su correo
  ↓
Usuario abre su email
  ↓
Hace clic en "Verificar mi correo"
  ↓
✅ Cuenta activada
  ↓
Puede iniciar sesión
```

---

## 📊 Comparación

| Característica | Modo Consola | SendGrid | Gmail |
|---------------|--------------|----------|-------|
| Emails reales | ❌ No | ✅ Sí | ✅ Sí |
| Configuración | ✅ 0 min | ⚠️ 10 min | ⚠️ 5 min |
| Límite diario | ∞ | 100 | 500 |
| Para desarrollo | ✅ Ideal | ⚠️ Innecesario | ✅ Bueno |
| Para producción | ❌ No sirve | ✅ Ideal | ⚠️ Aceptable |
| Costo | Gratis | Gratis | Gratis |

---

## 🐛 Solución de Problemas

### Error: "SMTPAuthenticationError"

**SendGrid:**
- Verifica que `EMAIL_HOST_USER=apikey` (literal)
- Verifica que el API Key sea correcto
- Regenera el API Key si es necesario

**Gmail:**
- Verifica que la autenticación de 2 pasos esté activa
- Usa la contraseña de aplicación, NO tu contraseña normal
- Copia la contraseña CON espacios

### Los emails no llegan

1. Verifica la carpeta de **spam**
2. Asegúrate que el email de remitente esté verificado
3. En SendGrid: Ve a Activity para ver el estado del email
4. Ejecuta `python test_envio_email.py` para ver errores

---

## 📞 ¿Necesitas ayuda?

Lee la documentación completa:
- **CONFIGURAR_EMAIL_PRODUCCION.md** - Guía detallada
- **GUIA_RAPIDA_EMAIL.md** - Configuración rápida
- **AUTENTICACION_MEJORADA.md** - Documentación completa

O ejecuta:
```bash
python test_envio_email.py
```

---

**Siguiente paso:** Elige SendGrid o Gmail y sigue los pasos arriba ⬆️

**Fecha:** 7 de Noviembre de 2025  
**Sistema:** Prácticas ULEAM v3.0
