# 📧 CONFIGURAR EMAIL PARA PRODUCCIÓN - PASO A PASO

## 🎯 Opción 1: SendGrid (RECOMENDADA) - 100 emails/día GRATIS

### Paso 1: Crear cuenta en SendGrid

1. Ve a: **https://signup.sendgrid.com/**
2. Completa el formulario de registro:
   - Email: Tu correo institucional o personal
   - Contraseña: Una contraseña segura
   - Haz clic en "Create Account"

3. **Verificar tu email:**
   - Revisa tu correo
   - Haz clic en el enlace de verificación
   - Inicia sesión en SendGrid

### Paso 2: Completar el perfil (obligatorio)

SendGrid te pedirá información:

1. **Tell us about yourself:**
   - First Name: Tu nombre
   - Last Name: Tu apellido
   - Company: ULEAM o Universidad Laica Eloy Alfaro de Manabí
   - Website: https://uleam.edu.ec (o tu dominio)

2. **What will you use SendGrid for?**
   - Selecciona: "Transactional Email" (emails transaccionales)

3. **How many emails do you send per month?**
   - Selecciona: "Less than 100" o "100 - 1,000"

4. **Complete your profile:**
   - Completa la información restante
   - Haz clic en "Get Started!"

### Paso 3: Crear un API Key

1. En el dashboard de SendGrid, ve a:
   - **Settings** (menú izquierdo)
   - **API Keys**

2. Haz clic en **"Create API Key"**

3. Configurar el API Key:
   - **API Key Name:** `Sistema-Practicas-ULEAM-Produccion`
   - **API Key Permissions:** Selecciona **"Full Access"** o **"Restricted Access"** con permisos de Mail Send

4. **MUY IMPORTANTE:** 
   - Haz clic en "Create & View"
   - **COPIA EL API KEY INMEDIATAMENTE** (se muestra solo una vez)
   - Ejemplo: `SG.Xabcd1234efgh5678ijkl9012mnop3456qrst7890uvwx`
   - Guárdalo en un lugar seguro (lo necesitarás en el Paso 5)

### Paso 4: Verificar el dominio de email (Opcional pero recomendado)

1. Ve a **Settings > Sender Authentication**

2. **Opción A - Single Sender Verification (Rápido):**
   - Haz clic en "Verify a Single Sender"
   - Completa el formulario:
     - From Name: `Sistema de Prácticas ULEAM`
     - From Email Address: Tu correo (ej: `practicas@uleam.edu.ec` o tu Gmail)
     - Reply To: El mismo email
     - Company Address: Dirección de ULEAM
     - City, State, Country: Manta, Manabí, Ecuador
   - Haz clic en "Create"
   - **Verifica tu email** (recibirás un correo de SendGrid)

3. **Opción B - Domain Authentication (Avanzado - si tienes dominio):**
   - Si tienes acceso a los DNS de uleam.edu.ec
   - Sigue las instrucciones para agregar registros DNS
   - Esto permite usar `noreply@uleam.edu.ec`

### Paso 5: Configurar variables de entorno

#### A. **Para desarrollo local (.env):**

Crea o edita el archivo `.env` en la raíz del proyecto:

```env
# Email Configuration - SendGrid
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.Xabcd1234efgh5678ijkl9012mnop3456qrst7890uvwx
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <practicas@uleam.edu.ec>
SITE_URL=http://localhost:8000
```

**IMPORTANTE:** Reemplaza:
- `EMAIL_HOST_PASSWORD` con tu API Key de SendGrid
- `DEFAULT_FROM_EMAIL` con el email que verificaste en el Paso 4

#### B. **Para producción en Render:**

1. Ve a tu proyecto en Render.com
2. Selecciona tu servicio (web service)
3. Ve a la pestaña **"Environment"**
4. Agrega estas variables:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.Xabcd1234efgh5678ijkl9012mnop3456qrst7890uvwx
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <practicas@uleam.edu.ec>
SITE_URL=https://tu-app.onrender.com
```

**IMPORTANTE:** 
- Usa tu API Key real de SendGrid
- Actualiza `SITE_URL` con tu URL de Render

### Paso 6: Probar el envío de emails

#### Opción A - Desde la terminal:

```bash
python manage.py shell
```

Luego ejecuta:

```python
from django.core.mail import send_mail

send_mail(
    subject='Prueba de Email - Sistema ULEAM',
    message='Este es un email de prueba desde el sistema de prácticas.',
    from_email='practicas@uleam.edu.ec',
    recipient_list=['tu_email_personal@gmail.com'],
    fail_silently=False,
)
```

Si recibes `1` como respuesta, ¡funcionó! Revisa tu email.

#### Opción B - Registrar un usuario de prueba:

1. Inicia el servidor: `python manage.py runserver`
2. Ve a: http://localhost:8000/registro/
3. Registra un nuevo usuario con tu email personal
4. **Revisa tu bandeja de entrada** (y spam) para el email de verificación

### Paso 7: Monitorear emails enviados

1. En SendGrid, ve a **Activity**
2. Aquí verás todos los emails enviados, entregados, abiertos, etc.
3. Útil para debugging si un email no llega

---

## 🎯 Opción 2: Gmail (Alternativa - Límite 500 emails/día)

### Paso 1: Habilitar autenticación de 2 pasos

1. Ve a: **https://myaccount.google.com/security**
2. Busca **"Verificación en dos pasos"**
3. Haz clic en **"Comenzar"**
4. Sigue las instrucciones (necesitarás tu teléfono)

### Paso 2: Generar contraseña de aplicación

1. Ve a: **https://myaccount.google.com/apppasswords**
2. Si no puedes acceder, primero completa el Paso 1

3. Generar la contraseña:
   - **Seleccionar app:** Elige "Correo"
   - **Seleccionar dispositivo:** Elige "Otro (nombre personalizado)"
   - Escribe: `Sistema Practicas ULEAM`
   - Haz clic en **"Generar"**

4. **COPIA LA CONTRASEÑA DE 16 CARACTERES**
   - Ejemplo: `abcd efgh ijkl mnop`
   - Gmail la muestra una sola vez
   - Guárdala en un lugar seguro

### Paso 3: Configurar variables de entorno

#### A. **Para desarrollo local (.env):**

```env
# Email Configuration - Gmail
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <tu_correo@gmail.com>
SITE_URL=http://localhost:8000
```

**IMPORTANTE:** Reemplaza:
- `EMAIL_HOST_USER` con tu Gmail
- `EMAIL_HOST_PASSWORD` con la contraseña de aplicación (CON espacios)

#### B. **Para producción en Render:**

1. Ve a tu proyecto en Render.com
2. Pestaña **"Environment"**
3. Agrega las mismas variables con tus valores reales
4. Actualiza `SITE_URL=https://tu-app.onrender.com`

### Paso 4: Probar

Igual que con SendGrid (ver Opción 1, Paso 6)

---

## ⚠️ Comparación: SendGrid vs Gmail

| Característica | SendGrid | Gmail |
|---------------|----------|-------|
| **Límite diario** | 100 emails/día (gratis) | 500 emails/día |
| **Límite mensual** | 3,000 emails/mes | 15,000 emails/mes |
| **Configuración** | 10 minutos | 5 minutos |
| **Profesionalismo** | ⭐⭐⭐⭐⭐ Muy profesional | ⭐⭐⭐ Aceptable |
| **Monitoreo** | ✅ Dashboard completo | ❌ No disponible |
| **Reputación** | ✅ Alta (IP compartida profesional) | ⚠️ Puede ir a spam |
| **Escalabilidad** | ✅ Fácil (planes de pago) | ❌ Limitada |
| **Ideal para** | Producción | Desarrollo/Testing |

**Recomendación:** Usa **SendGrid** para producción y Gmail para desarrollo local.

---

## 🔍 Verificar configuración actual

Ejecuta este script para ver tu configuración actual:

```bash
python test_autenticacion.py
```

Deberías ver:

```
EMAIL_BACKEND: django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST: smtp.sendgrid.net (o smtp.gmail.com)
EMAIL_PORT: 587
EMAIL_HOST_USER: apikey (o tu@gmail.com)
✅ Configurado correctamente
```

---

## 🐛 Solución de Problemas

### Error: "SMTPAuthenticationError 535"

**Con SendGrid:**
- Verifica que el API Key esté correcto
- Asegúrate que `EMAIL_HOST_USER=apikey` (literalmente "apikey")
- Regenera el API Key si es necesario

**Con Gmail:**
- Verifica que la autenticación de 2 pasos esté activa
- Usa la contraseña de aplicación, NO tu contraseña normal
- Copia la contraseña CON espacios

### Error: "Connection timed out"

- Verifica que tu firewall no bloquee el puerto 587
- Prueba con: `EMAIL_PORT=465` y agrega `EMAIL_USE_SSL=True`

### Los emails van a spam

**SendGrid:**
- Completa la verificación de dominio (Paso 4)
- Asegúrate que el remitente esté verificado

**Gmail:**
- Es normal, pide a los usuarios revisar spam
- O usa SendGrid para mejor reputación

### Los emails no llegan

1. Verifica en SendGrid Activity o Gmail enviados
2. Revisa la carpeta de spam
3. Verifica que `DEFAULT_FROM_EMAIL` sea el email verificado
4. Ejecuta `python test_autenticacion.py` para ver errores

---

## ✅ Checklist Final - Producción

Antes de deploy:

- [ ] API Key de SendGrid creado y guardado
- [ ] Email de remitente verificado en SendGrid
- [ ] Variables de entorno configuradas en Render
- [ ] `SITE_URL` actualizado a tu dominio de producción
- [ ] Email de prueba enviado y recibido correctamente
- [ ] `DEBUG=False` en producción
- [ ] `ALLOWED_HOSTS` incluye tu dominio
- [ ] Emails de verificación funcionando
- [ ] Emails de recuperación funcionando

---

## 📊 Límites y Costos

### SendGrid - Plan Gratuito:
- ✅ 100 emails/día
- ✅ 3,000 emails/mes
- ✅ Gratis para siempre
- 💰 Planes pagos desde $19.95/mes (100,000 emails/mes)

### Gmail:
- ✅ 500 emails/día
- ✅ 15,000 emails/mes
- ✅ Gratis
- ⚠️ Cuenta personal, no profesional

---

## 🎓 Siguiente Paso

Una vez configurado:

1. **Prueba en local:**
   ```bash
   python manage.py runserver
   ```
   - Registra un usuario
   - Verifica que llegue el email

2. **Deploy a producción:**
   - Configura las variables en Render
   - Haz un nuevo deploy
   - Prueba el registro en producción

3. **Monitorea:**
   - SendGrid: Dashboard → Activity
   - Verifica que los emails se entreguen

---

**¿Necesitas ayuda?** Revisa la sección de solución de problemas o ejecuta `python test_autenticacion.py`

**Fecha:** 7 de Noviembre de 2025  
**Sistema:** Prácticas Preprofesionales ULEAM v3.0
